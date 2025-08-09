# app/main.py
import logging
import uvicorn
import os
import cloudinary
from fastapi import FastAPI
from contextlib import asynccontextmanager

# Import your settings object and routers
from core.config import settings
from api.routes import auth, food
# Import the client and db objects from your database module
from db.database import db, client

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- This block runs once on application startup ---
    logging.info("Application startup...")

    # Configure Cloudinary
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_CLOUD_NAME,
        api_key=settings.CLOUDINARY_API_KEY,
        api_secret=settings.CLOUDINARY_API_SECRET,
    )
    logging.info("Cloudinary has been configured.")

    # Create database indexes
    if db is not None:
        await db.users.create_index("email", unique=True)
        logging.info("Database indexes created successfully.")
    else:
        logging.error("Database not available, skipping index creation.")
    
    yield # The application runs after this yield
    
    # --- This block runs once on application shutdown ---
    if client is not None:
        client.close()
        logging.info("MongoDB connection closed.")
    logging.info("Application shutdown complete.")

app = FastAPI(title="Caffe App API", lifespan=lifespan)

# Include routers
app.include_router(auth.router)
app.include_router(food.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Caffe App API!"}

# For local testing
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)