import os
import time
import requests
from dotenv import load_dotenv
from config import CATEGORIES
from src.scraper import Scraper
from src.processor import Processor
from src.publisher import WordPressPublisher

# 加载环境变量
load_dotenv()

def get_unsplash_image(keywords):
    """根据 AI 提供的关键词从 Unsplash 获取图片"""
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    # 如果 AI 没给关键词，用默认的
    search_query = keywords if keywords else "positivity,nature"
    
    url = f"https://api.unsplash.com/photos/random?query={search_query}&orientation=landscape&client_id={access_key}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            res_data = response.json()
            return res_data['urls']['regular']
        else:
            print(f"🖼️ Unsplash API 返回错误: {response.status_code}")
            return "https://images.unsplash.com/photo-1499209974431-9dac3adaf477" # 默认温馨图
    except Exception as e:
        print(f"🖼️ 获取图片异常: {e}")
        return "https://images.unsplash.com/photo-1499209974431-9dac3adaf477"

def is_posted(url):
    """检查链接是否已发布"""
    if not os.path.exists("processed_urls.txt"):
        return False
    with open("processed_urls.txt", "r") as f:
        return url in f.read()

def mark_as_posted(url):
    """记录已发布的链接"""
    with open("processed_urls.txt", "a") as f:
        f.write(url + "\n")

def main():
    scraper = Scraper()
    processor = Processor()
    publisher = WordPressPublisher()

    print("🚀 开始自动化任务 (Global English Edition)...")
    
    # 获取新闻
    news_items = scraper.fetch_all(limit=2)
    print(f"📝 总共抓取到 {len(news_items)} 条待处理新闻")
    
    for item in news_items:
        if is_posted(item['link']):
            print(f"⏭️ 跳过已发布的: {item['title'][:30]}...")
            continue
            
        try:
            print(f"📰 处理新闻: {item['title'][:40]}...")
            
            # 1. AI 处理 (翻译、分类、生成关键词)
            ai_data = processor.process_with_ai(item)
            
            # 2. 准备发布内容
            final_title = ai_data.get('title', item['title'])
            # 在内容末尾增加原文链接
            final_content = ai_data.get('content', '') + f'<br><hr><p>Source: <a href="{item["link"]}" target="_blank">Read Original</a></p>'
            
            # 3. 获取并上传相关图片
            img_kw = ai_data.get('image_keywords', 'positivity')
            img_url = get_unsplash_image(img_kw)
            print(f"🖼️ 为关键词 '{img_kw}' 匹配到图片: {img_url}")
            
            media_id = publisher.upload_image(img_url)
            
            # 4. 获取分类 (确保是列表格式)
            cat_ids = ai_data.get('category_id', [2])
            if not isinstance(cat_ids, list):
                cat_ids = [cat_ids]
            
            # 5. 发布到 WordPress
            if publisher.publish(final_title, final_content, cat_ids, media_id):
                print(f"✅ 发布成功: {final_title}")
                mark_as_posted(item['link'])
            else:
                print(f"❌ 发布失败")
            
            # 适当停顿，防止请求过快
            time.sleep(15)
            
        except Exception as e:
            print(f"⚠️ 处理单条新闻时发生错误: {e}")

if __name__ == "__main__":
    main()