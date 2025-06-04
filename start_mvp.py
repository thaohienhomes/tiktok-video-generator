#!/usr/bin/env python3
"""
Script để khởi động EBook to Video AI Generator MVP
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_step(message):
    """Print step với formatting đẹp"""
    print(f"\n🚀 {message}")
    print("=" * 50)

def check_python_version():
    """Kiểm tra Python version"""
    if sys.version_info < (3, 8):
        print("❌ Cần Python 3.8 trở lên")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} OK")

def check_env_file():
    """Kiểm tra file .env"""
    env_path = Path("backend/.env")
    if not env_path.exists():
        print("❌ Không tìm thấy file backend/.env")
        print("📝 Tạo file backend/.env với nội dung:")
        print("""
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
""")
        return False
    print("✅ File .env tồn tại")
    return True

def install_backend_deps():
    """Cài đặt backend dependencies"""
    print_step("Cài đặt Backend Dependencies")
    
    # Change to backend directory
    os.chdir("backend")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ Backend dependencies đã được cài đặt")
    except subprocess.CalledProcessError:
        print("❌ Lỗi khi cài đặt backend dependencies")
        return False
    finally:
        os.chdir("..")
    
    return True

def install_frontend_deps():
    """Cài đặt frontend dependencies"""
    print_step("Cài đặt Frontend Dependencies")
    
    # Change to frontend directory
    os.chdir("frontend")
    
    try:
        subprocess.run(["npm", "install"], check=True)
        print("✅ Frontend dependencies đã được cài đặt")
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["yarn", "install"], check=True)
            print("✅ Frontend dependencies đã được cài đặt (với Yarn)")
        except subprocess.CalledProcessError:
            print("❌ Lỗi khi cài đặt frontend dependencies")
            print("💡 Hãy chắc chắn Node.js và npm/yarn đã được cài đặt")
            return False
    finally:
        os.chdir("..")
    
    return True

def start_backend():
    """Khởi động backend server"""
    print_step("Khởi động Backend Server")
    
    os.chdir("backend")
    
    # Start backend in background
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ])
        print("✅ Backend server đang chạy tại http://localhost:8000")
        time.sleep(3)  # Wait for server to start
        return process
    except Exception as e:
        print(f"❌ Lỗi khi khởi động backend: {e}")
        return None
    finally:
        os.chdir("..")

def start_frontend():
    """Khởi động frontend development server"""
    print_step("Khởi động Frontend Server")
    
    os.chdir("frontend")
    
    try:
        process = subprocess.Popen(["npm", "run", "dev"])
        print("✅ Frontend server đang chạy tại http://localhost:3000")
        return process
    except Exception as e:
        try:
            process = subprocess.Popen(["yarn", "dev"])
            print("✅ Frontend server đang chạy tại http://localhost:3000")
            return process
        except Exception as e:
            print(f"❌ Lỗi khi khởi động frontend: {e}")
            return None
    finally:
        os.chdir("..")

def main():
    """Main function"""
    print("🎬 EBook to Video AI Generator - MVP Startup")
    print("=" * 60)
    
    # Check requirements
    check_python_version()
    
    if not check_env_file():
        print("\n⚠️  Vui lòng tạo file .env trước khi tiếp tục")
        return
    
    # Install dependencies
    if not install_backend_deps():
        return
    
    if not install_frontend_deps():
        return
    
    # Start servers
    backend_process = start_backend()
    if not backend_process:
        return
    
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return
    
    print("\n" + "=" * 60)
    print("🎉 MVP ĐÃ KHỞI ĐỘNG THÀNH CÔNG!")
    print("=" * 60)
    print("🌐 Frontend: http://localhost:3000")
    print("🔧 Backend API: http://localhost:8000")
    print("📖 API Docs: http://localhost:8000/docs")
    print("\n💡 Để dừng servers, nhấn Ctrl+C")
    print("=" * 60)
    
    try:
        # Wait for user interrupt
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Đang dừng servers...")
        frontend_process.terminate()
        backend_process.terminate()
        print("✅ Servers đã được dừng")

if __name__ == "__main__":
    main() 