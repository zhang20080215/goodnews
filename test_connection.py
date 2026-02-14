from src.publisher import WordPressPublisher
from dotenv import load_dotenv
import os

def test():
    print("Testing connection to WordPress...")
    publisher = WordPressPublisher()
    
    test_title = "Connection Test from Local Bot"
    test_content = """
    <h2>This is a test post</h2>
    <p>If you see this, your local Python environment can successfully talk to your Cloudways WordPress site via API.</p>
    <p>Good news is on the way!</p>
    """
    # 建议先发到分类ID 1，或者你查到的任何一个ID
    # 如果不知道ID，可以先传空列表 []
    test_category_ids = [] 

    result = publisher.publish(
        title=test_title,
        content=test_content,
        category_ids=test_category_ids,
        status='draft'  # 测试建议用 draft（草稿），不破坏前端页面
    )

    if result:
        print(f"Test Successful! Post ID: {result.get('id')}")
        print(f"Check your WP dashboard: {os.getenv('WP_SITE_URL')}/wp-admin/edit.php")
    else:
        print("Test Failed. Please check your .env credentials and Cloudways settings.")

if __name__ == "__main__":
    test()