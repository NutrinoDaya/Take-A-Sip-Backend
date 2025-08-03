# app/core/config.py
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # For Render, set this in your environment variables.
    MONGO_DETAILS: str = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
    DATABASE_NAME: str = "caffe_app"
    
    # For Render, generate a strong secret and set it as an environment variable.
    # You can generate one with: openssl rand -hex 32
    SECRET_KEY: str = os.getenv("SECRET_KEY", "a_very_secret_key_that_should_be_changed")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env" # Optional: for local development with a .env file

settings = Settings()