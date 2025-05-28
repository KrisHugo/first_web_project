import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    # 基础配置
    BASE_DIR = Path(__file__).parent.parent
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-123')
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',  'mysql+pymysql://root:123456@localhost/test_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-456')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_EXPIRES', 3600))  # 1小时
    
    # 文件上传
    UPLOAD_FOLDER = BASE_DIR / 'app' / 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

    @staticmethod
    def init_app(app):
        # 确保上传目录存在
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)