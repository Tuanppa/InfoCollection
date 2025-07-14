import os

def create_project_structure():
    # Tên project
    project_name = "facebook-sentiment-analyzer"
    
    # Cấu trúc folders
    folders = [
        "src",
        "data",
        "models", 
        "config",
        "logs",
        "tests"
    ]
    
    # Cấu trúc files
    files = {
        "src": ["__init__.py", "scraper.py", "analyzer.py", "utils.py", "config.py"],
        "config": ["settings.py", "database.py"],
        "tests": ["__init__.py", "test_scraper.py", "test_analyzer.py"],
        "": ["requirements.txt", ".env", ".gitignore", "README.md", "main.py", "setup.py"]
    }
    
    # Tạo folder chính
    if not os.path.exists(project_name):
        os.makedirs(project_name)
        print(f"✅ Đã tạo folder: {project_name}")
    
    # Chuyển vào folder chính
    os.chdir(project_name)
    
    # Tạo các folder con
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"✅ Đã tạo folder: {folder}")
    
    # Tạo các file
    for folder, file_list in files.items():
        for file_name in file_list:
            file_path = os.path.join(folder, file_name) if folder else file_name
            
            if not os.path.exists(file_path):
                # Tạo file với nội dung mặc định
                with open(file_path, 'w', encoding='utf-8') as f:
                    if file_name.endswith('.py'):
                        f.write(f'"""\n{file_name}\n"""\n\n')
                    elif file_name == 'requirements.txt':
                        f.write(get_requirements_content())
                    elif file_name == '.gitignore':
                        f.write(get_gitignore_content())
                    elif file_name == 'README.md':
                        f.write(get_readme_content())
                    elif file_name == '.env':
                        f.write(get_env_content())
                    else:
                        f.write('')
                
                print(f"✅ Đã tạo file: {file_path}")
    
    print(f"\n🎉 Hoàn thành! Project structure đã được tạo trong folder: {project_name}")
    print("\n📁 Cấu trúc project:")
    print_directory_structure(".", "")

def get_requirements_content():
    return """requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.15.2
facebook-scraper==0.2.59
pandas==2.1.3
numpy==1.24.3
python-dotenv==1.0.0
pillow==10.1.0
opencv-python==4.8.1.78
transformers==4.35.2
torch==2.1.1
matplotlib==3.8.2
jupyter==1.0.0
webdriver-manager==4.0.1
scikit-learn==1.3.2
nltk==3.8.1
textblob==0.17.1
"""

def get_gitignore_content():
    return """# Environment
.env
venv/
env/
__pycache__/
*.pyc
*.pyo
*.pyd

# Data
data/
*.db
*.csv
*.json
*.xlsx

# Models
models/
*.pkl
*.model
*.pt
*.pth

# Logs
logs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Jupyter
.ipynb_checkpoints/

# Distribution
dist/
build/
*.egg-info/
"""

def get_readme_content():
    return """# Facebook Sentiment Analyzer

## Mô tả
Dự án phân tích sentiment cho các bài viết trên Facebook sử dụng AI và Machine Learning.

## Tính năng
- Thu thập dữ liệu từ Facebook
- Phân tích sentiment văn bản
- Phân tích hình ảnh  
- Báo cáo và visualize kết quả

## Cài đặt
```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\\Scripts\\activate
# Mac/Linux:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

## Sử dụng
```bash
python main.py
```

## Cấu trúc project
```
facebook-sentiment-analyzer/
├── src/          # Source code
├── data/         # Dữ liệu
├── models/       # AI models
├── config/       # Cấu hình
├── tests/        # Unit tests
└── logs/         # Log files
```

## Lưu ý
- Tuân thủ Terms of Service của Facebook
- Chỉ sử dụng cho mục đích học tập/nghiên cứu
"""

def get_env_content():
    return """# Facebook credentials
FACEBOOK_EMAIL=your_email@example.com
FACEBOOK_PASSWORD=your_password
FACEBOOK_ACCESS_TOKEN=your_access_token

# Database
DATABASE_URL=sqlite:///facebook_data.db

# API Keys
OPENAI_API_KEY=your_openai_key
HUGGING_FACE_API_KEY=your_hf_key

# Settings
DEBUG=True
LOG_LEVEL=INFO
MAX_POSTS=100
"""

def print_directory_structure(rootdir, indent):
    """In cấu trúc thư mục"""
    for item in sorted(os.listdir(rootdir)):
        if item.startswith('.'):
            continue
        item_path = os.path.join(rootdir, item)
        if os.path.isdir(item_path):
            print(f"{indent}📁 {item}/")
            print_directory_structure(item_path, indent + "  ")
        else:
            print(f"{indent}📄 {item}")

if __name__ == "__main__":
    create_project_structure()