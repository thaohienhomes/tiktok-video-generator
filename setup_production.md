# 🚀 **SETUP PRODUCTION - COMPLETE GUIDE**

## **Bước 1: Cài đặt API Keys**

### **OpenAI API Key**
1. Truy cập: https://platform.openai.com/api-keys
2. Tạo API key mới
3. Copy key và thêm vào environment:

```bash
# Windows
set OPENAI_API_KEY=sk-your-openai-key-here

# Linux/Mac
export OPENAI_API_KEY=sk-your-openai-key-here
```

### **ElevenLabs API Key**
1. Truy cập: https://elevenlabs.io/api
2. Tạo API key mới
3. Thêm vào environment:

```bash
# Windows
set ELEVENLABS_API_KEY=your-elevenlabs-key-here

# Linux/Mac
export ELEVENLABS_API_KEY=your-elevenlabs-key-here
```

### **Permanent Environment Setup**

Tạo file `.env` trong thư mục root:

```env
# API Keys
OPENAI_API_KEY=sk-your-openai-key-here
ELEVENLABS_API_KEY=your-elevenlabs-key-here

# Server Configuration
SERVER_PORT=8005
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Video Settings
MAX_VIDEO_DURATION=180
DEFAULT_VOICE_STYLE=professional
DEFAULT_LANGUAGE=vi
```

---

## **Bước 2: Cài đặt Production Dependencies**

### **Backend Dependencies**
```bash
cd backend
pip install python-dotenv
pip install moviepy
pip install imageio[ffmpeg]
```

### **Frontend Dependencies (Optional)**
```bash
cd frontend
npm install
npm run build
```

---

## **Bước 3: Production Server Setup**

### **3.1 Update MVP Server để đọc .env**

Thêm vào `backend/mvp_server.py`:

```python
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
```

### **3.2 Tạo Production Startup Script**

Tạo file `start_production.py`:

```python
#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def start_production():
    print("🚀 Starting TikTok Video Generator - PRODUCTION MODE")
    
    # Check environment variables
    required_vars = ['OPENAI_API_KEY', 'ELEVENLABS_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Missing environment variables: {', '.join(missing_vars)}")
        print("📖 Please check setup_production.md for instructions")
        return False
    
    # Start backend server
    os.chdir('backend')
    subprocess.run([sys.executable, 'mvp_server.py'])

if __name__ == "__main__":
    start_production()
```

---

## **Bước 4: Testing Production Setup**

### **4.1 Test API Keys**
```bash
python test_api_keys.py
```

### **4.2 Test Complete Workflow**
```bash
python test_enhanced_workflow.py
```

### **4.3 Test Video Generation**
```bash
python test_video_generation.py
```

---

## **Bước 5: Deployment Options**

### **Option 1: Local Server**
```bash
python start_production.py
```

### **Option 2: Docker Deployment**
```dockerfile
FROM python:3.11

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .
COPY .env .

EXPOSE 8005

CMD ["python", "mvp_server.py"]
```

### **Option 3: Cloud Deployment**

#### **Heroku**
```bash
# Tạo Procfile
echo "web: python backend/mvp_server.py" > Procfile

# Deploy
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your-key
heroku config:set ELEVENLABS_API_KEY=your-key
git push heroku main
```

#### **Railway**
```bash
# Tạo railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "cd backend && python mvp_server.py"
  }
}
```

---

## **Bước 6: Performance Optimization**

### **6.1 Redis Cache (Optional)**
```bash
pip install redis
docker run -d -p 6379:6379 redis:alpine
```

### **6.2 Database Setup (Optional)**
```bash
pip install sqlalchemy alembic
```

### **6.3 File Storage**
- **Local**: `outputs/` folder
- **Cloud**: AWS S3, Google Cloud Storage
- **CDN**: CloudFlare, AWS CloudFront

---

## **Bước 7: Monitoring & Logs**

### **7.1 Logging Setup**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### **7.2 Health Monitoring**
- **Endpoint**: `GET /health`
- **Metrics**: API response times, job completion rates
- **Alerts**: Email/Slack notifications for failures

---

## **Bước 8: Security & Best Practices**

### **8.1 API Rate Limiting**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/process-url")
@limiter.limit("10/minute")
async def process_url_endpoint(...):
    ...
```

### **8.2 Input Validation**
```python
from pydantic import BaseModel, HttpUrl

class ProcessUrlRequest(BaseModel):
    url: HttpUrl
    settings: dict
```

### **8.3 CORS Configuration**
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## **🎯 PRODUCTION CHECKLIST**

- [ ] API keys được set up
- [ ] Environment variables configured
- [ ] All dependencies installed
- [ ] Enhanced workflow tested
- [ ] Video generation working
- [ ] Content extraction working
- [ ] Frontend integrated (optional)
- [ ] Error handling implemented
- [ ] Logging configured
- [ ] Security measures in place
- [ ] Performance optimized
- [ ] Deployment ready

---

## **🆘 Troubleshooting**

### **Common Issues**

1. **ElevenLabs Import Error**
   ```bash
   pip uninstall elevenlabs
   pip install elevenlabs==0.2.26
   ```

2. **MoviePy Installation Issues**
   ```bash
   pip install moviepy==1.0.3
   pip install imageio[ffmpeg]
   ```

3. **Font Issues on Linux**
   ```bash
   sudo apt-get install fonts-liberation
   ```

4. **FFMPEG Not Found**
   ```bash
   # Windows: Download from https://ffmpeg.org/
   # Linux: sudo apt-get install ffmpeg
   # Mac: brew install ffmpeg
   ```

### **Support**

- **Documentation**: README.md
- **Issues**: Create GitHub issue
- **Testing**: Run all test scripts
- **Logs**: Check `app.log` for errors

---

**🎉 Ready for Production!**

Your TikTok Video Generator is now ready for production use with full AI capabilities! 