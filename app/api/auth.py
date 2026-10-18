from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import os

from fastapi import APIRouter, HTTPException, status
import jwt
from pydantic import BaseModel, Field

SECRET_KEY = os.getenv("SECRET_KEY", "default-jwt-secret-key-change-in-prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

AUTH_USERNAME = os.getenv("AUTH_USERNAME", "admin")
AUTH_EMAIL = os.getenv("AUTH_EMAIL", "admin@example.com")
ENV_PASSWORD = os.getenv("AUTH_PASSWORD", "admin123")
ENV_PASSWORD_HASH = os.getenv("AUTH_PASSWORD_HASH")

def hash_password(password: str) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        b"fastapi_auth_salt_v1",
        100000
    ).hex()

STORED_PASSWORD_HASH = ENV_PASSWORD_HASH if ENV_PASSWORD_HASH else hash_password(ENV_PASSWORD)

router = APIRouter(prefix="/api", tags=["auth"])

class LoginRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str = Field(min_length=1)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login")
def login(credentials: LoginRequest) -> Token:
    identifier = credentials.username or credentials.email
    if not identifier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email is required",
        )

    valid_user = (identifier == AUTH_USERNAME or identifier == AUTH_EMAIL)
    input_hash = hash_password(credentials.password)
    valid_password = hmac.compare_digest(input_hash, STORED_PASSWORD_HASH)

    if not valid_user or not valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": identifier})
    return Token(access_token=token, token_type="bearer", username=identifier)
