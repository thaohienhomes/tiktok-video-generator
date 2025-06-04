from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any, List
from enum import Enum

class VoiceStyle(str, Enum):
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    AUTHORITATIVE = "authoritative"
    INSPIRING = "inspiring"
    EDUCATIONAL = "educational"

class ContentCategory(str, Enum):
    BUSINESS = "business"
    SELF_DEVELOPMENT = "self_development"
    SCIENCE = "science"
    HISTORY = "history"
    TECHNOLOGY = "technology"
    HEALTH = "health"
    OTHER = "other"

class ProcessingStatus(str, Enum):
    INITIALIZED = "initialized"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"

class VideoRequest(BaseModel):
    url: Optional[HttpUrl] = None
    duration: int = 180  # seconds
    voice_style: VoiceStyle = VoiceStyle.PROFESSIONAL
    
    class Config:
        use_enum_values = True

class ContentAnalysis(BaseModel):
    category: ContentCategory
    key_points: List[str]
    script: str
    estimated_duration: int
    tone: str

class MarketingContent(BaseModel):
    caption: str
    hashtags: List[str]
    description: str
    hook: str

class VideoResult(BaseModel):
    video_path: str
    audio_path: str
    script: str
    category: ContentCategory
    marketing: MarketingContent
    duration: int

class ProcessingJob(BaseModel):
    status: ProcessingStatus
    progress: int  # 0-100
    message: str
    result: Optional[VideoResult] = None
    error: Optional[str] = None

class VideoResponse(BaseModel):
    job_id: str
    message: str 