#!/usr/bin/env python3
"""
MVP HTTP Server cho TikTok Video Generator
Sử dụng http.server thay vì FastAPI
"""

import json
import os
import uuid
import threading
import time
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import logging
from pathlib import Path

# Import our services
try:
    from ai_services import content_processor, voice_generator, marketing_generator
    AI_SERVICES_AVAILABLE = True
    print("✅ AI Services loaded successfully")
except ImportError as e:
    AI_SERVICES_AVAILABLE = False
    print(f"⚠️ AI Services not available: {e}")
    print("🔄 Using simulation mode")

try:
    from content_extractor import content_extractor
    CONTENT_EXTRACTOR_AVAILABLE = True
    print("✅ Content Extractor loaded successfully")
except ImportError as e:
    CONTENT_EXTRACTOR_AVAILABLE = False
    print(f"⚠️ Content Extractor not available: {e}")

try:
    from video_generator import video_generator
    VIDEO_GENERATOR_AVAILABLE = True
    print("✅ Video Generator loaded successfully")
except ImportError as e:
    VIDEO_GENERATOR_AVAILABLE = False
    print(f"⚠️ Video Generator not available: {e}")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Tạo thư mục cần thiết
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Lưu trữ jobs đang xử lý (trong production sẽ dùng database)
jobs = {}

class MVPHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        logger.info(f"🔧 OPTIONS preflight request for {self.path}")
        
        # Send proper CORS preflight response
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS, HEAD')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Accept, Origin, X-Requested-With, X-HTTP-Method-Override')
        self.send_header('Access-Control-Max-Age', '86400')
        self.send_header('Access-Control-Allow-Credentials', 'false')
        self.send_header('Content-Length', '0')
        self.end_headers()
        
        logger.info(f"✅ CORS preflight response sent for {self.path}")

    def send_cors_headers(self):
        """Add comprehensive CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, Accept, Origin, X-Requested-With')
        self.send_header('Access-Control-Max-Age', '86400')
        self.send_header('Access-Control-Allow-Credentials', 'false')

    def do_GET(self):
        """Handle GET requests"""
        logger.info(f"GET request for {self.path}")
        
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            query_params = parse_qs(parsed_path.query)
            
            if path == "/":
                self.handle_root()
            elif path == "/health":
                self.handle_health()
            elif path.startswith("/api/job/"):
                job_id = path.split("/")[-1]
                self.handle_job_status(job_id)
            elif path.startswith("/api/download/"):
                file_id = path.split("/")[-1]
                self.handle_download(file_id)
            else:
                self.send_error(404, "Endpoint not found")
                
        except Exception as e:
            logger.error(f"Error handling GET request: {e}")
            self.send_error_response(500, f"Internal error: {str(e)}")

    def do_POST(self):
        """Handle POST requests"""
        logger.info(f"POST request for {self.path}")
        
        try:
            if self.path == "/api/upload":
                self.handle_upload()
            elif self.path == "/api/process":
                self.handle_process()
            else:
                self.send_error(404, "Endpoint not found")
                
        except Exception as e:
            logger.error(f"Error handling POST request: {e}")
            self.send_error_response(500, f"Internal error: {str(e)}")

    def handle_root(self):
        """Root endpoint - API info"""
        response_data = {
            "message": "TikTok Video Generator API",
            "status": "running",
            "server": "enhanced_mvp_v2_cors_fixed",
            "version": "1.0.0",
            "endpoints": {
                "GET /": "API info",
                "GET /health": "Health check",
                "POST /api/upload": "Upload file",
                "POST /api/process": "Process content",
                "GET /api/job/{id}": "Check job status",
                "GET /api/download/{id}": "Download result"
            }
        }
        self.send_json_response(response_data)

    def handle_health(self):
        """Enhanced health check endpoint with capabilities"""
        response_data = {
            "status": "OK",
            "server": "enhanced_mvp_server",
            "timestamp": int(time.time()),
            "jobs_count": len(jobs),
            "ai_services": AI_SERVICES_AVAILABLE,
            "content_extraction": CONTENT_EXTRACTOR_AVAILABLE,
            "video_generation": VIDEO_GENERATOR_AVAILABLE,
            "voice_generation": AI_SERVICES_AVAILABLE,
            "capabilities": {
                "real_ai_processing": AI_SERVICES_AVAILABLE,
                "pdf_extraction": CONTENT_EXTRACTOR_AVAILABLE,
                "url_extraction": CONTENT_EXTRACTOR_AVAILABLE,
                "video_creation": VIDEO_GENERATOR_AVAILABLE,
                "voice_synthesis": AI_SERVICES_AVAILABLE
            }
        }
        self.send_json_response(response_data)

    def handle_upload(self):
        """Handle file upload"""
        try:
            # Parse multipart form data (simplified)
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                self.send_error_response(400, "No file uploaded")
                return
                
            # Generate unique file ID
            file_id = str(uuid.uuid4())
            
            # Simulate file saving (trong thực tế sẽ parse multipart data)
            file_path = f"uploads/{file_id}.pdf"
            
            response_data = {
                "success": True,
                "file_id": file_id,
                "message": "File uploaded successfully",
                "file_path": file_path
            }
            self.send_json_response(response_data)
            
        except Exception as e:
            logger.error(f"Upload error: {e}")
            self.send_error_response(500, f"Upload failed: {str(e)}")

    def handle_process(self):
        """Handle content processing request"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            request_body = self.rfile.read(content_length).decode('utf-8')
            request_data = json.loads(request_body)
            
            # Validate request
            if 'content_type' not in request_data:
                self.send_error_response(400, "Missing content_type")
                return
                
            # Generate job ID
            job_id = str(uuid.uuid4())
            
            # Create job
            job = {
                "id": job_id,
                "status": "processing",
                "progress": 0,
                "created_at": int(time.time()),
                "content_type": request_data['content_type'],
                "file_id": request_data.get('file_id'),
                "url": request_data.get('url'),
                "settings": request_data.get('settings', {}),
                "result": None,
                "error": None
            }
            
            jobs[job_id] = job
            
            # Start processing in background
            threading.Thread(target=self.process_content_background, args=(job_id,)).start()
            
            response_data = {
                "success": True,
                "job_id": job_id,
                "message": "Processing started",
                "status": "processing"
            }
            self.send_json_response(response_data)
            
        except Exception as e:
            logger.error(f"Process error: {e}")
            self.send_error_response(500, f"Processing failed: {str(e)}")

    def handle_job_status(self, job_id):
        """Check job status"""
        try:
            if job_id not in jobs:
                self.send_error_response(404, "Job not found")
                return
                
            job = jobs[job_id]
            response_data = {
                "job_id": job_id,
                "status": job["status"],
                "progress": job["progress"],
                "created_at": job["created_at"],
                "result": job.get("result"),
                "error": job.get("error")
            }
            self.send_json_response(response_data)
            
        except Exception as e:
            logger.error(f"Job status error: {e}")
            self.send_error_response(500, f"Status check failed: {str(e)}")

    def handle_download(self, file_id):
        """Handle file download"""
        try:
            # Simulate file download
            file_path = f"outputs/{file_id}.mp4"
            
            if not os.path.exists(file_path):
                self.send_error_response(404, "File not found")
                return
                
            # Send file (simplified - trong thực tế sẽ stream file)
            response_data = {
                "success": True,
                "file_id": file_id,
                "download_url": f"/outputs/{file_id}.mp4",
                "message": "File ready for download"
            }
            self.send_json_response(response_data)
            
        except Exception as e:
            logger.error(f"Download error: {e}")
            self.send_error_response(500, f"Download failed: {str(e)}")

    def process_content_background(self, job_id):
        """Background processing with real AI services"""
        
        async def async_process():
            try:
                job = jobs[job_id]
                logger.info(f"Starting background processing for job {job_id} (AI: {AI_SERVICES_AVAILABLE})")
                
                # Step 1: Extract content
                job["progress"] = 10
                job["current_step"] = "Extracting content"
                
                # Real content extraction
                if CONTENT_EXTRACTOR_AVAILABLE:
                    logger.info(f"Job {job_id}: Using real content extraction")
                    if job["content_type"] == "url":
                        extracted_data = await content_extractor.extract_content("url", job.get('url', ''))
                    else:
                        # For file uploads, use file path
                        file_id = job.get('file_id', '')
                        file_path = f"uploads/{file_id}"
                        extracted_data = await content_extractor.extract_content("pdf", file_path)
                    
                    content = extracted_data.get('content', '')
                    content_metadata = extracted_data.get('metadata', {})
                else:
                    logger.info(f"Job {job_id}: Using simulated content extraction")
                    if job["content_type"] == "url":
                        content = f"Sample content from URL: {job.get('url', '')}"
                    else:
                        content = "Sample content from uploaded file"
                    content_metadata = {"title": "Sample Content"}
                
                logger.info(f"Job {job_id}: Content extracted ({len(content)} chars)")
                
                # Step 2: AI Content Analysis
                job["progress"] = 30
                job["current_step"] = "Analyzing with AI"
                
                if AI_SERVICES_AVAILABLE:
                    logger.info(f"Job {job_id}: Using real AI content analysis")
                    script_data = await content_processor.analyze_content(
                        content=content,
                        duration=job["settings"].get("duration", 180)
                    )
                else:
                    logger.info(f"Job {job_id}: Using simulated content analysis")
                    script_data = {
                        "hook": "📚 Bạn có biết bí mật này từ cuốn sách này không?",
                        "main_points": ["Điểm quan trọng", "Insight thú vị", "Kết luận"],
                        "script": "Generated script for TikTok video...",
                        "category": "education",
                        "keywords": ["sách", "kiến thức"],
                        "estimated_duration": job["settings"].get("duration", 180)
                    }
                    time.sleep(2)
                
                # Step 3: Voice Generation
                job["progress"] = 50
                job["current_step"] = "Generating voiceover"
                
                if AI_SERVICES_AVAILABLE:
                    logger.info(f"Job {job_id}: Using real voice generation")
                    voice_file = await voice_generator.generate_speech(
                        text=script_data['script'],
                        voice_style=job["settings"].get('voice_style', 'professional')
                    )
                else:
                    logger.info(f"Job {job_id}: Using simulated voice generation")
                    voice_file = f"outputs/simulated_voice_{job_id}.mp3"
                    time.sleep(3)
                
                # Step 4: Marketing Content
                job["progress"] = 70
                job["current_step"] = "Creating marketing content"
                
                if AI_SERVICES_AVAILABLE:
                    logger.info(f"Job {job_id}: Using real marketing generation")
                    marketing_data = await marketing_generator.generate_marketing(
                        script=script_data['script'],
                        category=script_data['category'],
                        keywords=script_data['keywords']
                    )
                else:
                    logger.info(f"Job {job_id}: Using simulated marketing generation")
                    marketing_data = {
                        "caption": "📚✨ Kiến thức vàng từ sách hay!",
                        "hashtags": ["#sachhay", "#kienthuc", "#viral", "#fyp"],
                        "description": "Video chia sẻ kiến thức từ sách hay",
                        "hook": "Bạn nghĩ gì về video này?"
                    }
                    time.sleep(1)
                
                # Step 5: Video Generation
                job["progress"] = 90
                job["current_step"] = "Generating video"
                
                if VIDEO_GENERATOR_AVAILABLE:
                    logger.info(f"Job {job_id}: Using real video generation")
                    video_result = await video_generator.generate_video(
                        script_data=script_data,
                        voice_file=voice_file,
                        settings=job["settings"]
                    )
                    video_path = video_result.get('video_path', '')
                    video_filename = video_result.get('filename', '')
                else:
                    logger.info(f"Job {job_id}: Using simulated video generation")
                    video_path = f"outputs/simulated_video_{job_id}.mp4"
                    video_filename = f"simulated_video_{job_id}.mp4"
                    time.sleep(3)
                
                # Complete job
                job["status"] = "completed"
                job["progress"] = 100
                job["current_step"] = "Completed"
                job["result"] = {
                    "video_file": video_filename,
                    "video_path": video_path,
                    "voice_file": voice_file,
                    "script": script_data['script'],
                    "script_data": script_data,
                    "content_metadata": content_metadata if 'content_metadata' in locals() else {},
                    "duration": f"{job['settings'].get('duration', 60)} seconds",
                    "format": "MP4",
                    "resolution": "1080x1920",
                    "voice_style": job["settings"].get('voice_style', 'professional'),
                    "marketing": marketing_data,
                    "ai_powered": AI_SERVICES_AVAILABLE,
                    "content_extraction": CONTENT_EXTRACTOR_AVAILABLE,
                    "video_generation": VIDEO_GENERATOR_AVAILABLE
                }
                
                logger.info(f"✅ Job {job_id} completed successfully (AI: {AI_SERVICES_AVAILABLE})")
                
            except Exception as e:
                logger.error(f"❌ Background processing error for job {job_id}: {e}")
                job["status"] = "failed"
                job["error"] = str(e)
        
        # Run async function in thread
        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(async_process())
            loop.close()
        
        thread = threading.Thread(target=run_async)
        thread.start()

    def send_json_response(self, data, status_code=200):
        """Send JSON response with CORS headers"""
        try:
            json_data = json.dumps(data, indent=2)
            self.send_response(status_code)
            self.send_cors_headers()  # CORS headers for all responses
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(json_data.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
            logger.info(f"✅ JSON response sent ({status_code}): {json_data[:100]}...")
        except Exception as e:
            logger.error(f"❌ Error sending JSON response: {e}")
            self.send_error(500, f"Response error: {str(e)}")

    def send_error_response(self, status_code, message):
        """Send error response with CORS headers"""
        error_data = {
            "error": True,
            "status_code": status_code,
            "message": message,
            "timestamp": int(time.time())
        }
        self.send_json_response(error_data, status_code)

    def log_message(self, format, *args):
        """Override to use logger"""
        logger.info(format % args)

def run_mvp_server(host='127.0.0.1', port=8005):
    """Start the MVP HTTP server"""
    try:
        server_address = (host, port)
        httpd = HTTPServer(server_address, MVPHandler)
        logger.info(f"🚀 MVP Server starting on http://{host}:{port}")
        logger.info("Available endpoints:")
        logger.info("  GET  /          - API info")
        logger.info("  GET  /health    - Health check")
        logger.info("  POST /api/upload - Upload file")
        logger.info("  POST /api/process - Process content")
        logger.info("  GET  /api/job/{id} - Job status")
        logger.info("  GET  /api/download/{id} - Download result")
        logger.info("✅ Server ready!")
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server failed to start: {e}")
        raise

if __name__ == "__main__":
    import os
    print("🔧 Starting TikTok Video Generator MVP Server...")
    
    # Get port from environment (Railway sets PORT automatically)
    port = int(os.environ.get('PORT', 8005))
    host = os.environ.get('HOST', '0.0.0.0')  # Railway needs 0.0.0.0
    
    run_mvp_server(host=host, port=port) 