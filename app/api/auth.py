import os
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel

router = APIRouter(tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

AUTH_USERNAME = os.getenv("AUTH_USERNAME") or os.getenv("ADMIN_USERNAME") or "admin"
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD") or os.getenv("ADMIN_PASSWORD") or "password123"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
HASHED_AUTH_PASSWORD = pwd_context.hash(AUTH_PASSWORD) if not AUTH_PASSWORD.startswith("$2b$") else AUTH_PASSWORD

class LoginRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_or_plain: str) -> bool:
    if plain_password == hashed_or_plain:
        return True
    try:
        return pwd_context.verify(plain_password, hashed_or_plain)
    except Exception:
        return False

@router.post("/api/login", response_model=TokenResponse)
@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest) -> TokenResponse:
    user_identifier = credentials.username or credentials.email
    if not user_identifier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is required",
        )
    if user_identifier != AUTH_USERNAME or not verify_password(credentials.password, HASHED_AUTH_PASSWORD):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user_identifier})
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={"username": user_identifier}
    )
