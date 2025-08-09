# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # --- MongoDB Settings ---
    # This MUST be set in your Render environment variables
    MONGO_DETAILS: str 
    DATABASE_NAME: str = "caffe_app"
    
    # --- JWT Settings ---
    # Generate a strong secret for Render: openssl rand -hex 32
    SECRET_KEY: str = "a_very_secret_key_for_local_development"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # --- Cloudinary Settings ---
    # These MUST be set in your Render environment variables
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    class Config:
        # For local development, it will read from a .env file
        env_file = ".env"

# Create a single instance of settings to be used throughout the app
settings = Settings()