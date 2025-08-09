# app/api/routes/food.py
import os
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Form
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

from api.deps import get_current_admin
from db.database import db
from models.food import FoodItem, Image

# Load environment variables from .env file
load_dotenv()

router = APIRouter(prefix="/food", tags=["Food Items"])

# --- Cloudinary Configuration ---
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)


@router.get("/", response_model=List[FoodItem])
async def get_food_items():
    items = await db.food_items.find().to_list(100)
    for item in items:
        item["_id"] = str(item["_id"])
    return items


@router.post("/add", response_model=FoodItem, dependencies=[Depends(get_current_admin)])
async def add_food_item(
    # Receive all data as form fields instead of a JSON body
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    section: str = Form(...),
    file: UploadFile = File(...)
):
    # 1. Upload the file to Cloudinary
    upload_result = cloudinary.uploader.upload(
        file.file,
        folder="take_a_sip_food_items" # Optional: organizes uploads in Cloudinary
    )
    
    # 2. Create the image data object for our database
    image_data = Image(
        public_id=upload_result.get("public_id"),
        url=upload_result.get("secure_url")
    )

    # 3. Create the full food item document
    item_doc = {
        "name": name,
        "description": description,
        "price": price,
        "section": section,
        "image": image_data.dict() # Store the nested image object
    }
    
    # 4. Insert into MongoDB
    new_item = await db.food_items.insert_one(item_doc)
    created_item = await db.food_items.find_one({"_id": new_item.inserted_id})
    created_item["_id"] = str(created_item["_id"])
    
    return created_item