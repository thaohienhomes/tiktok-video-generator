#!/usr/bin/env python3
"""
🚀 Script tự động deploy dự án TikTok Video Generator lên GitHub
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Chạy command và hiển thị kết quả"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} thành công!")
            if result.stdout.strip():
                print(f"📝 Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} thất bại!")
            print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Lỗi khi {description}: {e}")
        return False
    return True

def check_git_installed():
    """Kiểm tra git đã được cài đặt chưa"""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git chưa được cài đặt. Vui lòng cài git trước!")
        return False

def main():
    print("🎬 TikTok Video Generator - GitHub Deployment Script")
    print("=" * 60)
    
    # Kiểm tra git
    if not check_git_installed():
        return
    
    # Nhập thông tin GitHub
    print("\n📝 Nhập thông tin GitHub:")
    github_username = input("GitHub Username: ").strip()
    if not github_username:
        print("❌ Vui lòng nhập GitHub username!")
        return
    
    repository_name = input("Repository name (mặc định: tiktok-video-generator): ").strip()
    if not repository_name:
        repository_name = "tiktok-video-generator"
    
    # Xác nhận
    print(f"\n🔍 Thông tin deploy:")
    print(f"GitHub: https://github.com/{github_username}/{repository_name}")
    confirm = input("Tiếp tục? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Hủy deploy.")
        return
    
    print("\n🚀 Bắt đầu deploy...")
    
    # Các bước deploy
    steps = [
        ("git init", "Khởi tạo Git repository"),
        ("git add .", "Thêm tất cả file vào Git"),
        ('git commit -m "🚀 Initial commit: TikTok Video Generator MVP"', "Tạo commit đầu tiên"),
        ("git branch -M main", "Đổi tên branch thành main"),
        (f"git remote add origin https://github.com/{github_username}/{repository_name}.git", "Thêm remote origin"),
        ("git push -u origin main", "Push code lên GitHub")
    ]
    
    for command, description in steps:
        if not run_command(command, description):
            print(f"\n❌ Deploy thất bại tại bước: {description}")
            print("💡 Hướng dẫn sửa lỗi:")
            print("1. Kiểm tra kết nối internet")
            print("2. Đảm bảo repository đã được tạo trên GitHub")
            print("3. Kiểm tra quyền truy cập GitHub")
            return
    
    print("\n🎉 Deploy thành công!")
    print(f"🔗 Repository: https://github.com/{github_username}/{repository_name}")
    print("\n📋 Các bước tiếp theo:")
    print("1. Truy cập repository trên GitHub")
    print("2. Thêm API keys vào GitHub Secrets (nếu deploy production)")
    print("3. Cấu hình GitHub Actions (tùy chọn)")
    print("4. Thêm collaborators (nếu cần)")

if __name__ == "__main__":
    main() 