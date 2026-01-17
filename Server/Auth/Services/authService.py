 
import jwt
from datetime import datetime, timedelta
import os
import bcrypt
from dotenv import load_dotenv
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from Database.database import get_db
from Database.models import User

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
if JWT_SECRET is None:
    raise Exception('JWT SECRET environment not set')
algorithm = "HS256"

# Use HTTPBearer instead of OAuth2PasswordBearer (no tokenUrl required)
bearer_scheme = HTTPBearer()

# Password hashing
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# JWT creation - include user ID and email
def access_token(data: dict, expires_delta: timedelta = timedelta(hours=9)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    token = jwt.encode(to_encode, JWT_SECRET, algorithm)
    return token

def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")

# Get current user from PostgreSQL database
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db)
):
    """
    Dependency to get the current authenticated user from the JWT token.
    The token is extracted from the Authorization header (Bearer scheme).
    """
    token = credentials.credentials
    
    try:
        payload = decode_token(token)
        email = payload.get("email")
        
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: email not found"
            )
        
        # Query user from PostgreSQL
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        # Return user dict for compatibility
        return {
            "_id": str(user.id),
            "email": user.email,
            "name": user.name,
            "id": user.id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
