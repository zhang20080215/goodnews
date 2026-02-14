import feedparser
import requests
import re
import os
# 确保这一行导入了配置
from config import NEWS_SOURCES, FETCH_LIMIT_PER_SOURCE, HISTORY_FILE

class Scraper:
    def __init__(self):
        # 👇 确保下面这些行前面有 8 个空格（或 2 个 Tab）
        self.sources = NEWS_SOURCES
        self.limit = FETCH_LIMIT_PER_SOURCE
        self.history_file = HISTORY_FILE
        self.processed_urls = self._load_history()

    def _load_history(self):
        """加载已处理的 URL"""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return set(line.strip() for line in f if line.strip())
        return set()

    # ... 其他函数也要保持正确的缩进层级

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