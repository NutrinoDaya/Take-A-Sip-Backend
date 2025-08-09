from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Form
import cloudinary.uploader

from api.deps import get_current_admin
from db.database import db
from models.food import FoodItem, Image

router = APIRouter(prefix="/food", tags=["Food Items"])


@router.get("/", response_model=List[FoodItem])
async def get_food_items():
    items = await db.food_items.find().to_list(100)
    for item in items:
        item["_id"] = str(item["_id"])
    return items


@router.post("/add", response_model=FoodItem, dependencies=[Depends(get_current_admin)])
async def add_food_item(
    name: str = Form(...),
    description: str = Form(...),
    # ⭐️ FIX #1: Accept the price as a string to match the form data
    price: str = Form(...),
    section: str = Form(...),
    file: UploadFile = File(...)
):
    # 1. Upload the file to Cloudinary
    upload_result = cloudinary.uploader.upload(
        file.file,
        folder="take_a_sip_food_items"
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
        # ⭐️ FIX #2: Convert the price string to a float before saving
        "price": float(price),
        "section": section,
        "image": image_data.dict()
    }
    
    # 4. Insert into MongoDB
    new_item = await db.food_items.insert_one(item_doc)
    created_item = await db.food_items.find_one({"_id": new_item.inserted_id})
    created_item["_id"] = str(created_item["_id"])
    
    return created_item