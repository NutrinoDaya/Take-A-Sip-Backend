# app/main.py
import logging
import uvicorn
import os
import cloudinary
from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.config import settings
from api.routes import auth, food
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

    # Ping the database to verify connection
    try:
        await client.admin.command('ping')
        logging.info("Successfully connected to MongoDB.")
        # Create database indexes
        await db.users.create_index("email", unique=True)
        logging.info("Database indexes created successfully.")
    except Exception as e:
        logging.critical(f"Could not connect to MongoDB during startup: {e}")

    yield # The application runs after this yield

    # --- This block runs once on application shutdown ---
    client.close()
    logging.info("MongoDB connection closed. Application shutdown complete.")

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