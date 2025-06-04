# 🚀 **DEPLOY PUBLIC DEMO TO RAILWAY**

## **Quick Deploy (5 phút)**

### **Bước 1: Tạo Repository**
```bash
# Upload code lên GitHub (private repo cũng được)
git init
git add .
git commit -m "TikTok Video Generator MVP"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### **Bước 2: Deploy trên Railway**
1. Truy cập: https://railway.app/
2. Sign up với GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Chọn repository vừa tạo
5. Railway sẽ auto-detect Python và deploy

### **Bước 3: Configure Environment**
```bash
# Thêm environment variables trong Railway dashboard:
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
PORT=8005
```

### **Bước 4: Setup Startup Command**
Trong Railway settings:
```bash
cd backend && python mvp_server.py
```

---

## **Expected Demo URL:**
```
🌐 Public Demo: https://your-app-name.railway.app
📊 Health Check: https://your-app-name.railway.app/health
📖 API Docs: https://your-app-name.railway.app/
``` 