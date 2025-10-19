# backend/config.py

import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    # ==============================================================
    # Flask Core
    # ==============================================================
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")

    # ==============================================================
    # Database (PostgreSQL)
    # ==============================================================
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER', 'postgres')}:"
        f"{os.getenv('POSTGRES_PASSWORD', 'postgres')}@"
        f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
        f"{os.getenv('POSTGRES_PORT', '5432')}/"
        f"{os.getenv('POSTGRES_DB', 'analytics')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==============================================================
    # JWT Authentication
    # ==============================================================
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-jwt-secret")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_SEC", 1800))  # 30 minutes
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 7))
    )

    # ==============================================================
    # Flask-Mail (SMTP)
    # ==============================================================
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() in ("true", "1", "yes")
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "False").lower() in ("true", "1", "yes")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

    # ==============================================================
    # Redis (shared between Flask-Caching and Celery)
    # ==============================================================
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Flask-Caching
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = REDIS_URL

    # ==============================================================
    # Celery (for background jobs)
    # ==============================================================
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_TASK_TRACK_STARTED = True
    CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes timeout per task

    # ==============================================================
    # ClickHouse (analytics DB)
    # ==============================================================
    CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
    CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", 9000))  # 9000 → native protocol
    CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
    CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")
    CLICKHOUSE_DATABASE = os.getenv("CLICKHOUSE_DATABASE", "analytics")

    # ==============================================================
    # AWS S3 (for archived PDF storage)
    # ==============================================================
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")
    AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

    # ==============================================================
    # Other optional integrations
    # ==============================================================
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
