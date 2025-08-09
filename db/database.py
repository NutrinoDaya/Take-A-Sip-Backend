# app/db/database.py
import motor.motor_asyncio
import logging
from core.config import settings

# This will raise a clear error during startup if MONGO_DETAILS is invalid,
# which is better than failing silently.
try:
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DETAILS)
    db = client[settings.DATABASE_NAME]
    logging.info("MongoDB client initialized.")
except Exception as e:
    logging.critical(f"Failed to initialize MongoDB client: {e}")
    # Set them to None so the app can still import them, but startup will fail elsewhere
    client = None
    db = None