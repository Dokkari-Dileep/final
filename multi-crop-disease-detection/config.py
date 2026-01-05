import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # EmailJS Configuration
    EMAILJS_USER_ID = os.getenv('EMAILJS_USER_ID')
    EMAILJS_SERVICE_ID = os.getenv('EMAILJS_SERVICE_ID')
    EMAILJS_TEMPLATE_ID = os.getenv('EMAILJS_TEMPLATE_ID')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@example.com')
    
    # Model Configuration
    MODEL_PATH = 'model/disease_model.h5'
    IMG_SIZE = (224, 224)
    
    # Application Configuration
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    SUPPORTED_CROPS = [
        'Apple', 'Tomato', 'Potato', 'Grape', 'Corn', 'Cherry',
        'Strawberry', 'Peach', 'Pepper', 'Watermelon', 'Pomegranate',
        'Eggplant', 'Custard Apple', 'Lemon'
    ]