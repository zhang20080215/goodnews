import requests
from requests.auth import HTTPBasicAuth
import os

class WordPressPublisher:
    def __init__(self):
        self.base_url = os.getenv('WP_SITE_URL')
        self.user = os.getenv('WP_USERNAME')
        self.password = os.getenv('WP_APP_PASSWORD')

    def upload_image(self, image_url):
        """下载远程图片并上传到 WP 媒体库"""
        try:
            # 1. 下载图片
            img_data = requests.get(image_url).content
            # 2. 上传到 WP
            headers = {
                'Content-Disposition': 'attachment; filename=featured_image.jpg',
                'Content-Type': 'image/jpeg'
            }
            res = requests.post(
                f"{self.base_url}/wp-json/wp/v2/media",
                headers=headers,
                data=img_data,
                auth=HTTPBasicAuth(self.user, self.password)
            )
            return res.json().get('id') if res.status_code == 201 else None
        except:
            return None

    def publish(self, title, content, category_ids, featured_media_id=None):
        payload = {
            "title": title,
            "content": content,
            "status": "publish",
            "categories": category_ids
        }
        if featured_media_id:
            payload["featured_media"] = featured_media_id

        res = requests.post(
            f"{self.base_url}/wp-json/wp/v2/posts",
            json=payload,
            auth=HTTPBasicAuth(self.user, self.password)
        )
        return res.status_code == 201