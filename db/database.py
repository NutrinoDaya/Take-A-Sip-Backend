# app/db/database.py
import motor.motor_asyncio
from core.config import settings

# Initialize the client directly.
# If the MONGO_DETAILS are invalid, this will raise an error and crash the app on startup,
# which is the correct behavior. This prevents the app from running without a database.
client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_DETAILS)

# Get a reference to the database
db = client[settings.DATABASE_NAME]