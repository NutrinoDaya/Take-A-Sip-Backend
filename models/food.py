# app/models/food.py
from pydantic import BaseModel, Field
from .user import PyObjectId

class FoodItem(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    price: float
    section: str
    image: str

class FoodItemCreate(BaseModel):
    name: str
    description: str
    price: float
    section: str
    image: str