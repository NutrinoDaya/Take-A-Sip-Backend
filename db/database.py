# app/db/database.py
import motor.motor_asyncio
import logging
from core.config import settings

try:
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DETAILS)
    db = client[settings.DATABASE_NAME]
    
    # Ensure indexes are created for performance and constraints
    async def create_indexes():
        await db.users.create_index("email", unique=True)
        logging.info("Indexes created successfully.")

    logging.info("Successfully connected to MongoDB.")
except Exception as e:
    logging.critical(f"Could not connect to MongoDB: {e}")
    client = None
    db = None