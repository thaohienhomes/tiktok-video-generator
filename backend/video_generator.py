#!/usr/bin/env python3
"""
Video Generator for TikTok-style videos
Creates MP4 videos with voiceover, text overlays, and transitions
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
import time

# Try to import MoviePy
try:
    from moviepy.editor import *
    from moviepy.config import IMAGEIO_BINARY
    MOVIEPY_AVAILABLE = True
    print("✅ MoviePy imported successfully")
except ImportError as e:
    MOVIEPY_AVAILABLE = False
    print(f"⚠️ MoviePy not available: {e}")
    print("🔄 Using simulation mode for video generation")

class VideoGenerator:
    """Generate TikTok-style videos with AI content"""
    
    def __init__(self):
        self.output_dir = Path("outputs")
        self.output_dir.mkdir(exist_ok=True)
        
        # TikTok standard dimensions
        self.width = 1080
        self.height = 1920
        self.fps = 30
        
        # Default colors and fonts
        self.bg_color = (20, 20, 30)  # Dark background
        self.text_color = "white"
        self.accent_color = "#00D4FF"  # TikTok blue
        
    async def generate_video(self, 
                           script_data: Dict[str, Any],
                           voice_file: str,
                           settings: Dict[str, Any]) -> Dict[str, Any]:
        """Generate complete video from script and voice"""
        
        if not MOVIEPY_AVAILABLE:
            return self._simulate_video_generation(script_data, voice_file, settings)
        
        try:
            # Parse script into segments
            segments = self._parse_script_segments(script_data)
            
            # Load voice audio
            if os.path.exists(voice_file):
                audio = AudioFileClip(voice_file)
                duration = audio.duration
            else:
                # Fallback: estimate duration from text
                word_count = len(script_data.get('script', '').split())
                duration = max(15, word_count / 2.5)  # ~150 words per minute
                audio = None
            
            # Create video clips
            clips = []
            
            # 1. Background clip
            bg_clip = self._create_background_clip(duration)
            clips.append(bg_clip)
            
            # 2. Text overlay clips
            text_clips = self._create_text_overlays(segments, duration)
            clips.extend(text_clips)
            
            # 3. Add visual elements (hook, transitions)
            visual_clips = self._create_visual_elements(script_data, duration)
            clips.extend(visual_clips)
            
            # Composite all clips
            final_video = CompositeVideoClip(clips, size=(self.width, self.height))
            
            # Add audio if available
            if audio:
                final_video = final_video.set_audio(audio)
            
            # Generate output filename
            timestamp = int(time.time())
            output_filename = f"tiktok_video_{timestamp}.mp4"
            output_path = self.output_dir / output_filename
            
            # Render video
            final_video.write_videofile(
                str(output_path),
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                verbose=False,
                logger=None
            )
            
            # Clean up
            final_video.close()
            if audio:
                audio.close()
            
            return {
                "success": True,
                "video_path": str(output_path),
                "filename": output_filename,
                "duration": duration,
                "resolution": f"{self.width}x{self.height}",
                "fps": self.fps,
                "file_size": os.path.getsize(output_path) if output_path.exists() else 0,
                "segments_count": len(segments)
            }
            
        except Exception as e:
            print(f"❌ Video generation error: {e}")
            return self._simulate_video_generation(script_data, voice_file, settings)
    
    def _parse_script_segments(self, script_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse script into timed segments for text overlays"""
        
        script = script_data.get('script', '')
        main_points = script_data.get('main_points', [])
        hook = script_data.get('hook', '')
        
        segments = []
        
        # Hook segment (first 3 seconds)
        if hook:
            segments.append({
                "text": hook,
                "start_time": 0,
                "duration": 3,
                "style": "hook",
                "position": "center"
            })
        
        # Main content segments
        remaining_duration = script_data.get('estimated_duration', 60) - 3
        
        if main_points:
            segment_duration = remaining_duration / len(main_points)
            
            for i, point in enumerate(main_points):
                segments.append({
                    "text": point,
                    "start_time": 3 + (i * segment_duration),
                    "duration": segment_duration,
                    "style": "main_point",
                    "position": "bottom" if i % 2 == 0 else "top"
                })
        else:
            # Split script into sentences
            sentences = [s.strip() + '.' for s in script.split('.') if s.strip()]
            if sentences:
                segment_duration = remaining_duration / len(sentences)
                
                for i, sentence in enumerate(sentences):
                    segments.append({
                        "text": sentence,
                        "start_time": 3 + (i * segment_duration),
                        "duration": segment_duration,
                        "style": "sentence",
                        "position": "center"
                    })
        
        return segments
    
    def _create_background_clip(self, duration: float) -> VideoClip:
        """Create animated background"""
        
        def make_frame(t):
            # Create gradient background with subtle animation
            import numpy as np
            
            # Gradient colors that change over time
            r = int(self.bg_color[0] + 10 * np.sin(t * 0.5))
            g = int(self.bg_color[1] + 15 * np.sin(t * 0.3))
            b = int(self.bg_color[2] + 20 * np.sin(t * 0.7))
            
            # Create frame
            frame = np.full((self.height, self.width, 3), [r, g, b], dtype=np.uint8)
            
            return frame
        
        return VideoClip(make_frame, duration=duration)
    
    def _create_text_overlays(self, segments: List[Dict[str, Any]], total_duration: float) -> List[VideoClip]:
        """Create text overlay clips for each segment"""
        
        text_clips = []
        
        for segment in segments:
            style = segment['style']
            position = segment['position']
            
            # Text styling based on segment type
            if style == "hook":
                fontsize = 80
                color = self.accent_color
                font = 'Arial-Bold'
            elif style == "main_point":
                fontsize = 60
                color = self.text_color
                font = 'Arial'
            else:
                fontsize = 50
                color = self.text_color
                font = 'Arial'
            
            # Position mapping
            if position == "top":
                pos = ('center', 200)
            elif position == "bottom":
                pos = ('center', self.height - 300)
            else:
                pos = 'center'
            
            # Create text clip
            txt_clip = TextClip(
                segment['text'],
                fontsize=fontsize,
                color=color,
                font=font,
                stroke_color='black',
                stroke_width=2
            ).set_position(pos).set_start(segment['start_time']).set_duration(segment['duration'])
            
            # Add fade in/out
            txt_clip = txt_clip.crossfadein(0.5).crossfadeout(0.5)
            
            text_clips.append(txt_clip)
        
        return text_clips
    
    def _create_visual_elements(self, script_data: Dict[str, Any], duration: float) -> List[VideoClip]:
        """Create additional visual elements (particles, shapes, etc.)"""
        
        visual_clips = []
        
        # Add subtle particles or shapes
        # This is simplified - in production, you'd add more sophisticated animations
        
        try:
            # Create accent color bars that move across screen
            def make_accent_frame(t):
                import numpy as np
                frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
                
                # Moving accent bar
                bar_y = int((t * 50) % self.height)
                frame[bar_y:bar_y+5, :] = [0, 212, 255]  # TikTok blue
                
                return frame
            
            accent_clip = VideoClip(make_accent_frame, duration=duration).set_opacity(0.1)
            visual_clips.append(accent_clip)
            
        except Exception as e:
            print(f"❌ Visual elements error: {e}")
        
        return visual_clips
    
    def _simulate_video_generation(self, script_data: Dict[str, Any], voice_file: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        """Simulation fallback when MoviePy is not available"""
        
        print("🎬 Video Generation Simulated:")
        print(f"   Script length: {len(script_data.get('script', ''))}")
        print(f"   Voice file: {voice_file}")
        print(f"   Duration: {script_data.get('estimated_duration', 60)} seconds")
        print(f"   Resolution: {self.width}x{self.height}")
        
        timestamp = int(time.time())
        output_filename = f"simulated_video_{timestamp}.mp4"
        
        return {
            "success": True,
            "video_path": f"outputs/{output_filename}",
            "filename": output_filename,
            "duration": script_data.get('estimated_duration', 60),
            "resolution": f"{self.width}x{self.height}",
            "fps": self.fps,
            "file_size": 50000000,  # Simulated 50MB
            "segments_count": len(script_data.get('main_points', [])),
            "simulated": True
        }
    
    async def create_thumbnail(self, video_path: str) -> Optional[str]:
        """Create thumbnail from video"""
        
        if not MOVIEPY_AVAILABLE or not os.path.exists(video_path):
            return None
        
        try:
            video = VideoFileClip(video_path)
            
            # Extract frame at 25% of video
            frame_time = video.duration * 0.25
            
            thumbnail_path = video_path.replace('.mp4', '_thumbnail.jpg')
            video.save_frame(thumbnail_path, t=frame_time)
            
            video.close()
            
            return thumbnail_path
            
        except Exception as e:
            print(f"❌ Thumbnail creation error: {e}")
            return None

# Initialize video generator
video_generator = VideoGenerator()

# Export for easy import
__all__ = ['video_generator'] 