from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    API_KEY = os.getenv('API_KEY', 'your_default_api_key')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    AUDIO_EXPIRY_TIME = 864000  # 10 days in seconds

    @staticmethod
    def init_app(app):
        pass