# src/selenium_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from dotenv import load_dotenv
import os

load_dotenv()

class FacebookSeleniumScraper:
    def __init__(self):
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """
        Setup Chrome driver
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Headless mode (tùy chọn)
        # chrome_options.add_argument('--headless')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def login(self):
        """
        Login to Facebook (cần cẩn thận với policy)
        """
        email = os.getenv('FACEBOOK_EMAIL')
        password = os.getenv('FACEBOOK_PASSWORD')
        
        if not email or not password:
            print("Please set FACEBOOK_EMAIL and FACEBOOK_PASSWORD in .env file")
            return False
        
        self.driver.get('https://www.facebook.com')
        
        # Wait and find email input
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(email)
        
        # Find password input
        password_input = self.driver.find_element(By.ID, "pass")
        password_input.send_keys(password)
        
        # Click login
        login_button = self.driver.find_element(By.NAME, "login")
        login_button.click()
        
        # Wait for login to complete
        time.sleep(5)
        return True
    
    def scrape_page_posts(self, page_url, max_posts=10):
        """
        Scrape posts from a Facebook page
        """
        self.driver.get(page_url)
        time.sleep(3)
        
        posts = []
        post_elements = []
        
        # Scroll to load more posts
        for i in range(max_posts // 5):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
        
        # Find post elements
        post_elements = self.driver.find_elements(By.CSS_SELECTOR, '[data-pagelet="FeedUnit_0"]')
        
        for idx, post_element in enumerate(post_elements[:max_posts]):
            try:
                # Extract post text
                try:
                    text_element = post_element.find_element(By.CSS_SELECTOR, '[data-ad-preview="message"]')
                    text = text_element.text
                except:
                    text = ""
                
                # Extract reactions
                try:
                    reactions = post_element.find_element(By.CSS_SELECTOR, '[aria-label*="reaction"]').text
                except:
                    reactions = "0"
                
                post_data = {
                    'index': idx,
                    'text': text,
                    'reactions': reactions,
                    'timestamp': time.time()
                }
                
                posts.append(post_data)
                print(f"Post {idx+1}: {text[:50]}...")
                
            except Exception as e:
                print(f"Error extracting post {idx}: {str(e)}")
        
        return posts
    
    def close(self):
        """
        Close the browser
        """
        if self.driver:
            self.driver.quit()

# Sử dụng
if __name__ == "__main__":
    scraper = FacebookSeleniumScraper()
    
    try:
        # Login (tùy chọn)
        # scraper.login()
        
        # Scrape posts
        posts = scraper.scrape_page_posts('https://www.facebook.com/vnexpress', max_posts=5)
        
        # Save data
        with open('data/selenium_posts.json', 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        
        print(f"Scraped {len(posts)} posts")
        
    finally:
        scraper.close()