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
    
    # 安全性检查：如果没有 key，直接返回默认图，不浪费 API 请求
    if not access_key:
        print("⚠️ 未检测到 UNSPLASH_ACCESS_KEY，使用默认图")
        return "https://images.unsplash.com/photo-1499209974431-9dac3adaf477"

    # 关键词清洗：限制为前 3 个词，避免 AI 给的长句子导致搜索失败
    search_query = keywords if keywords else "positivity"
    search_query = ",".join(search_query.split()[:3])
    
    url = f"https://api.unsplash.com/photos/random?query={search_query}&orientation=landscape&client_id={access_key}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            res_data = response.json()
            return res_data['urls']['regular']
        elif response.status_code == 401:
            print("❌ Unsplash 认证失败 (401)，请检查 Access Key")
            return "https://images.unsplash.com/photo-1499209974431-9dac3adaf477"
        else:
            print(f"🖼️ Unsplash API 返回错误: {response.status_code}")
            return "https://images.unsplash.com/photo-1499209974431-9dac3adaf477"
    except Exception as e:
        print(f"🖼️ 获取图片异常: {e}")
        return "https://images.unsplash.com/photo-1499209974431-9dac3adaf477"

def is_posted(url):
    """检查链接是否已发布"""
    if not os.path.exists("processed_urls.txt"):
        return False
    with open("processed_urls.txt", "r", encoding='utf-8') as f:
        # 使用精准匹配，防止子串包含导致误删
        history = f.read().splitlines()
        return url.strip() in history

def mark_as_posted(url):
    """记录已发布的链接"""
    with open("processed_urls.txt", "a", encoding='utf-8') as f:
        f.write(url.strip() + "\n")
        f.flush()

def main():
    # 实例化各个模块
    scraper = Scraper()
    processor = Processor()
    publisher = WordPressPublisher()

    print("🚀 开始自动化任务 (Global English Edition)...")
    
    # 获取新闻：现在参数 limit 已在 scraper.__init__ 中由 config 控制
    news_items = scraper.fetch_all() 
    print(f"📝 总共抓取到 {len(news_items)} 条待处理新闻")
    
    for item in news_items:
        # 即使 scraper 内部去重，main 这里再过一遍双保险
        if is_posted(item['link']):
            print(f"⏭️ 跳过已发布的: {item['title'][:30]}...")
            continue
            
        try:
            print(f"📰 处理新闻: {item['title'][:40]}...")
            
            # 1. AI 处理 (这里现在会接收截断后的 1000 字符，既省钱又精准)
            ai_data = processor.process_with_ai(item)
            
            # 2. 准备发布内容
            final_title = ai_data.get('title', item['title'])
            # 增加来源说明，符合版权友好原则
            final_content = ai_data.get('content', '') + \
                            f'<br><hr><p>Source: <a href="{item["link"]}" target="_blank">Read Original Article</a></p>'
            
            # 3. 获取相关图片
            img_kw = ai_data.get('image_keywords', 'positivity')
            img_url = get_unsplash_image(img_kw)
            print(f"🎨 AI 关键词: '{img_kw}' -> 匹配图片: {img_url}")
            
            # 4. 上传图片到 WP 并获取 ID
            media_id = publisher.upload_image(img_url)
            
            # 5. 处理分类 ID
            cat_ids = ai_data.get('category_id', [2])
            if not isinstance(cat_ids, list):
                cat_ids = [cat_ids]
            
            # 6. 发布到 WordPress
            if publisher.publish(final_title, final_content, cat_ids, media_id):
                print(f"✅ 发布成功: {final_title}")
                mark_as_posted(item['link'])
            else:
                print(f"❌ 发布失败: WordPress 接口未响应")
            
            # 适当停顿，保护 API 频率限制，也让 WP 有喘息时间
            time.sleep(10)
            
        except Exception as e:
            print(f"⚠️ 处理单条新闻时发生错误: {e}")

if __name__ == "__main__":
    main()