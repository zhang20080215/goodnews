import os
import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from dotenv import load_dotenv
from config import CATEGORIES
from src.scraper import Scraper
from src.processor import Processor
from src.publisher import WordPressPublisher

# 加载环境变量
load_dotenv()

# --- 邮件配置 ---
GMAIL_USER = "zhang20080215@gmail.com"
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_notification(new_count):
    """任务完成后发送统计邮件"""
    if not GMAIL_APP_PASSWORD:
        print("📧 跳过邮件发送：环境变量 GMAIL_APP_PASSWORD 未配置")
        return

    # 计算 processed_urls.txt 中的总行数
    total_count = 0
    if os.path.exists("processed_urls.txt"):
        with open("processed_urls.txt", "r", encoding='utf-8') as f:
            total_count = len([line for line in f if line.strip()])

    subject = "Good News 自动化任务报告"
    content = (
        f"Hi Editor,\n\n"
        f"自动化脚本执行完毕，统计如下：\n"
        f"✅ 本次新增文章数量：{new_count}\n"
        f"📊 网站累计文章数量：{total_count}\n"
        f"⏰ 执行时间 (UTC): {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        f"祝你有美好的一天！"
    )

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER
    msg['Subject'] = Header(subject, 'utf-8')

    try:
        # 使用 Gmail SSL 端口
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, [GMAIL_USER], msg.as_string())
        print("📧 邮件报告已发送成功！")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")

# --- 原有辅助函数保持不变 ---
def get_unsplash_image(keywords):
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    if not access_key: return "https://images.unsplash.com/photo-1499209974431-9dac3adaf477"
    search_query = ",".join((keywords if keywords else "positivity").split()[:3])
    url = f"https://api.unsplash.com/photos/random?query={search_query}&orientation=landscape&client_id={access_key}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200: return response.json()['urls']['regular']
        return "https://images.unsplash.com/photo-1499209974431-9dac3adaf477"
    except: return "https://images.unsplash.com/photo-1499209974431-9dac3adaf477"

def is_posted(url):
    if not os.path.exists("processed_urls.txt"): return False
    with open("processed_urls.txt", "r", encoding='utf-8') as f:
        return url.strip() in f.read().splitlines()

def mark_as_posted(url):
    with open("processed_urls.txt", "a", encoding='utf-8') as f:
        f.write(url.strip() + "\n")
        f.flush()

def main():
    scraper = Scraper()
    processor = Processor()
    publisher = WordPressPublisher()
    
    new_post_count = 0 # 🌟 初始化本次新增计数器
    print("🚀 开始自动化任务 (Global English Edition)...")
    
    news_items = scraper.fetch_all() 
    print(f"📝 总共抓取到 {len(news_items)} 条待处理新闻")
    
    for item in news_items:
        if is_posted(item['link']):
            print(f"⏭️ 跳过已发布的: {item['title'][:30]}...")
            continue
            
        try:
            print(f"📰 处理新闻: {item['title'][:40]}...")
            ai_data = processor.process_with_ai(item)
            final_title = ai_data.get('title', item['title'])
            final_content = ai_data.get('content', '') + f'<br><hr><p>Source: <a href="{item["link"]}" target="_blank">Read Original</a></p>'
            
            img_kw = ai_data.get('image_keywords', 'positivity')
            img_url = get_unsplash_image(img_kw)
            media_id = publisher.upload_image(img_url)
            
            cat_ids = ai_data.get('category_id', [2])
            if not isinstance(cat_ids, list): cat_ids = [cat_ids]
            
            if publisher.publish(final_title, final_content, cat_ids, media_id):
                print(f"✅ 发布成功: {final_title}")
                mark_as_posted(item['link'])
                new_post_count += 1 # 🌟 成功发布后计数自增
            
            time.sleep(10)
        except Exception as e:
            print(f"⚠️ 处理单条新闻时发生错误: {e}")

    # 🌟 循环结束后，发送邮件统计
    send_notification(new_post_count)

if __name__ == "__main__":
    main()