# 🎬 TikTok Video Generator

Tự động tạo video TikTok từ nội dung văn bản/ebook sử dụng AI.

## ✨ Tính năng

- 📖 Trích xuất nội dung từ PDF, URL, văn bản
- 🤖 Phân tích và tối ưu nội dung bằng AI 
- 🎙️ Tạo giọng đọc tự động
- 🎥 Tạo video TikTok định dạng dọc (9:16)
- 📱 Giao diện web thân thiện
- ⚡ API RESTful hoàn chỉnh

## 🛠️ Công nghệ sử dụng

### Backend
- **FastAPI** - Web framework
- **OpenAI** - Phân tích nội dung AI
- **ElevenLabs** - Text-to-Speech
- **MoviePy** - Xử lý video
- **PDFPlumber** - Đọc PDF
- **SQLAlchemy** - Database ORM

### Frontend
- **Next.js** - React framework
- **TypeScript** - Type safety
- **TailwindCSS** - Styling
- **Shadcn/ui** - UI components

## 🚀 Cài đặt

### 1. Clone repository
```bash
git clone https://github.com/yourusername/tiktok-video-generator.git
cd tiktok-video-generator
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### 3. Environment Variables
Tạo file `.env` trong thư mục backend:
```env
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

### 4. Chạy Backend
```bash
python mvp_server.py
```
Server sẽ chạy tại: http://127.0.0.1:8005

### 5. Frontend Setup (tùy chọn)
```bash
cd frontend
npm install
npm run dev
```

## 📖 Sử dụng

### API Endpoints

- `GET /` - Thông tin API
- `GET /health` - Kiểm tra sức khỏe server
- `POST /api/process` - Xử lý nội dung
- `GET /api/job/{id}` - Trạng thái công việc
- `GET /api/download/{id}` - Tải video

### Ví dụ sử dụng

```bash
# Xử lý URL
curl -X POST "http://127.0.0.1:8005/api/process" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com/article", "use_ai": true}'
```

## 📁 Cấu trúc thư mục

```
tiktok-video-generator/
├── backend/
│   ├── mvp_server.py          # Server chính
│   ├── ai_services.py         # Tích hợp AI
│   ├── content_extractor.py   # Trích xuất nội dung
│   ├── video_generator.py     # Tạo video
│   └── requirements.txt       # Dependencies
├── frontend/                  # Frontend (tùy chọn)
├── outputs/                   # Video đầu ra
├── .gitignore
└── README.md
```

## 🔧 Cấu hình

### AI Services
- OpenAI GPT-4 cho phân tích nội dung
- ElevenLabs cho text-to-speech
- Simulation mode khi không có API key

### Video Settings
- Độ phân giải: 1080x1920 (TikTok format)
- Thời lượng: Tự động dựa trên nội dung
- Audio: High quality voice synthesis

## 🐛 Troubleshooting

### Lỗi thường gặp

1. **MoviePy error**: Cài đặt ImageIO
```bash
pip install imageio[ffmpeg]
```

2. **API Key error**: Kiểm tra file .env
3. **Port conflict**: Thay đổi port trong mvp_server.py

## 📝 Roadmap

- [ ] Giao diện web hoàn chỉnh
- [ ] Hỗ trợ nhiều ngôn ngữ
- [ ] Template video tùy chỉnh
- [ ] Database persistence
- [ ] User authentication
- [ ] Batch processing

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit thay đổi
4. Push và tạo Pull Request

## 📄 License

MIT License - xem file LICENSE để biết chi tiết.

## 🙋‍♂️ Hỗ trợ

Nếu gặp vấn đề, vui lòng tạo issue trên GitHub.

## 🌟 Features

- **AI Content Analysis**: Extract key insights from articles and blogs
- **Script Generation**: Create viral-optimized scripts for TikTok format
- **Voice Synthesis**: Natural voiceover using ElevenLabs AI
- **Video Production**: Automated MP4 generation ready for upload
- **Multi-Language**: Support for Vietnamese and English
- **Real-time Processing**: Job queue with progress tracking

## 🚀 Live Demo

**Hosted Demo**: https://yourusername.github.io/your-repo-name/

### Local Testing:
```bash
cd docs
python -m http.server 3000
# Open http://localhost:3000
```

## 📋 Deployment

### 1. Railway Backend
```bash
railway deploy
```

### 2. GitHub Pages Frontend
1. Push `docs/` folder to GitHub repository
2. Go to Repository Settings → Pages
3. Source: Deploy from branch `main`
4. Folder: `/docs`
5. Your demo will be live at: `https://yourusername.github.io/repo-name/`

## 🛠️ Installation

### Requirements
```bash
pip install -r requirements.txt
```

### Environment Variables
```bash
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
DATABASE_URL=your_postgres_url
```

### Development
```bash
python main.py
# Server runs on http://localhost:8000
```

## 🔧 Configuration

### Voice Settings
- Professional, Casual, Energetic, Calm styles
- Duration: 60s, 90s, 2min, 3min options
- Multi-language support

### AI Services
- Content extraction and analysis
- Script optimization for virality
- Natural voice generation
- Smart video composition

## 📊 API Usage

### Generate Video
```javascript
POST /api/process
{
    "url": "https://example.com/article",
    "content_type": "url",
    "use_ai": true,
    "settings": {
        "duration": 60,
        "voice_style": "professional",
        "language": "en"
    }
}
```

### Check Status
```javascript
GET /api/job/{job_id}
```

## 🔍 Troubleshooting

### CORS Issues
- Use hosted demo instead of local files
- Ensure Railway deployment is updated
- Check browser console for detailed errors

### API Connection
- Verify Railway service is running
- Check environment variables
- Test with `/health` endpoint first

## 📈 Monitoring

- Real-time job progress tracking
- Server health checks
- AI service status monitoring
- Error logging and debugging

---
Created with ❤️ for content creators who want to automate TikTok video production. 