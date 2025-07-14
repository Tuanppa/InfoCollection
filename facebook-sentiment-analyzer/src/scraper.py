# src/scraper.py
from facebook_scraper import get_posts
import pandas as pd
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class FacebookScraper:
    def __init__(self):
        self.posts_data = []
    
    def scrape_posts(self, page_name, pages=5):
        """
        Scrape posts from a Facebook page
        """
        try:
            posts = get_posts(
                page_name,
                pages=pages,
                extra_info=True,
                youtube_dl=False
            )
            
            for post in posts:
                post_data = {
                    'post_id': post.get('post_id'),
                    'text': post.get('text', ''),
                    'time': post.get('time'),
                    'likes': post.get('likes', 0),
                    'comments': post.get('comments', 0),
                    'shares': post.get('shares', 0),
                    'images': post.get('images', []),
                    'video': post.get('video'),
                    'post_url': post.get('post_url'),
                    'page_name': page_name
                }
                self.posts_data.append(post_data)
                
                # In thông tin post
                print(f"Post ID: {post_data['post_id']}")
                print(f"Text: {post_data['text'][:100]}...")
                print(f"Likes: {post_data['likes']}")
                print("-" * 50)
                
        except Exception as e:
            print(f"Error scraping {page_name}: {str(e)}")
    
    def save_to_csv(self, filename='facebook_posts.csv'):
        """
        Save scraped data to CSV
        """
        df = pd.DataFrame(self.posts_data)
        df.to_csv(f'data/{filename}', index=False, encoding='utf-8')
        print(f"Data saved to data/{filename}")
    
    def save_to_json(self, filename='facebook_posts.json'):
        """
        Save scraped data to JSON
        """
        with open(f'data/{filename}', 'w', encoding='utf-8') as f:
            json.dump(self.posts_data, f, ensure_ascii=False, indent=2, default=str)
        print(f"Data saved to data/{filename}")

# Sử dụng
if __name__ == "__main__":
    scraper = FacebookScraper()
    
    # Scrape posts from a public page
    scraper.scrape_posts('VnExpress', pages=2)
    
    # Save data
    scraper.save_to_csv()
    scraper.save_to_json()

