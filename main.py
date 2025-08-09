# app/main.py
import logging
import uvicorn
import os
import cloudinary # Import the cloudinary library
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import your settings object and routers
from core.config import settings
from api.routes import auth, food
from db.database import client, create_indexes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- This block runs once on application startup ---
    logging.info("Application startup...")

    # Configure Cloudinary using the settings loaded from the environment
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
    )
    logging.info("Cloudinary has been configured.")

    await create_indexes()
    
    yield # The application runs after this yield
    
    # --- This block runs once on application shutdown ---
    client.close()
    logging.info("MongoDB connection closed. Application shutdown complete.")

app = FastAPI(title="Caffe App API", lifespan=lifespan)

# Include routers from the api directory
app.include_router(auth.router)
app.include_router(food.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Caffe App API!"}

# This block allows you to run the server directly for local testing
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)