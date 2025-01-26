from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    MONGO_URI = os.getenv("MONGO_URI")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")  # Valor padrão: localhost
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))  # Valor padrão: 6379
    FLASK_ENV = os.getenv("FLASK_ENV", "production")
