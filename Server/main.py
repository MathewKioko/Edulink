from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Auth.Services.authService import hash_password
from Auth.Services.authService import verify_password
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from Routes import user, group
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Database.database import get_db, init_db
from Database.models import User
from fastapi import Depends

# CORS Configuration
# Allow specific origins for security. Add http://localhost:5173 for frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",  # Alternative Vite port
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCredentials(BaseModel):
    email: str
    password: str
    name: str

class LoginCredentials(BaseModel):
    email: str
    password: str

try:
    from Auth.Services.authService import access_token
    print("Auth import successful")
except ImportError as e:
    print(f" Auth import failed: {e}")


@app.get('/')
async def landing():
    return {"Message": "Hello user"}

@app.get("/test")
async def test(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User))
        count = len(result.scalars().all())
        return {"Message": f"Successfully connected to PostgreSQL ({count} users)"}
    except Exception as e:
        return {"error": f"PostgreSQL connection failed: {str(e)}"}
    
# Login Route
@app.post('/signin')
async def Login(user: LoginCredentials, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.email == user.email))
        existing_user = result.scalar_one_or_none()

        if not existing_user:
            return {"Message": "User not found"}
        
        token = access_token({"email": user.email})
        return {"Message": "Login successful", "token": token}
    except Exception as e:
        return {"error": f"Login Failed {str(e)}"}


# Register Route
@app.post('/signup')
async def Register(user: UserCredentials, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User).where(User.email == user.email))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            return {"error": "User already exists"}
        
        hashed_password = hash_password(user.password)

        db_user = User(email=user.email, name=user.name, password=hashed_password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        token = access_token({"email": user.email})
        return {"message": "User registered successfully", "token": token}
    except Exception as e:
        await db.rollback()
        return {"error": f"Registration failed: {str(e)}"}
    


app.include_router(user.router, prefix="/user")
app.include_router(group.router, prefix="/groups")

@app.on_event("startup")
async def startup():
    await init_db()
