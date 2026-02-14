import requests
import os
from dotenv import load_dotenv

# 💡 必须添加这一行，否则 os.getenv 拿不到数据
load_dotenv()

class Processor:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        # 💡 如果环境变量里没有，就给一个默认值防止报错
        self.base_url = os.getenv("DEEPSEEK_BASE_URL") or "https://api.deepseek.com"

    def process_with_ai(self, raw_news):
        print(f"🤖 正在调用 DeepSeek 处理文章...")
        
        prompt = f"""
        你是一个正能量新闻编辑。请将以下内容改写成一篇温馨、积极的中文博客文章。
        原文语言: {raw_news.get('lang', 'en')}
        原文标题: {raw_news.get('title', '')}
        原文内容: {raw_news.get('summary', '')}
        
        要求：
        1. 标题要吸引人。
        2. 正文要求通顺、温馨，字数约300-500字。
        3. 统一输出为中文。
        4. 结尾加一个【今日感悟】。
        
        输出格式严格遵守：
        TITLE: [标题]
        CONTENT: [正文内容]
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}", 
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", json=data, headers=headers)
        
        # 检查 API 是否请求成功
        if response.status_code != 200:
            raise Exception(f"DeepSeek API 报错: {response.text}")

        result = response.json()['choices'][0]['message']['content']
        
        # 更加稳健的解析逻辑
        try:
            if "TITLE:" in result and "CONTENT:" in result:
                new_title = result.split("TITLE:")[1].split("CONTENT:")[0].strip()
                new_content = result.split("CONTENT:")[1].strip()
            else:
                # 如果 AI 没按格式返回，则简单处理
                new_title = raw_news.get('title', '今日好消息')
                new_content = result
            
            return new_title, new_content
        except Exception as e:
            print(f"解析 AI 返回内容失败: {e}")
            return raw_news.get('title'), result