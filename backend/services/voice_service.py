import os
import aiofiles
from elevenlabs import Voice, VoiceSettings, generate, set_api_key
from config import settings
from typing import Dict

class VoiceService:
    """Service để tạo giọng đọc bằng ElevenLabs"""
    
    def __init__(self):
        if not settings.elevenlabs_api_key:
            raise ValueError("ElevenLabs API key không được tìm thấy")
        
        set_api_key(settings.elevenlabs_api_key)
        
        # Voice mapping cho các style khác nhau
        self.voice_mapping = {
            "professional": {
                "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel - Professional female
                "stability": 0.75,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            },
            "friendly": {
                "voice_id": "AZnzlk1XvdvUeBnXmlld",  # Domi - Friendly female
                "stability": 0.65,
                "similarity_boost": 0.80,
                "style": 0.2,
                "use_speaker_boost": True
            },
            "authoritative": {
                "voice_id": "2EiwWnXFnvU5JabPnv8n",  # Clyde - Authoritative male
                "stability": 0.85,
                "similarity_boost": 0.70,
                "style": 0.1,
                "use_speaker_boost": True
            },
            "inspiring": {
                "voice_id": "29vD33N1CtxCmqQRPOHJ",  # Drew - Inspiring male
                "stability": 0.70,
                "similarity_boost": 0.75,
                "style": 0.3,
                "use_speaker_boost": True
            },
            "educational": {
                "voice_id": "pNInz6obpgDQGcFmaJgB",  # Adam - Educational male
                "stability": 0.80,
                "similarity_boost": 0.75,
                "style": 0.1,
                "use_speaker_boost": True
            }
        }
    
    async def generate_speech(self, text: str, voice_style: str, job_id: str) -> str:
        """Tạo file audio từ text"""
        
        # Get voice configuration
        voice_config = self.voice_mapping.get(voice_style, self.voice_mapping["professional"])
        
        try:
            # Create voice settings
            voice_settings = VoiceSettings(
                stability=voice_config["stability"],
                similarity_boost=voice_config["similarity_boost"],
                style=voice_config.get("style", 0.0),
                use_speaker_boost=voice_config.get("use_speaker_boost", True)
            )
            
            # Generate audio
            audio = generate(
                text=text,
                voice=Voice(
                    voice_id=voice_config["voice_id"],
                    settings=voice_settings
                ),
                model="eleven_multilingual_v2"  # Supports Vietnamese better
            )
            
            # Save audio file
            audio_filename = f"audio_{job_id}.mp3"
            audio_path = os.path.join(settings.output_folder, audio_filename)
            
            # Write audio file
            async with aiofiles.open(audio_path, 'wb') as f:
                await f.write(audio)
            
            return audio_path
            
        except Exception as e:
            raise Exception(f"Lỗi khi tạo giọng đọc: {str(e)}")
    
    async def get_available_voices(self) -> Dict[str, str]:
        """Lấy danh sách voices có sẵn"""
        return {
            "professional": "Rachel - Giọng nữ chuyên nghiệp",
            "friendly": "Domi - Giọng nữ thân thiện", 
            "authoritative": "Clyde - Giọng nam uy quyền",
            "inspiring": "Drew - Giọng nam truyền cảm hứng",
            "educational": "Adam - Giọng nam giáo dục"
        }
    
    def get_recommended_voice(self, category: str, tone: str) -> str:
        """Gợi ý voice phù hợp với thể loại nội dung"""
        
        # Mapping category và tone với voice style
        recommendation_map = {
            "business": {
                "professional": "professional",
                "authoritative": "authoritative",
                "friendly": "professional"
            },
            "self_development": {
                "inspiring": "inspiring",
                "motivational": "inspiring",
                "friendly": "friendly"
            },
            "science": {
                "educational": "educational",
                "professional": "professional",
                "clear": "educational"
            },
            "history": {
                "educational": "educational",
                "authoritative": "authoritative",
                "storytelling": "friendly"
            },
            "technology": {
                "professional": "professional",
                "educational": "educational",
                "modern": "professional"
            },
            "health": {
                "caring": "friendly",
                "professional": "professional",
                "educational": "educational"
            }
        }
        
        category_map = recommendation_map.get(category, {})
        recommended = category_map.get(tone, "professional")
        
        return recommended
    
    def estimate_audio_duration(self, text: str) -> float:
        """Ước tính thời lượng audio từ text"""
        # Average speaking rate: 150-160 words per minute
        # Vietnamese might be slightly slower, so use 140 WPM
        word_count = len(text.split())
        duration_minutes = word_count / 140
        duration_seconds = duration_minutes * 60
        
        # Add some buffer for pauses and pronunciation
        duration_seconds *= 1.1
        
        return round(duration_seconds, 1)
    
    async def validate_text_length(self, text: str) -> bool:
        """Kiểm tra độ dài text có phù hợp không"""
        # ElevenLabs có giới hạn ký tự cho mỗi request
        max_characters = 5000  # Conservative limit
        
        if len(text) > max_characters:
            return False
        
        return True
    
    async def split_long_text(self, text: str, max_chars: int = 4000) -> list:
        """Chia text dài thành các đoạn nhỏ"""
        
        if len(text) <= max_chars:
            return [text]
        
        chunks = []
        sentences = text.split('. ')
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) + 2 <= max_chars:
                current_chunk += sentence + ". "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks 