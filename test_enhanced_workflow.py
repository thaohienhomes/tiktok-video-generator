#!/usr/bin/env python3
"""
Test Enhanced TikTok Video Generator Workflow
Tests real content extraction, AI processing, and video generation
"""

import requests
import json
import time

def test_enhanced_workflow():
    """Test complete enhanced workflow"""
    
    base_url = "http://127.0.0.1:8005"
    
    print("🧪 TESTING ENHANCED WORKFLOW")
    print("=" * 50)
    
    # 1. Test health check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Server healthy: {health_data}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return
    
    # 2. Test URL processing with real content extraction
    print("\n2️⃣ Testing URL Processing with Real Content Extraction...")
    
    test_url = "https://blog.openai.com/chatgpt"  # Sample URL
    
    payload = {
        "url": test_url,
        "settings": {
            "duration": 60,
            "voice_style": "professional",
            "language": "vi"
        }
    }
    
    try:
        # Use correct endpoint for URL processing
        payload_with_type = {
            "content_type": "url",
            "url": test_url,
            "settings": payload["settings"]
        }
        response = requests.post(f"{base_url}/api/process", json=payload_with_type)
        if response.status_code == 200:
            result = response.json()
            job_id = result.get("job_id")
            print(f"✅ URL processing started: Job ID {job_id}")
            
            # Monitor job progress
            print("\n📊 Monitoring Job Progress...")
            for i in range(20):  # Max 20 checks (2 minutes)
                time.sleep(6)
                
                status_response = requests.get(f"{base_url}/api/job/{job_id}")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    progress = status_data.get("progress", 0)
                    current_step = status_data.get("current_step", "")
                    status = status_data.get("status", "")
                    
                    print(f"   Progress: {progress}% - {current_step} ({status})")
                    
                    if status == "completed":
                        print("\n🎉 JOB COMPLETED!")
                        result_data = status_data.get("result", {})
                        
                        print(f"📹 Video: {result_data.get('video_file', 'N/A')}")
                        print(f"🎵 Voice: {result_data.get('voice_file', 'N/A')}")
                        print(f"⏱️ Duration: {result_data.get('duration', 'N/A')}")
                        print(f"📱 Resolution: {result_data.get('resolution', 'N/A')}")
                        print(f"🤖 AI Powered: {result_data.get('ai_powered', False)}")
                        print(f"📄 Content Extraction: {result_data.get('content_extraction', False)}")
                        print(f"🎬 Video Generation: {result_data.get('video_generation', False)}")
                        
                        # Show script preview
                        script_data = result_data.get('script_data', {})
                        if script_data:
                            print(f"\n📝 Generated Script:")
                            print(f"   Hook: {script_data.get('hook', 'N/A')}")
                            print(f"   Main Points: {len(script_data.get('main_points', []))}")
                            print(f"   Category: {script_data.get('category', 'N/A')}")
                        
                        # Show marketing content
                        marketing = result_data.get('marketing', {})
                        if marketing:
                            print(f"\n📱 Marketing Content:")
                            print(f"   Caption: {marketing.get('caption', 'N/A')}")
                            print(f"   Hashtags: {len(marketing.get('hashtags', []))} tags")
                        
                        # Show content metadata
                        content_meta = result_data.get('content_metadata', {})
                        if content_meta:
                            print(f"\n📖 Content Source:")
                            print(f"   Title: {content_meta.get('title', 'N/A')}")
                            print(f"   Length: {content_meta.get('length', 0)} chars")
                            print(f"   Domain: {content_meta.get('domain', 'N/A')}")
                        
                        break
                    elif status == "failed":
                        print(f"❌ Job failed: {status_data.get('error', 'Unknown error')}")
                        break
                else:
                    print(f"❌ Status check failed: {status_response.status_code}")
                    break
            else:
                print("⏱️ Job timed out after 2 minutes")
                
        else:
            print(f"❌ URL processing failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ URL processing error: {e}")
    
    # 3. Test capabilities summary
    print("\n📊 ENHANCED CAPABILITIES SUMMARY")
    print("=" * 50)
    
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health_data = response.json()
            
            print(f"🚀 Server Status: {health_data.get('status', 'Unknown')}")
            print(f"⚡ AI Services: {'✅ Enabled' if health_data.get('ai_services', False) else '❌ Simulation'}")
            print(f"📄 Content Extraction: {'✅ Available' if health_data.get('content_extraction', False) else '❌ Not Available'}")
            print(f"🎬 Video Generation: {'✅ Available' if health_data.get('video_generation', False) else '❌ Not Available'}")
            print(f"🔊 Voice Generation: {'✅ Available' if health_data.get('voice_generation', False) else '❌ Simulation'}")
            
    except Exception as e:
        print(f"❌ Cannot get capabilities: {e}")
    
    print("\n✅ Enhanced Workflow Test Completed!")

if __name__ == "__main__":
    test_enhanced_workflow()