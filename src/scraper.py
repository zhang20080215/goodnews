import feedparser

class Scraper:
    def __init__(self):
        self.sources = {
            "en": ["https://www.goodnewsnetwork.org/category/news/feed/"],
            "zh": ["https://rsshub.app/thepaper/featured"] # 建议替换为更稳定的正能量源
        }

    def fetch_all(self, limit=3):
        news_list = []
        for lang, urls in self.sources.items():
            for url in urls:
                feed = feedparser.parse(url)
                for entry in feed.entries[:limit]:
                    news_list.append({
                        "title": entry.title,
                        "summary": entry.get("summary", ""),
                        "link": entry.link,
                        "lang": lang
                    })
        return news_list