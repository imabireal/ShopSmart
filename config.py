import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key-here')
    MONGODB_URL = os.environ.get('MONGODB_URL', 'mongodb://localhost:27017/shop_smart')
