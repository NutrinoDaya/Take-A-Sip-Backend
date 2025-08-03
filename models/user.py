# app/models/user.py
from pydantic import BaseModel, Field
from pydantic_core import core_schema
from bson import ObjectId
from typing import Any

# --- THIS IS THE CORRECTED HELPER CLASS ---
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        """
        This method is essential for Pydantic v2. It defines how to:
        1. Validate data coming into the model (from a string or an existing ObjectId).
        2. Serialize data going out of the model (turning ObjectId into a string).
        """
        def validate_from_str(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return ObjectId(value)

        # Schema for converting a string to an ObjectId
        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            # For JSON data (like in a request body), expect a string.
            json_schema=from_str_schema,
            # For Python data (like from the DB), accept an existing ObjectId or a string.
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    from_str_schema,
                ]
            ),
            # When serializing to JSON, always convert the ObjectId to a string.
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )


class UserBase(BaseModel):
    email: str
    user_type: str = "user"

class UserCreate(UserBase):
    password: str

# ADD THIS NEW MODEL FOR LOGIN
class UserLogin(BaseModel):
    email: str
    password: str

class UserInDB(UserBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hashed_password: str

class UserViewModel(BaseModel):
    id: str = Field(alias="_id")
    email: str
    user_type: str