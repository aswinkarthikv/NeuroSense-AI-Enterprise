import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-enterprise-key-do-not-share')
    
    # SQLite Configuration map
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "neurosense_enterprise.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Storage Configuration
    STORAGE_PATH = os.path.join(BASE_DIR, 'storage')
    MEDIA_AUDIO_PATH = os.path.join(STORAGE_PATH, 'audio')
    MEDIA_VIDEO_PATH = os.path.join(STORAGE_PATH, 'video')
    MEDIA_IMAGE_PATH = os.path.join(STORAGE_PATH, 'images')
    REPORTS_PATH = os.path.join(STORAGE_PATH, 'reports')
    
    # Upload limits
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB max upload
    
    @staticmethod
    def init_app(app):
        # Create necessary directories
        os.makedirs(Config.MEDIA_AUDIO_PATH, exist_ok=True)
        os.makedirs(Config.MEDIA_VIDEO_PATH, exist_ok=True)
        os.makedirs(Config.MEDIA_IMAGE_PATH, exist_ok=True)
        os.makedirs(Config.REPORTS_PATH, exist_ok=True)
