import requests
import os
import json
from dotenv import load_dotenv
from config import CATEGORIES

load_dotenv()

class Processor:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.base_url = os.getenv("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"

    def process_with_ai(self, raw_news):
        print(f"🤖 正在调用 DeepSeek 处理文章...")
        cat_info = "\n".join([f"ID {v['id']}: {k}" for k, v in CATEGORIES.items()])
        
        # ✨ 强化 Prompt：明确禁止通用词，要求提取具体特征
        prompt = f"""
        Task: Rewrite this news for a global audience in Professional English and extract high-quality search keywords for a cover image.
        
        Source Title: {raw_news['title']}
        Source Content: {raw_news['summary']}
        
        Available Categories (Pick the most suitable ID):
        {cat_info}
        
        Output Requirements:
        1. Tone: Uplifting, positive, and professional.
        2. Format: Return a valid JSON object.
        3. Content Style: Use HTML tags (<p>, <strong>) for formatting. Break text into 2-3 paragraphs.
        4. Image Keywords Rules:
           - DO NOT use generic words like 'nature', 'happiness', 'news', or 'technology'.
           - Extract 2-3 SPECIFIC and VISUAL keywords based on the actual story (e.g., if it's about a solar farm, use 'solar panels energy'; if it's about a dog rescue, use 'golden retriever rescue').
           - Keywords must be in English and suitable for Unsplash search.
        
        Expected JSON Structure:
        {{
            "title": "A catchy, uplifting headline",
            "content": "<p>Paragraph 1...</p><p>Paragraph 2...</p>",
            "category_id": [2],
            "image_keywords": "specific visual keywords"
        }}
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}", 
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}
        }
        
        try:
            # 注意：确保 base_url 后面拼接的是正确的路径，有些厂商是 /v1/chat/completions
            response = requests.post(f"{self.base_url}/v1/chat/completions", json=data, headers=headers)
            response.raise_for_status()
            
            res_content = response.json()['choices'][0]['message']['content']
            res_dict = json.loads(res_content)
            
            # 容错处理：确保 category_id 是列表且元素为整数
            raw_cat = res_dict.get('category_id', [2])
            if isinstance(raw_cat, list):
                res_dict['category_id'] = [int(x) for x in raw_cat]
            else:
                res_dict['category_id'] = [int(raw_cat)]
            
            # 打印一下 AI 到底给出了什么词，方便你在后台观察
            print(f"🎨 AI 建议的配图关键词: {res_dict.get('image_keywords')}")
                
            return res_dict
            
        except Exception as e:
            print(f"❌ AI 处理失败: {e}")
            # 保底逻辑：如果失败，我们尝试从标题提取一个词，而不是死板的 "nature"
            fallback_keyword = raw_news['title'].split()[0] if raw_news['title'] else "inspiration"
            return {
                "title": raw_news['title'],
                "content": raw_news['summary'],
                "category_id": [2],
                "image_keywords": fallback_keyword
            }