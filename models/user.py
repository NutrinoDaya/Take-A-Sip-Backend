# app/models/user.py
from pydantic import BaseModel, Field
from pydantic_core import core_schema
from bson import ObjectId

# Helper for handling MongoDB's '_id'
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler) -> core_schema.CoreSchema:
        def validate(v: str) -> ObjectId:
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            return ObjectId(v)
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(validate),
            json_schema=core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

class UserBase(BaseModel):
    email: str
    user_type: str = "user"

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str

class UserViewModel(BaseModel):
    id: str = Field(alias="_id")
    email: str
    user_type: str


# ADD THIS NEW MODEL FOR LOGIN
class UserLogin(BaseModel):
    email: str
    password: str

