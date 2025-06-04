#!/usr/bin/env python3
"""
Real AI Services for TikTok Video Generator
Integrates with OpenAI GPT-4 and ElevenLabs for real processing
"""

import os
import openai
import requests
import elevenlabs
from elevenlabs import Voice, VoiceSettings
import time
import json
from typing import Dict, Any, Optional

# Environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')

# Initialize clients
openai.api_key = OPENAI_API_KEY

# Set ElevenLabs API key
if ELEVENLABS_API_KEY:
    elevenlabs.set_api_key(ELEVENLABS_API_KEY)
    ELEVENLABS_AVAILABLE = True
else:
    ELEVENLABS_AVAILABLE = False

class AIContentProcessor:
    """Process ebook content with OpenAI GPT-4"""
    
    def __init__(self):
        self.client = openai
        
    async def analyze_content(self, content: str, duration: int = 180) -> Dict[str, Any]:
        """Analyze content and create TikTok script"""
        
        if not OPENAI_API_KEY:
            # Fallback to simulation if no API key
            return self._simulate_analysis(content, duration)
            
        try:
            # Calculate target word count (150-200 words per minute)
            target_words = int((duration / 60) * 175)
            
            prompt = f"""
Phân tích nội dung ebook sau và tạo script cho video TikTok {duration} giây:

NỘI DUNG:
{content[:2000]}...

YÊU CẦU:
1. Tạo script khoảng {target_words} từ ({duration} giây)
2. Hook hấp dẫn trong 3 giây đầu
3. Chia thành 3-5 điểm chính
4. Ngôn ngữ đơn giản, dễ hiểu
5. Call-to-action cuối video
6. Phù hợp xu hướng TikTok

FORMAT JSON:
{{
    "hook": "câu mở đầu hấp dẫn",
    "main_points": ["điểm 1", "điểm 2", "điểm 3"],
    "script": "script đầy đủ để đọc",
    "category": "danh mục nội dung",
    "keywords": ["từ khóa 1", "từ khóa 2"],
    "estimated_duration": {duration}
}}
"""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Bạn là chuyên gia tạo nội dung TikTok viral"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            content_analysis = json.loads(response.choices[0].message.content)
            return content_analysis
            
        except Exception as e:
            print(f"❌ OpenAI API Error: {e}")
            return self._simulate_analysis(content, duration)
    
    def _simulate_analysis(self, content: str, duration: int) -> Dict[str, Any]:
        """Simulation fallback"""
        return {
            "hook": "📚 Bạn có biết bí mật này từ cuốn sách này không?",
            "main_points": [
                "Điểm quan trọng đầu tiên từ nội dung",
                "Insight thú vị thứ hai", 
                "Kết luận và bài học"
            ],
            "script": f"📚 Bạn có biết bí mật này từ cuốn sách này không? Hôm nay mình sẽ chia sẻ {duration//60} phút kiến thức vàng từ cuốn sách này. Đầu tiên là điểm quan trọng từ nội dung. Tiếp theo là insight thú vị. Cuối cùng là kết luận và bài học. Nhớ follow để không bỏ lỡ video tiếp theo nhé! 🔥",
            "category": "education",
            "keywords": ["sách", "kiến thức", "học tập"],
            "estimated_duration": duration
        }

class VoiceGenerator:
    """Generate voice with ElevenLabs"""
    
    def __init__(self):
        self.voices = {
            'professional': 'Rachel',  # English voice IDs
            'casual': 'Josh',
            'energetic': 'Antoni',
            'calm': 'Bella'
        }
    
    async def generate_speech(self, text: str, voice_style: str = 'professional') -> Optional[str]:
        """Generate speech from text"""
        
        if not ELEVENLABS_AVAILABLE:
            # Fallback to simulation
            return self._simulate_voice_generation(text, voice_style)
            
        try:
            # Get voice ID
            voice_name = self.voices.get(voice_style, 'Rachel')
            
            # Generate speech using new API
            audio = elevenlabs.generate(
                text=text,
                voice=voice_name,
                model="eleven_monolingual_v1"
            )
            
            # Save audio file
            audio_filename = f"audio_{int(time.time())}.mp3"
            audio_path = f"outputs/{audio_filename}"
            
            # Ensure outputs directory exists
            os.makedirs("outputs", exist_ok=True)
            
            with open(audio_path, "wb") as f:
                f.write(audio)
            
            return audio_path
            
        except Exception as e:
            print(f"❌ ElevenLabs API Error: {e}")
            return self._simulate_voice_generation(text, voice_style)
    
    def _simulate_voice_generation(self, text: str, voice_style: str) -> str:
        """Simulation fallback"""
        print(f"🎙️ Voice Generation Simulated:")
        print(f"   Style: {voice_style}")
        print(f"   Text length: {len(text)} chars")
        print(f"   Estimated duration: {len(text.split()) / 150 * 60:.1f} seconds")
        
        # Return simulated path
        return f"outputs/simulated_voice_{voice_style}_{int(time.time())}.mp3"

class MarketingGenerator:
    """Generate marketing content with AI"""
    
    def __init__(self):
        self.client = openai
    
    async def generate_marketing(self, script: str, category: str, keywords: list) -> Dict[str, Any]:
        """Generate TikTok marketing content"""
        
        if not OPENAI_API_KEY:
            return self._simulate_marketing(script, category, keywords)
            
        try:
            prompt = f"""
Tạo nội dung marketing cho video TikTok:

SCRIPT: {script[:500]}...
CATEGORY: {category}
KEYWORDS: {', '.join(keywords)}

YÊU CẦU:
1. Caption hấp dẫn (2-3 dòng)
2. 10-15 hashtags trending
3. Mô tả chi tiết cho SEO
4. Hook comment để tăng engagement

FORMAT JSON:
{{
    "caption": "caption ngắn gọn hấp dẫn",
    "hashtags": ["#hashtag1", "#hashtag2"],
    "description": "mô tả đầy đủ cho SEO",
    "hook": "câu hỏi để khuyến khích comment"
}}
"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Bạn là chuyên gia marketing TikTok"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            marketing_content = json.loads(response.choices[0].message.content)
            return marketing_content
            
        except Exception as e:
            print(f"❌ Marketing AI Error: {e}")
            return self._simulate_marketing(script, category, keywords)
    
    def _simulate_marketing(self, script: str, category: str, keywords: list) -> Dict[str, Any]:
        """Simulation fallback"""
        return {
            "caption": "📚✨ Kiến thức vàng từ sách hay! Bạn đã biết điều này chưa?",
            "hashtags": [
                "#sachhay", "#kienthuc", "#hoctap", "#viral", "#fyp",
                "#sachnoitru", "#docgia", "#kienthucbonphuong", "#trending", "#educational"
            ],
            "description": f"Video chia sẻ kiến thức từ sách hay trong lĩnh vực {category}. Nội dung được tóm tắt ngắn gọn, dễ hiểu cho mọi người. Đừng quên follow để xem thêm những video kiến thức bổ ích khác!",
            "hook": "Bạn nghĩ điều gì là quan trọng nhất trong video này? Comment để thảo luận nhé! 💭"
        }

# Initialize services
content_processor = AIContentProcessor()
voice_generator = VoiceGenerator()
marketing_generator = MarketingGenerator()

# Export for easy import
__all__ = ['content_processor', 'voice_generator', 'marketing_generator'] 