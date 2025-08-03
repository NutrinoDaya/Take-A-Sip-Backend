# app/api/routes/auth.py
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError

from core.security import create_access_token, verify_password, get_password_hash
from db.database import db
from models.token import Token
from models.user import UserCreate, UserViewModel, UserLogin
from api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ... /register endpoint is correct ...
@router.post("/register", response_model=UserViewModel, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_doc = {"email": user.email, "hashed_password": hashed_password, "user_type": user.user_type}
    try:
        new_user = await db.users.insert_one(user_doc)
        created_user = await db.users.find_one({"_id": new_user.inserted_id})
        created_user["_id"] = str(created_user["_id"])
        return created_user
    except DuplicateKeyError:
        logging.warning(f"Registration attempt with existing email: {user.email}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")


# --- THIS IS THE UPDATED LOGIN FUNCTION ---
@router.post("/login", response_model=Token)
async def login(credentials: UserLogin): # Changed from form_data to use the UserLogin model
    # Access credentials via the Pydantic model
    user = await db.users.find_one({"email": credentials.email})
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
    
# ... /me endpoint is correct ...
@router.get("/me")
async def read_users_me(current_user: UserViewModel = Depends(get_current_user)):
    return {
        "uid": str(current_user.id),
        "email": current_user.email,
        "isAdmin": current_user.user_type == 'admin'
    }