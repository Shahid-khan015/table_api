import os
from pathlib import Path

class Config:
    """Application configuration"""
    STATIC_FOLDER = os.path.join(os.getcwd(), 'static')
    ALLOWED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Ensure static folder exists
    Path(STATIC_FOLDER).mkdir(parents=True, exist_ok=True)