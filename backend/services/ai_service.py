import openai
import json
from typing import Dict, List, Any
from config import settings
from models.schemas import ContentCategory, MarketingContent

class AIService:
    """Service để xử lý AI tasks với OpenAI GPT"""
    
    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key không được tìm thấy")
        
        openai.api_key = settings.openai_api_key
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
    
    async def analyze_content(self, content: str, target_duration: int) -> Dict[str, Any]:
        """Phân tích nội dung và tạo script cho video"""
        
        # Estimate words per minute for script (average speaking speed: 150-160 WPM)
        target_words = int(target_duration * 2.5)  # Conservative estimate
        
        system_prompt = f"""
        Bạn là chuyên gia phân tích nội dung và tạo script video. Nhiệm vụ:
        
        1. Phân tích nội dung và xác định thể loại chính
        2. Trích xuất những điểm hay nhất, ấn tượng nhất
        3. Tạo script video hấp dẫn với thời lượng khoảng {target_duration} giây ({target_words} từ)
        
        Yêu cầu script:
        - Bắt đầu với hook hấp dẫn để giữ chân người xem
        - Trình bày các điểm chính một cách súc tích và mạnh mẽ
        - Sử dụng ngôn ngữ dễ hiểu, phù hợp với video ngắn
        - Kết thúc với call-to-action hoặc câu khuyến khích
        - Độ dài phù hợp để đọc trong {target_duration} giây
        
        Trả về JSON với format:
        {{
            "category": "business/self_development/science/history/technology/health/other",
            "key_points": ["điểm 1", "điểm 2", "điểm 3"],
            "script": "script hoàn chỉnh",
            "estimated_duration": {target_duration},
            "tone": "mô tả tone phù hợp"
        }}
        """
        
        user_prompt = f"Nội dung cần phân tích:\n\n{content[:8000]}"  # Limit content length
        
        try:
            response = self.client.chat.completions.create(
                model=settings.gpt_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=settings.max_tokens,
                temperature=settings.temperature
            )
            
            result = response.choices[0].message.content
            
            # Parse JSON response
            analysis = json.loads(result)
            
            # Validate and set defaults
            analysis["category"] = analysis.get("category", "other")
            analysis["key_points"] = analysis.get("key_points", [])
            analysis["script"] = analysis.get("script", "")
            analysis["estimated_duration"] = analysis.get("estimated_duration", target_duration)
            analysis["tone"] = analysis.get("tone", "professional")
            
            return analysis
            
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return await self._fallback_analysis(content, target_duration)
        except Exception as e:
            raise Exception(f"Lỗi khi phân tích nội dung với AI: {str(e)}")
    
    async def generate_marketing_content(self, script: str, category: str) -> MarketingContent:
        """Tạo caption, hashtag và description cho video"""
        
        system_prompt = """
        Bạn là chuyên gia marketing content cho TikTok/social media. 
        Tạo content marketing hấp dẫn cho video dựa trên script và thể loại.
        
        Yêu cầu:
        - Caption ngắn gọn, hấp dẫn, có emoji
        - Hashtag mix giữa trending và niche (10-15 hashtags)
        - Description chi tiết hơn cho mô tả video
        - Hook câu mở đầu thu hút attention
        
        Trả về JSON format:
        {
            "caption": "caption với emoji",
            "hashtags": ["hashtag1", "hashtag2", ...],
            "description": "mô tả chi tiết",
            "hook": "câu hook thu hút"
        }
        """
        
        user_prompt = f"""
        Script video: {script}
        
        Thể loại: {category}
        
        Tạo marketing content phù hợp.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=settings.gpt_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.8
            )
            
            result = response.choices[0].message.content
            marketing_data = json.loads(result)
            
            return MarketingContent(
                caption=marketing_data.get("caption", ""),
                hashtags=marketing_data.get("hashtags", []),
                description=marketing_data.get("description", ""),
                hook=marketing_data.get("hook", "")
            )
            
        except Exception as e:
            # Fallback marketing content
            return self._fallback_marketing_content(category)
    
    async def _fallback_analysis(self, content: str, target_duration: int) -> Dict[str, Any]:
        """Fallback analysis nếu AI response lỗi"""
        
        # Simple content analysis
        content_lower = content.lower()
        
        # Determine category based on keywords
        category = "other"
        if any(word in content_lower for word in ["business", "kinh doanh", "marketing", "bán hàng"]):
            category = "business"
        elif any(word in content_lower for word in ["phát triển", "cải thiện", "thành công", "kỹ năng"]):
            category = "self_development"
        elif any(word in content_lower for word in ["khoa học", "nghiên cứu", "thí nghiệm"]):
            category = "science"
        elif any(word in content_lower for word in ["lịch sử", "quá khứ", "cổ đại"]):
            category = "history"
        elif any(word in content_lower for word in ["công nghệ", "AI", "digital", "tech"]):
            category = "technology"
        
        # Extract first few sentences as key points
        sentences = content.split('.')[:5]
        key_points = [s.strip() for s in sentences if len(s.strip()) > 20][:3]
        
        # Simple script creation
        preview = content[:500] + "..."
        script = f"Hôm nay tôi sẽ chia sẻ với các bạn những insights thú vị từ nội dung này. {preview} Đây thực sự là những kiến thức quý giá mà chúng ta nên áp dụng trong cuộc sống."
        
        return {
            "category": category,
            "key_points": key_points,
            "script": script,
            "estimated_duration": target_duration,
            "tone": "friendly"
        }
    
    def _fallback_marketing_content(self, category: str) -> MarketingContent:
        """Fallback marketing content"""
        
        hashtag_map = {
            "business": ["#business", "#entrepreneur", "#success", "#marketing", "#kinh doanh"],
            "self_development": ["#selfimprovement", "#motivation", "#success", "#mindset", "#phát triển bản thân"],
            "science": ["#science", "#education", "#learning", "#khoa học", "#knowledge"],
            "history": ["#history", "#facts", "#educational", "#lịch sử", "#story"],
            "technology": ["#tech", "#AI", "#innovation", "#technology", "#công nghệ"],
            "health": ["#health", "#wellness", "#fitness", "#sức khỏe", "#lifestyle"]
        }
        
        base_hashtags = ["#viral", "#fyp", "#trending", "#shorts", "#video", "#vietnamese", "#việt nam"]
        category_hashtags = hashtag_map.get(category, ["#educational", "#interesting"])
        
        all_hashtags = category_hashtags + base_hashtags
        
        return MarketingContent(
            caption=f"🔥 Kiến thức thú vị mà bạn nên biết! #{category} #trending",
            hashtags=all_hashtags,
            description=f"Video chia sẻ những insights quý giá trong lĩnh vực {category}. Đừng quên follow để cập nhật thêm nhiều nội dung hay!",
            hook="Bạn có biết điều này không? 🤔"
        ) 