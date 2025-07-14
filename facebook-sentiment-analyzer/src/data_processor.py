# src/data_processor.py
import pandas as pd
import json
from datetime import datetime

class DataProcessor:
    def __init__(self, data_file):
        self.data_file = data_file
        self.df = None
        self.load_data()
    
    def load_data(self):
        """
        Load data from CSV or JSON
        """
        if self.data_file.endswith('.csv'):
            self.df = pd.read_csv(self.data_file)
        elif self.data_file.endswith('.json'):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.df = pd.DataFrame(data)
    
    def clean_data(self):
        """
        Clean and preprocess data
        """
        # Xóa posts trống
        self.df = self.df.dropna(subset=['text'])
        
        # Xóa duplicates
        self.df = self.df.drop_duplicates(subset=['text'])
        
        # Convert time to datetime
        if 'time' in self.df.columns:
            self.df['time'] = pd.to_datetime(self.df['time'])
        
        print(f"Cleaned data: {len(self.df)} posts")
    
    def basic_stats(self):
        """
        Show basic statistics
        """
        print("\n=== BASIC STATISTICS ===")
        print(f"Total posts: {len(self.df)}")
        print(f"Average likes: {self.df['likes'].mean():.2f}")
        print(f"Average comments: {self.df['comments'].mean():.2f}")
        print(f"Average shares: {self.df['shares'].mean():.2f}")
        
        # Top posts by engagement
        self.df['engagement'] = self.df['likes'] + self.df['comments'] + self.df['shares']
        top_posts = self.df.nlargest(5, 'engagement')
        
        print("\n=== TOP 5 POSTS BY ENGAGEMENT ===")
        for idx, post in top_posts.iterrows():
            print(f"Engagement: {post['engagement']}")
            print(f"Text: {post['text'][:100]}...")
            print("-" * 30)
    
    def export_cleaned_data(self, filename='cleaned_data.csv'):
        """
        Export cleaned data
        """
        self.df.to_csv(f'data/{filename}', index=False, encoding='utf-8')
        print(f"Cleaned data saved to data/{filename}")

# Sử dụng
if __name__ == "__main__":
    processor = DataProcessor('data/vnexpress_posts.csv')
    processor.clean_data()
    processor.basic_stats()
    processor.export_cleaned_data()