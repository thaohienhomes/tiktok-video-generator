#!/usr/bin/env python3
"""
Create Public Demo URL for TikTok Video Generator
Uses ngrok to expose local server to internet
"""

import subprocess
import os
import time
import requests
import json

def create_public_demo():
    """Create public demo URL"""
    
    print("🌐 CREATING PUBLIC DEMO URL")
    print("=" * 50)
    
    # Check if ngrok is installed
    try:
        result = subprocess.run(["ngrok", "version"], capture_output=True, text=True)
        print(f"✅ Ngrok found: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Ngrok not found!")
        print("📥 Install ngrok:")
        print("   1. Download: https://ngrok.com/download")
        print("   2. Extract to PATH")
        print("   3. Sign up: https://dashboard.ngrok.com/signup")
        print("   4. Get auth token: https://dashboard.ngrok.com/get-started/your-authtoken")
        print("   5. Run: ngrok config add-authtoken YOUR_TOKEN")
        return
    
    # Start ngrok tunnel
    print("\n🚀 Starting ngrok tunnel...")
    
    # Kill any existing ngrok processes
    try:
        subprocess.run(["pkill", "-f", "ngrok"], capture_output=True)
    except:
        pass
    
    # Start ngrok in background
    ngrok_process = subprocess.Popen(
        ["ngrok", "http", "8005"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for ngrok to start
    time.sleep(3)
    
    # Get public URL from ngrok API
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        tunnels = response.json()
        
        if tunnels["tunnels"]:
            public_url = tunnels["tunnels"][0]["public_url"]
            print(f"🎉 PUBLIC DEMO URL: {public_url}")
            
            # Test the public URL
            health_url = f"{public_url}/health"
            health_response = requests.get(health_url)
            
            if health_response.status_code == 200:
                capabilities = health_response.json()
                
                print("\n✅ DEMO IS LIVE!")
                print("=" * 50)
                print(f"🌐 Demo URL: {public_url}")
                print(f"📊 Health Check: {health_url}")
                print(f"📖 API Docs: {public_url}/")
                
                print(f"\n🤖 AI Capabilities:")
                print(f"   ⚡ AI Services: {'✅' if capabilities.get('ai_services') else '❌'}")
                print(f"   📄 Content Extraction: {'✅' if capabilities.get('content_extraction') else '❌'}")
                print(f"   🎬 Video Generation: {'✅' if capabilities.get('video_generation') else '❌'}")
                print(f"   🔊 Voice Generation: {'✅' if capabilities.get('voice_generation') else '❌'}")
                
                print(f"\n🎯 TEST COMMANDS:")
                print(f"curl {health_url}")
                print(f"""curl -X POST {public_url}/api/process \\
  -H "Content-Type: application/json" \\
  -d '{{"content_type": "url", "url": "https://example.com", "settings": {{"duration": 60}}}}'""")
                
                print(f"\n🌍 SHARE THIS DEMO:")
                print(f"   Frontend Demo: {public_url}")
                print(f"   API Explorer: {public_url}/")
                print(f"   Real-time Health: {health_url}")
                
                print(f"\n⚠️ Note: Demo will run until you press Ctrl+C")
                
                # Keep running
                try:
                    ngrok_process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping demo...")
                    ngrok_process.terminate()
            else:
                print(f"❌ Demo health check failed: {health_response.status_code}")
        else:
            print("❌ No ngrok tunnels found")
            
    except Exception as e:
        print(f"❌ Error getting ngrok URL: {e}")
        print("🔧 Make sure local server is running on port 8005")

def test_demo_workflow(demo_url):
    """Test complete demo workflow"""
    
    print(f"\n🧪 TESTING DEMO WORKFLOW")
    print("=" * 50)
    
    # Test URL processing
    test_payload = {
        "content_type": "url",
        "url": "https://www.wikipedia.org/wiki/Artificial_intelligence",
        "settings": {
            "duration": 60,
            "voice_style": "professional",
            "language": "vi"
        }
    }
    
    try:
        print("🚀 Starting demo job...")
        response = requests.post(f"{demo_url}/api/process", json=test_payload)
        
        if response.status_code == 200:
            result = response.json()
            job_id = result.get("job_id")
            print(f"✅ Demo job started: {job_id}")
            print(f"📊 Monitor at: {demo_url}/api/job/{job_id}")
            
            return True
        else:
            print(f"❌ Demo job failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Demo test error: {e}")
        return False

if __name__ == "__main__":
    create_public_demo() 