from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Database.database import get_db
from Database.models import User
from pydantic import BaseModel
from datetime import datetime

load_dotenv()

router = APIRouter(tags=["user"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

# Pydantic model for creating user
class CreateUser(BaseModel):
    email: str
    name: str

# Pydantic model for user response
class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=UserResponse)
async def create_user(user: CreateUser, db: AsyncSession = Depends(get_db)):
    try:
        # Check if user exists
        result = await db.execute(select(User).where(User.email == user.email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Create new user
        db_user = User(email=user.email, name=user.name)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profile")
async def get_profile(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token payload")
        
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"user": {"name": user.name, "email": user.email}}
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
