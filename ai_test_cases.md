# 🧪 AI Features Test Cases

## 🎯 High-Quality Content Sources

### 📚 Educational Content
1. **Wikipedia AI Article:**
   ```
   URL: https://en.wikipedia.org/wiki/Artificial_intelligence
   Expected: Technical but accessible explanation
   Duration: 90 seconds
   Voice: Professional
   ```

2. **Medium AI Article:**
   ```
   URL: https://medium.com/@example/future-of-ai
   Expected: Engaging narrative style
   Duration: 60 seconds
   Voice: Conversational
   ```

### 📖 Book Summaries
3. **Atomic Habits Summary:**
   ```
   URL: https://www.blinkist.com/en/books/atomic-habits-en
   Expected: Actionable insights format
   Duration: 120 seconds
   Voice: Motivational
   ```

4. **Business Article:**
   ```
   URL: https://hbr.org/2024/01/how-ai-will-transform-business
   Expected: Professional insights
   Duration: 90 seconds
   Voice: Executive
   ```

## 🎪 Test API Calls

### Test 1: Simple URL Processing
```json
{
  "url": "https://en.wikipedia.org/wiki/Machine_learning",
  "content_type": "url",
  "use_ai": true,
  "settings": {
    "duration": 60,
    "voice_style": "professional",
    "language": "en"
  }
}
```

### Test 2: Vietnamese Content
```json
{
  "url": "https://vi.wikipedia.org/wiki/Tr%C3%AD_tu%E1%BB%87_nh%C3%A2n_t%E1%BA%A1o",
  "content_type": "url",
  "use_ai": true,
  "settings": {
    "duration": 90,
    "voice_style": "friendly",
    "language": "vi"
  }
}
```

### Test 3: Long-form Content
```json
{
  "url": "https://waitbutwhy.com/2015/01/artificial-intelligence-revolution-1.html",
  "content_type": "url", 
  "use_ai": true,
  "settings": {
    "duration": 180,
    "voice_style": "storytelling",
    "language": "en"
  }
}
```

## ✅ Expected AI Improvements

### 🤖 Content Analysis (OpenAI)
- Extract key insights automatically
- Generate compelling hooks
- Create viral-worthy scripts
- Suggest optimal video length
- Add emotional triggers

### 🎙️ Voice Generation (ElevenLabs)
- Natural pronunciation
- Appropriate pacing
- Emotional inflection
- Clear articulation
- Professional quality

### 📊 Quality Metrics
- Script engagement score
- Voice naturalness rating
- Content comprehension level
- Viral potential indicator
- Time-to-completion

## 🚨 Troubleshooting Checklist

### If AI Not Working:
- [ ] Check API keys are valid
- [ ] Verify Railway environment variables
- [ ] Test API key permissions
- [ ] Check billing/credits
- [ ] Monitor Railway logs

### If Voice Generation Fails:
- [ ] Verify ElevenLabs subscription
- [ ] Check character limits
- [ ] Test with shorter text
- [ ] Try different voice IDs
- [ ] Check audio format support

### If Content Analysis Poor:
- [ ] Improve prompt engineering
- [ ] Add content guidelines
- [ ] Filter low-quality sources
- [ ] Implement content scoring
- [ ] A/B test prompts 