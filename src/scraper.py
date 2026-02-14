import feedparser
import requests

class Scraper:
    def __init__(self):
        # 💡 精选 5 个高质量英文正能量源
        self.sources = [
            "https://www.goodnewsnetwork.org/category/news/feed/",
            "https://www.positive.news/feed/",
            "https://www.optimistdaily.com/feed/",
            "https://reasonstobecheerful.world/feed/",
            "https://www.goodgoodgood.co/feed/"
        ]

    def fetch_all(self, limit=3):
        news_list = []
        headers = {'User-Agent': 'Mozilla/5.0'}
        for url in self.sources:
            try:
                print(f"🔍 Scraping: {url}")
                resp = requests.get(url, headers=headers, timeout=15)
                if resp.status_code == 200:
                    feed = feedparser.parse(resp.content)
                    for entry in feed.entries[:limit]:
                        news_list.append({
                            "title": entry.title,
                            "summary": entry.get("summary", ""),
                            "link": entry.link
                        })
            except Exception as e:
                print(f"⚠️ Failed to fetch {url}: {e}")
        return news_list