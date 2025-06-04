import os
import asyncio
from moviepy.editor import (
    VideoFileClip, AudioFileClip, ImageClip, TextClip, 
    CompositeVideoClip, concatenate_videoclips
)
from moviepy.config import check_for_package
from PIL import Image, ImageDraw, ImageFont
import textwrap
from typing import List, Dict, Any
from config import settings
import requests
import random

class VideoService:
    """Service để tạo video từ audio và nội dung"""
    
    def __init__(self):
        self.video_width = settings.video_resolution[0]
        self.video_height = settings.video_resolution[1]
        
        # Background colors cho các thể loại khác nhau
        self.category_themes = {
            "business": {
                "bg_color": "#1a365d",
                "text_color": "#ffffff",
                "accent_color": "#3182ce"
            },
            "self_development": {
                "bg_color": "#2d3748", 
                "text_color": "#ffffff",
                "accent_color": "#38a169"
            },
            "science": {
                "bg_color": "#1a202c",
                "text_color": "#ffffff", 
                "accent_color": "#805ad5"
            },
            "history": {
                "bg_color": "#744210",
                "text_color": "#ffffff",
                "accent_color": "#d69e2e"
            },
            "technology": {
                "bg_color": "#1a1a1a",
                "text_color": "#ffffff",
                "accent_color": "#00d9ff"
            },
            "health": {
                "bg_color": "#22543d",
                "text_color": "#ffffff", 
                "accent_color": "#48bb78"
            },
            "other": {
                "bg_color": "#2d3748",
                "text_color": "#ffffff",
                "accent_color": "#4299e1"
            }
        }
    
    async def create_video(self, script: str, audio_path: str, category: str, job_id: str) -> str:
        """Tạo video từ script và audio"""
        
        try:
            # Get audio duration
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
            
            # Create video clips
            video_clips = await self._create_video_scenes(script, category, duration)
            
            # Combine all clips
            final_video = concatenate_videoclips(video_clips, method="compose")
            
            # Add audio
            final_video = final_video.set_audio(audio_clip)
            
            # Output path
            video_filename = f"video_{job_id}.mp4"
            video_path = os.path.join(settings.output_folder, video_filename)
            
            # Export video
            final_video.write_videofile(
                video_path,
                fps=30,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                preset='medium',
                ffmpeg_params=['-crf', '23']
            )
            
            # Clean up
            audio_clip.close()
            final_video.close()
            
            return video_path
            
        except Exception as e:
            raise Exception(f"Lỗi khi tạo video: {str(e)}")
    
    async def _create_video_scenes(self, script: str, category: str, duration: float) -> List[VideoFileClip]:
        """Tạo các scene cho video"""
        
        # Split script into segments
        segments = self._split_script_into_segments(script, duration)
        
        theme = self.category_themes.get(category, self.category_themes["other"])
        scenes = []
        
        for i, segment in enumerate(segments):
            scene_duration = segment["duration"]
            scene_text = segment["text"]
            
            # Create background
            bg_clip = self._create_background_clip(theme, scene_duration)
            
            # Create text overlay
            text_clip = self._create_text_clip(
                scene_text, 
                theme, 
                scene_duration,
                position="center"
            )
            
            # Create title/subtitle if first scene
            if i == 0:
                title_clip = self._create_title_clip(
                    "💡 Kiến Thức Hay",
                    theme,
                    scene_duration
                )
                scene = CompositeVideoClip([bg_clip, title_clip, text_clip])
            else:
                scene = CompositeVideoClip([bg_clip, text_clip])
            
            scenes.append(scene)
        
        return scenes
    
    def _split_script_into_segments(self, script: str, total_duration: float) -> List[Dict[str, Any]]:
        """Chia script thành các segments với timing"""
        
        sentences = script.split('. ')
        segments = []
        
        # Calculate duration per sentence (rough estimate)
        total_sentences = len(sentences)
        avg_duration_per_sentence = total_duration / total_sentences
        
        current_text = ""
        current_duration = 0
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Group 2-3 sentences per segment for better readability
            if len(current_text.split('. ')) < 3 and i < total_sentences - 1:
                current_text += sentence + ". "
                current_duration += avg_duration_per_sentence
            else:
                current_text += sentence + "."
                current_duration += avg_duration_per_sentence
                
                segments.append({
                    "text": current_text.strip(),
                    "duration": current_duration
                })
                
                current_text = ""
                current_duration = 0
        
        # Add any remaining text
        if current_text.strip():
            segments.append({
                "text": current_text.strip(),
                "duration": avg_duration_per_sentence
            })
        
        return segments
    
    def _create_background_clip(self, theme: Dict[str, str], duration: float) -> ImageClip:
        """Tạo background clip với gradient"""
        
        # Create gradient background
        img = Image.new('RGB', (self.video_width, self.video_height), theme["bg_color"])
        draw = ImageDraw.Draw(img)
        
        # Add subtle gradient effect
        for y in range(self.video_height):
            alpha = int(255 * (1 - y / self.video_height * 0.3))
            color = tuple([int(c * alpha / 255) for c in [255, 255, 255]])
            draw.line([(0, y), (self.video_width, y)], fill=color, width=1)
        
        # Save temporary background
        bg_path = f"temp_bg_{random.randint(1000, 9999)}.png"
        img.save(bg_path)
        
        # Create video clip
        bg_clip = ImageClip(bg_path).set_duration(duration)
        
        # Clean up temp file
        os.remove(bg_path)
        
        return bg_clip
    
    def _create_text_clip(self, text: str, theme: Dict[str, str], duration: float, position: str = "center") -> TextClip:
        """Tạo text clip với styling"""
        
        # Wrap text for better display
        wrapped_text = textwrap.fill(text, width=40)
        
        # Create text clip
        text_clip = TextClip(
            wrapped_text,
            fontsize=60,
            color=theme["text_color"],
            font='Arial-Bold',  # Use system font
            size=(self.video_width - 100, None)  # Leave margin
        ).set_duration(duration).set_position(position)
        
        return text_clip
    
    def _create_title_clip(self, title: str, theme: Dict[str, str], duration: float) -> TextClip:
        """Tạo title clip"""
        
        title_clip = TextClip(
            title,
            fontsize=80,
            color=theme["accent_color"],
            font='Arial-Bold',
            size=(self.video_width - 100, None)
        ).set_duration(min(3.0, duration)).set_position(('center', 'top')).set_margin(50)
        
        return title_clip
    
    async def _download_stock_image(self, query: str, category: str) -> str:
        """Download stock image based on category (placeholder for now)"""
        
        # For MVP, we'll use solid color backgrounds
        # In production, integrate with stock photo APIs like Unsplash
        
        return None
    
    def _get_category_keywords(self, category: str) -> List[str]:
        """Get relevant keywords for stock images"""
        
        keyword_map = {
            "business": ["office", "meeting", "success", "growth", "professional"],
            "self_development": ["motivation", "growth", "success", "mindset", "improvement"],
            "science": ["laboratory", "research", "discovery", "innovation", "technology"],
            "history": ["ancient", "historical", "monument", "artifacts", "civilization"],
            "technology": ["digital", "innovation", "future", "coding", "tech"],
            "health": ["wellness", "fitness", "nutrition", "healthcare", "lifestyle"],
            "other": ["education", "learning", "knowledge", "insight", "wisdom"]
        }
        
        return keyword_map.get(category, keyword_map["other"])
    
    async def create_thumbnail(self, script: str, category: str, job_id: str) -> str:
        """Tạo thumbnail cho video"""
        
        theme = self.category_themes.get(category, self.category_themes["other"])
        
        # Create thumbnail image
        img = Image.new('RGB', (1080, 1920), theme["bg_color"])
        draw = ImageDraw.Draw(img)
        
        # Extract first sentence for thumbnail text
        first_sentence = script.split('.')[0][:50] + "..."
        
        # Add text (simplified for MVP)
        try:
            # Use default font for now
            draw.text(
                (540, 960),  # Center position
                first_sentence,
                fill=theme["text_color"],
                anchor="mm"
            )
        except:
            # Fallback if text rendering fails
            pass
        
        # Save thumbnail
        thumbnail_filename = f"thumbnail_{job_id}.png"
        thumbnail_path = os.path.join(settings.output_folder, thumbnail_filename)
        img.save(thumbnail_path)
        
        return thumbnail_path 