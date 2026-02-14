# config.py

# WordPress 分类配置
# 请替换下面的 ID 为你 WP 后台真实的 tag_ID
CATEGORIES = {
    "Humanity": {
        "id": 2, 
        "keywords": "heartwarming acts of kindness charity"
    },
    "Environment": {
        "id": 3, 
        "keywords": "environmental protection wildlife rescue positive"
    },
    "Innovation": {
        "id": 4, 
        "keywords": "medical breakthrough technological innovation record"
    },
    "Daily Hero": {
        "id": 5, 
        "keywords": "everyday heroes inspirational act of courage"
    },
    "Uplifting Stories": {
        "id": 6, 
        "keywords": "inspirational success stories life changing"
    }
}

# AI 审核与摘要的系统提示词
SYSTEM_PROMPT = """
You are a positive news editor for 'Daily Good Vibes'. 
Your mission is to find and rewrite heartwarming stories.
1. Safety Check: Strictly filter out politics, war, crime, or negative news. If not a positive story, return 'REJECT'.
2. Tone: Uplifting, hopeful, and heartwarming.
3. Language: Professional English.
"""