from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid
from typing import Optional
import json

from config import settings
from services.content_processor import ContentProcessor
from services.ai_service import AIService
from services.voice_service import VoiceService
from services.video_service import VideoService
from models.schemas import VideoRequest, VideoResponse, ProcessingStatus

app = FastAPI(title="EBook to Video AI Generator", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/outputs", StaticFiles(directory=settings.output_folder), name="outputs")

# Service instances
content_processor = ContentProcessor()
ai_service = AIService()
voice_service = VoiceService()
video_service = VideoService()

# In-memory storage for processing status (sẽ thay bằng Redis trong production)
processing_jobs = {}

@app.get("/")
async def root():
    return {"message": "EBook to Video AI Generator API", "status": "running"}

@app.post("/api/upload", response_model=dict)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    duration: int = Form(180),
    voice_style: str = Form("professional")
):
    """Upload ebook file hoặc URL để xử lý"""
    
    if not file and not url:
        raise HTTPException(status_code=400, detail="Cần upload file hoặc nhập URL")
    
    if duration > settings.max_video_duration:
        raise HTTPException(
            status_code=400, 
            detail=f"Thời lượng tối đa là {settings.max_video_duration} giây"
        )
    
    # Generate job ID
    job_id = str(uuid.uuid4())
    
    # Initialize job status
    processing_jobs[job_id] = {
        "status": "initialized",
        "progress": 0,
        "message": "Đang khởi tạo...",
        "result": None,
        "error": None
    }
    
    # Process in background
    background_tasks.add_task(
        process_content_to_video,
        job_id, file, url, duration, voice_style
    )
    
    return {"job_id": job_id, "message": "Đã bắt đầu xử lý"}

@app.get("/api/status/{job_id}")
async def get_processing_status(job_id: str):
    """Kiểm tra trạng thái xử lý"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Không tìm thấy job")
    
    return processing_jobs[job_id]

@app.get("/api/download/{job_id}")
async def download_video(job_id: str):
    """Download video đã tạo"""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Không tìm thấy job")
    
    job = processing_jobs[job_id]
    if job["status"] != "completed":
        raise HTTPException(status_code=400, detail="Video chưa được tạo xong")
    
    video_path = job["result"]["video_path"]
    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="File video không tồn tại")
    
    return FileResponse(
        path=video_path,
        filename=f"video_{job_id}.mp4",
        media_type="video/mp4"
    )

async def process_content_to_video(
    job_id: str, 
    file: Optional[UploadFile], 
    url: Optional[str], 
    duration: int, 
    voice_style: str
):
    """Background task để xử lý toàn bộ quy trình tạo video"""
    
    try:
        # Step 1: Extract content
        processing_jobs[job_id].update({
            "status": "processing",
            "progress": 10,
            "message": "Đang trích xuất nội dung..."
        })
        
        if file:
            content = await content_processor.extract_from_file(file)
        else:
            content = await content_processor.extract_from_url(url)
        
        # Step 2: Analyze content with AI
        processing_jobs[job_id].update({
            "progress": 30,
            "message": "Đang phân tích nội dung với AI..."
        })
        
        analysis = await ai_service.analyze_content(content, duration)
        script = analysis["script"]
        category = analysis["category"]
        
        # Step 3: Generate voice
        processing_jobs[job_id].update({
            "progress": 50,
            "message": "Đang tạo giọng đọc..."
        })
        
        audio_path = await voice_service.generate_speech(
            script, voice_style, job_id
        )
        
        # Step 4: Create video
        processing_jobs[job_id].update({
            "progress": 70,
            "message": "Đang tạo video..."
        })
        
        video_path = await video_service.create_video(
            script, audio_path, category, job_id
        )
        
        # Step 5: Generate marketing content
        processing_jobs[job_id].update({
            "progress": 90,
            "message": "Đang tạo caption và hashtag..."
        })
        
        marketing = await ai_service.generate_marketing_content(script, category)
        
        # Complete
        processing_jobs[job_id].update({
            "status": "completed",
            "progress": 100,
            "message": "Hoàn thành!",
            "result": {
                "video_path": video_path,
                "audio_path": audio_path,
                "script": script,
                "category": category,
                "marketing": marketing,
                "duration": duration
            }
        })
        
    except Exception as e:
        processing_jobs[job_id].update({
            "status": "error",
            "error": str(e),
            "message": f"Lỗi: {str(e)}"
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 