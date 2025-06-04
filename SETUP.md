# 🚀 EBook to Video AI Generator - Setup MVP

## 📋 Yêu Cầu Hệ Thống

### Backend (Python)
- Python 3.8+
- pip hoặc conda
- FFmpeg (cho video processing)

### Frontend (Node.js)
- Node.js 16+
- npm hoặc yarn

### API Keys Cần Thiết
- **OpenAI API Key** - Để phân tích nội dung và tạo script
- **ElevenLabs API Key** - Để tạo giọng đọc

## ⚡ Setup Nhanh (1 phút)

### 1. Clone hoặc tải project về

### 2. Tạo file environment variables
Tạo file `backend/.env`:
```env
OPENAI_API_KEY=sk-your-openai-key-here
ELEVENLABS_API_KEY=your-elevenlabs-key-here
```

### 3. Chạy script tự động
```bash
python start_mvp.py
```

Script sẽ tự động:
- ✅ Kiểm tra Python version
- ✅ Cài đặt backend dependencies  
- ✅ Cài đặt frontend dependencies
- ✅ Khởi động backend server (port 8000)
- ✅ Khởi động frontend server (port 3000)

### 4. Truy cập ứng dụng
- **Web App**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Backend API**: http://localhost:8000

## 🔧 Setup Thủ Công

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend  
```bash
cd frontend
npm install
npm run dev
```

## 🎯 Cách Sử Dụng MVP

### 1. Upload File hoặc URL
- **File**: Drag & drop PDF/TXT file (tối đa 50MB)
- **URL**: Nhập link bài viết hoặc ebook online

### 2. Cấu Hình Video
- **Thời lượng**: 1-10 phút
- **Giọng đọc**: Chuyên nghiệp, thân thiện, uy quyền, truyền cảm hứng, giáo dục

### 3. Xử Lý AI
- AI phân tích nội dung (30 giây)
- Tạo script tối ưu (1 phút) 
- Tạo giọng đọc với ElevenLabs (1 phút)
- Tạo video với hình ảnh minh họa (2 phút)
- Xuất caption/hashtag cho TikTok (30 giây)

### 4. Kết Quả
- ⬇️ Download video MP4 (vertical 9:16)
- 📝 Script đã được tối ưu
- 📱 Caption + hashtags sẵn sàng cho TikTok
- 🎨 Thumbnail tự động

## 🛠️ Cài Đặt Dependencies Thủ Công

### FFmpeg (Required cho video processing)

**Windows:**
```bash
# Sử dụng chocolatey
choco install ffmpeg

# Hoặc download từ https://ffmpeg.org/download.html
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

### Python Dependencies (Backend)
```bash
pip install fastapi uvicorn python-multipart
pip install PyPDF2 pdfplumber requests beautifulsoup4
pip install openai elevenlabs moviepy Pillow
pip install python-dotenv aiofiles httpx validators
pip install celery redis sqlalchemy alembic psycopg2-binary
pip install pydantic pydantic-settings
```

### Node.js Dependencies (Frontend)
```bash
npm install next react react-dom
npm install react-hook-form react-dropzone
npm install @radix-ui/react-dialog @radix-ui/react-select
npm install @radix-ui/react-progress @radix-ui/react-button
npm install @radix-ui/react-toast
npm install class-variance-authority clsx tailwind-merge
npm install axios lucide-react
npm install -D typescript @types/node @types/react @types/react-dom
npm install -D autoprefixer postcss tailwindcss eslint eslint-config-next
```

## 🔍 Troubleshooting

### Backend Issues
```bash
# Check if backend is running
curl http://localhost:8000/

# Check logs
cd backend
python main.py
```

### Frontend Issues
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Video Processing Issues
```bash
# Test FFmpeg installation
ffmpeg -version

# Test MoviePy
python -c "import moviepy; print('MoviePy OK')"
```

### API Key Issues
- Kiểm tra file `backend/.env` có đúng format
- Verify OpenAI key: https://platform.openai.com/api-keys
- Verify ElevenLabs key: https://elevenlabs.io/docs/api-reference/authentication

## 📊 Monitoring & Logs

### Backend Logs
```bash
cd backend
tail -f uvicorn.log
```

### Processing Status
- Check API: `GET /api/status/{job_id}`
- Real-time progress trong web interface

## 🚀 Production Deployment

### Backend (Docker)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (Vercel/Netlify)
```bash
npm run build
npm run start
```

## 💡 Tips & Best Practices

### Để Có Kết Quả Tốt Nhất:
1. **File Input**: PDF có text rõ ràng, không phải scan
2. **URL Input**: Bài viết có cấu trúc tốt, ít ads
3. **Nội Dung**: Chọn đoạn hay, có insight
4. **Thời Lượng**: 1-3 phút tối ưu cho social media
5. **Giọng Đọc**: Match với thể loại content

### Performance:
- Video 3 phút: ~2-5 phút processing
- Concurrent jobs: Tối đa 3-5 jobs cùng lúc
- File size: Khuyến nghị < 10MB cho tốc độ tối ưu

## 📞 Support

Nếu gặp vấn đề:
1. Check file `.env` có đúng API keys
2. Kiểm tra FFmpeg đã cài đặt
3. Verify Python 3.8+ và Node.js 16+
4. Check logs trong terminal

Happy video creating! 🎬✨ 