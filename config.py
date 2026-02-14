# config.py

# --- 新闻源配置 ---
# 这里定义了你要抓取的所有 RSS 源
NEWS_SOURCES = [
    "https://www.goodnewsnetwork.org/category/news/feed/",
    "https://www.positive.news/feed/",
    "https://www.optimistdaily.com/feed/",
    "https://reasonstobecheerful.world/feed/",
    "https://www.goodgoodgood.co/feed/",
    "https://nypost.com/tag/good-news/feed/", # 额外新增：大报的正能量版块
    "https://www.huffpost.com/section/good-news/feed" # 额外新增：HuffPost 
]

# 每个数据源抓取的新闻数量限制（建议设为 2-3，防止 AI 处理过慢）
FETCH_LIMIT_PER_SOURCE = 5

# --- WordPress 分类配置 ---
# 请确保这些 ID 与你 WP 后台 -> 文章 -> 分类目录中的 ID 一致
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

# --- AI 配置 ---
# AI 审核与摘要的系统提示词
SYSTEM_PROMPT = """
You are a positive news editor for 'Daily Good Vibes'. 
Your mission is to find and rewrite heartwarming stories.
1. Safety Check: Strictly filter out politics, war, crime, or negative news. If not a positive story, return 'REJECT'.
2. Tone: Uplifting, hopeful, and heartwarming.
3. Language: Professional English only.
4. Formatting: Use HTML tags (<p>, <strong>) for the content body.
"""

# --- 存储配置 ---
HISTORY_FILE = "processed_urls.txt"
