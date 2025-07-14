# main.py
from src.scraper import FacebookScraper
import os

def main():
    # Tạo folder data nếu chưa có
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Khởi tạo scraper
    scraper = FacebookScraper()
    
    # Scrape posts từ trang VnExpress
    print("Đang scrape posts từ VnExpress...")
    scraper.scrape_posts('VnExpress', pages=2)
    
    # Lưu dữ liệu
    scraper.save_to_csv('vnexpress_posts.csv')
    scraper.save_to_json('vnexpress_posts.json')
    
    print("Hoàn thành!")

if __name__ == "__main__":
    main()

