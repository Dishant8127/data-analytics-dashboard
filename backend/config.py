
# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # -----------------------------
    # Flask settings
    # -----------------------------
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")

    # -----------------------------
    # Database settings
    # -----------------------------
    SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRES_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -----------------------------
    # JWT settings
    # -----------------------------
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-jwt-secret")

    # Access tokens → short-lived (default: 30 min, overridable via env)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_SEC", 1800))  # 1800s = 30 min
    )

    # Refresh tokens → long-lived (default: 7 days)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 7))
    )
    
    # -----------------------------
    # Email (SMTP) settings
    # -----------------------------
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "1") == "1"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")  # your email
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")  # app password
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "dishantpatel927@gmail.com")

    # Redis (shared between Flask-Caching and Celery)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Celery
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL