#!/usr/bin/env python3
"""
🚀 Enhanced AI Prompts for Viral TikTok Content
Optimized prompts for maximum engagement and virality
"""

class ViralContentPrompts:
    """Advanced prompts for viral TikTok content generation"""
    
    @staticmethod
    def get_content_analysis_prompt(content: str, duration: int, language: str = "en") -> str:
        """Get enhanced content analysis prompt"""
        
        target_words = int((duration / 60) * 175)
        
        if language == "vi":
            return f"""
🎬 NHIỆM VỤ: Tạo script TikTok VIRAL từ nội dung sau

📝 NỘI DUNG NGUỒN:
{content[:2500]}

🎯 YÊU CẦU CHI TIẾT:
- Thời lượng: {duration} giây ({target_words} từ)
- Ngôn ngữ: Tiếng Việt tự nhiên, Gen Z
- Hook: 3 giây đầu PHẢI hấp dẫn (dùng số liệu, câu hỏi, shock)
- Cấu trúc: Pattern 3-5-7 (3 hook, 5 điểm chính, 7 từ khóa)
- Tone: Conversation, friendly, như nói chuyện với bạn
- Call-to-action: Mạnh mẽ, specific

🔥 VIRAL ELEMENTS (PHẢI CÓ):
- Numbers/Statistics (70% hiệu quả hơn)
- Personal story element
- Controversy/Different perspective 
- Actionable tips
- Emotional hooks (surprise, curiosity, urgency)
- Trend-jacking (current events/viral topics)

📱 FORMAT CHUẨN:
{{
    "hook": "Câu mở VIRAL (dùng số/câu hỏi/shock fact)",
    "pain_point": "Vấn đề người xem đang gặp",
    "main_points": [
        "Điểm 1: Concrete + benefit",
        "Điểm 2: Story + emotion", 
        "Điểm 3: Action + result"
    ],
    "script": "Full script để đọc (natural flow)",
    "viral_elements": ["element1", "element2"],
    "engagement_hooks": ["câu hỏi 1", "câu hỏi 2"],
    "category": "education/entertainment/lifestyle",
    "trending_keywords": ["viral_keyword1", "viral_keyword2"],
    "estimated_duration": {duration},
    "virality_score": "8.5/10",
    "target_audience": "Gen Z, millennials interested in..."
}}

🚀 LƯU Ý: Script phải đọc được trong {duration} giây, tự nhiên như nói chuyện!
"""
        else:
            return f"""
🎬 MISSION: Create VIRAL TikTok script from this content

📝 SOURCE CONTENT:
{content[:2500]}

🎯 DETAILED REQUIREMENTS:
- Duration: {duration} seconds ({target_words} words)
- Language: Natural English, Gen Z tone
- Hook: First 3 seconds MUST grab attention (use stats, questions, shock)
- Structure: 3-5-7 Pattern (3 hooks, 5 main points, 7 keywords)
- Tone: Conversational, like talking to a friend
- CTA: Strong, specific action

🔥 VIRAL ELEMENTS (MUST INCLUDE):
- Numbers/Statistics (70% more effective)
- Personal story element
- Controversy/Different perspective
- Actionable tips
- Emotional hooks (surprise, curiosity, urgency)
- Trend-jacking (current events/viral topics)

📱 REQUIRED FORMAT:
{{
    "hook": "VIRAL opening (use numbers/questions/shock facts)",
    "pain_point": "Problem viewers are facing",
    "main_points": [
        "Point 1: Concrete + benefit",
        "Point 2: Story + emotion",
        "Point 3: Action + result"
    ],
    "script": "Complete readable script (natural flow)",
    "viral_elements": ["element1", "element2"],
    "engagement_hooks": ["question1", "question2"],
    "category": "education/entertainment/lifestyle",
    "trending_keywords": ["viral_keyword1", "viral_keyword2"],
    "estimated_duration": {duration},
    "virality_score": "8.5/10",
    "target_audience": "Gen Z, millennials interested in..."
}}

🚀 NOTE: Script must be readable in exactly {duration} seconds, natural like conversation!
"""

    @staticmethod
    def get_marketing_prompt(script: str, category: str, keywords: list, language: str = "en") -> str:
        """Get enhanced marketing content prompt"""
        
        if language == "vi":
            return f"""
🔥 TẠO MARKETING CONTENT VIRAL CHO TIKTOK

📝 SCRIPT: {script[:500]}...
🎯 CATEGORY: {category}
🔑 KEYWORDS: {', '.join(keywords)}

🚀 YÊU CẦU MARKETING:
1. Caption: 2-3 dòng, hook strong, CTA clear
2. Hashtags: 15-20 tags (mix trending + niche)
3. Description: SEO-optimized, 150-200 từ
4. Engagement bait: 3 câu hỏi khác nhau
5. Comments strategy: Seed comments đầu tiên

📱 VIRAL MARKETING ELEMENTS:
- Trending hashtags (check TikTok trends)
- Niche-specific tags for algorithm
- Question hooks for comments
- Share-worthy captions
- Cross-platform optimization

💎 FORMAT CHUẨN:
{{
    "caption": "Hook + value + CTA (2-3 dòng viral)",
    "hashtags": [
        "#viral", "#fyp", "#trending",
        "#{category}specific", "#niche_tags"
    ],
    "description": "SEO description với keywords natural",
    "engagement_questions": [
        "Câu hỏi 1 (controversial)",
        "Câu hỏi 2 (personal experience)", 
        "Câu hỏi 3 (action-oriented)"
    ],
    "seed_comments": [
        "Comment 1 (positive reaction)",
        "Comment 2 (asking for more)",
        "Comment 3 (sharing experience)"
    ],
    "cross_platform": {{
        "instagram": "IG-optimized caption",
        "youtube_shorts": "YT-optimized title",
        "twitter": "Twitter thread starter"
    }},
    "posting_strategy": {{
        "best_time": "7-9 PM weekdays",
        "frequency": "2-3 times per week",
        "follow_up": "Part 2 if viral"
    }}
}}
"""
        else:
            return f"""
🔥 CREATE VIRAL MARKETING CONTENT FOR TIKTOK

📝 SCRIPT: {script[:500]}...
🎯 CATEGORY: {category}
🔑 KEYWORDS: {', '.join(keywords)}

🚀 MARKETING REQUIREMENTS:
1. Caption: 2-3 lines, strong hook, clear CTA
2. Hashtags: 15-20 tags (mix trending + niche)
3. Description: SEO-optimized, 150-200 words
4. Engagement bait: 3 different question types
5. Comments strategy: First seed comments

📱 VIRAL MARKETING ELEMENTS:
- Trending hashtags (check TikTok trends)
- Niche-specific tags for algorithm
- Question hooks for comments
- Share-worthy captions
- Cross-platform optimization

💎 REQUIRED FORMAT:
{{
    "caption": "Hook + value + CTA (2-3 viral lines)",
    "hashtags": [
        "#viral", "#fyp", "#trending",
        "#{category}specific", "#niche_tags"
    ],
    "description": "SEO description with natural keywords",
    "engagement_questions": [
        "Question 1 (controversial)",
        "Question 2 (personal experience)",
        "Question 3 (action-oriented)"
    ],
    "seed_comments": [
        "Comment 1 (positive reaction)",
        "Comment 2 (asking for more)",
        "Comment 3 (sharing experience)"
    ],
    "cross_platform": {{
        "instagram": "IG-optimized caption",
        "youtube_shorts": "YT-optimized title", 
        "twitter": "Twitter thread starter"
    }},
    "posting_strategy": {{
        "best_time": "7-9 PM weekdays",
        "frequency": "2-3 times per week",
        "follow_up": "Part 2 if viral"
    }}
}}
"""

