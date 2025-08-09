# app/models/food.py
from pydantic import BaseModel, Field
from .user import PyObjectId

# New nested model for structured image data
class Image(BaseModel):
    public_id: str
    url: str

class FoodItem(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    description: str
    price: float
    section: str
    image: Image # Use the nested Image model

# This model is no longer needed for creation, as data will come from a form.
# We keep it for reference or other potential uses.
class FoodItemCreate(BaseModel):
    name: str
    description: str
    price: float
    section: str
    image: Image