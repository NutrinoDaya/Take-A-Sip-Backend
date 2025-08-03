# app/api/routes/food.py
from typing import List
from fastapi import APIRouter, Depends

from api.deps import get_current_admin
from db.database import db
from models.food import FoodItem, FoodItemCreate

router = APIRouter(prefix="/food", tags=["Food Items"])

@router.get("/", response_model=List[FoodItem])
async def get_food_items():
    items = await db.food_items.find().to_list(100)
    for item in items:
        item["_id"] = str(item["_id"])
    return items

@router.post("/add", response_model=FoodItem, dependencies=[Depends(get_current_admin)])
async def add_food_item(item: FoodItemCreate):
    item_doc = item.dict()
    new_item = await db.food_items.insert_one(item_doc)
    created_item = await db.food_items.find_one({"_id": new_item.inserted_id})
    created_item["_id"] = str(created_item["_id"])
    return created_item