class VoiceOptimization:
    """Optimize voice generation for different content types"""
    
    VOICE_STYLES = {
        "education": {
            "voice_id": "Rachel",  # Professional female
            "stability": 0.7,
            "similarity_boost": 0.8,
            "style": "clear and authoritative"
        },
        "entertainment": {
            "voice_id": "Josh",   # Energetic male
            "stability": 0.5,
            "similarity_boost": 0.9,
            "style": "dynamic and engaging"
        },
        "lifestyle": {
            "voice_id": "Bella",  # Friendly female
            "stability": 0.8,
            "similarity_boost": 0.7,
            "style": "warm and conversational"
        },
        "business": {
            "voice_id": "Antoni", # Professional male
            "stability": 0.9,
            "similarity_boost": 0.6,
            "style": "confident and trustworthy"
        }
    }
    
    @staticmethod
    def get_voice_settings(category: str, content_type: str = "script") -> dict:
        """Get optimized voice settings for content category"""
        
        base_settings = VoiceOptimization.VOICE_STYLES.get(
            category, 
            VoiceOptimization.VOICE_STYLES["education"]
        )
        
        # Adjust for content type
        if content_type == "hook":
            # More energetic for hooks
            base_settings["stability"] = max(0.4, base_settings["stability"] - 0.2)
            base_settings["similarity_boost"] = min(1.0, base_settings["similarity_boost"] + 0.1)
        elif content_type == "conclusion":
            # More stable for conclusions
            base_settings["stability"] = min(0.9, base_settings["stability"] + 0.1)
        
        return base_settings

# Export for use in ai_services.py
ENHANCED_PROMPTS = ViralContentPrompts()
VOICE_OPTIMIZER = VoiceOptimization() 