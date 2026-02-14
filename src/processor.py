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
        
        # 准备分类信息给 AI 参考
        cat_info = "\n".join([f"ID {v['id']}: {k}" for k, v in CATEGORIES.items()])
        
        prompt = f"""
        Task: Rewrite this news for a global audience in Professional English.
        
        Source Title: {raw_news['title']}
        Source Content: {raw_news['summary']}
        
        Available Categories (Pick the most suitable ID):
        {cat_info}
        
        Output Requirements:
        1. Tone: Uplifting and professional.
        2. Language: English only.
        3. Format: You MUST return a valid JSON object.
        
        Expected JSON Structure:
        {{
            "title": "Uplifting Title Here",
            "content": "Professional article content here...",
            "category_id": [The chosen ID number],
            "image_keywords": "2-3 keywords for Unsplash image search"
        }}
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}", 
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            # 💡 强制 DeepSeek 返回 JSON 格式
            "response_format": {"type": "json_object"}
        }
        
        try:
            response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
            response.raise_for_status()
            
            # 解析 JSON
            res_content = response.json()['choices'][0]['message']['content']
            res_dict = json.loads(res_content)
            
            # 💡 确保返回的是一个字典对象
            return res_dict
            
        except Exception as e:
            print(f"❌ AI 处理失败: {e}")
            # 如果失败，返回一个保底的字典格式，防止 main.py 崩溃
            return {
                "title": raw_news['title'],
                "content": raw_news['summary'],
                "category_id": [2], # 默认 Humanity
                "image_keywords": "nature"
            }