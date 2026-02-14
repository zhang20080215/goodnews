import os
import time
import requests
from dotenv import load_dotenv
from config import CATEGORIES
from src.scraper import Scraper
from src.processor import Processor
from src.publisher import WordPressPublisher

load_dotenv()

def get_unsplash_image(query):
    """根据关键词获取一张美图"""
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    url = f"https://api.unsplash.com/photos/random?query={query}&orientation=landscape&client_id={access_key}"
    try:
        res = requests.get(url).json()
        return res['urls']['regular']
    except:
        return "https://images.unsplash.com/photo-1499209974431-9dac3adaf477" # 默认图

def is_posted(url):
    if not os.path.exists("processed_urls.txt"): return False
    with open("processed_urls.txt", "r") as f:
        return url in f.read()

def mark_as_posted(url):
    with open("processed_urls.txt", "a") as f:
        f.write(url + "\n")

def main():
    scraper = Scraper()
    processor = Processor()
    publisher = WordPressPublisher()

    print("🚀 启动自动化任务...")
    news_items = scraper.fetch_all(limit=5)
    
    for item in news_items:
        if is_posted(item['link']): continue
            
        try:
            print(f"📰 处理: {item['title']}")
            
            # AI 处理内容
            title, content = processor.process_with_ai(item)
            
            # 💡 增加原文链接
            content += f'<br><hr><p>内容来源: <a href="{item["link"]}" target="_blank">阅读原文</a></p>'
            
            # 💡 获取并上传图片
            img_url = get_unsplash_image("positivity,nature")
            media_id = publisher.upload_image(img_url)
            
            # 发布
            if publisher.publish(title, content, [CATEGORIES["Humanity"]["id"]], media_id):
                print(f"✅ 发布成功")
                mark_as_posted(item['link'])
            
            time.sleep(10)
        except Exception as e:
            print(f"⚠️ 错误: {e}")

if __name__ == "__main__":
    main()