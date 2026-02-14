import feedparser
import requests # 引入 requests 来手动控制请求头

class Scraper:
    def __init__(self):
        self.sources = {
            "en": ["https://www.goodnewsnetwork.org/category/news/feed/"],
            "zh": ["https://www.thepaper.cn/rss_pms.jsp"] 
        }

    def fetch_all(self, limit=3):
        news_list = []
        # 💡 伪装成真实的浏览器访问
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        for lang, urls in self.sources.items():
            for url in urls:
                try:
                    print(f"🔍 尝试抓取: {url}")
                    # 💡 先用 requests 抓取内容，再交给 feedparser 解析
                    response = requests.get(url, headers=headers, timeout=15)
                    
                    if response.status_code == 200:
                        feed = feedparser.parse(response.content)
                        print(f"📊 成功！抓取到 {len(feed.entries)} 条新闻")
                        
                        for entry in feed.entries[:limit]:
                            news_list.append({
                                "title": entry.title,
                                "summary": entry.get("summary", ""),
                                "link": entry.link,
                                "lang": lang
                            })
                    else:
                        print(f"❌ 抓取失败，状态码: {response.status_code}")
                except Exception as e:
                    print(f"⚠️ 出错: {e}")
                    
        return news_list