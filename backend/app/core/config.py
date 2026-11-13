# backend/app/core/config.py
import os
from typing import Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    # SQLite for local verification; replace with PostgreSQL URL in production
    DATABASE_URL: str = Field('sqlite:///./test.db', env='DATABASE_URL')
    JWT_SECRET: str = Field('testsecret', env='JWT_SECRET')
    CORS_ORIGINS: str = Field('http://localhost:5173', env='CORS_ORIGINS')
    STORAGE_ROOT: str = Field('storage', env='STORAGE_ROOT')
    MAX_UPLOAD_SIZE: int = Field(500 * 1024 * 1024, env='MAX_UPLOAD_SIZE')  # 500 MB
    OPENAI_API_KEY: str = Field(default="", env='OPENAI_API_KEY')
    HF_TOKEN: str = Field(default="", env='HF_TOKEN')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
