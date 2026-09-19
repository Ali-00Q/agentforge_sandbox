import datetime
import jwt
from fastapi import APIRouter, HTTPException, status
from schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/api", tags=["auth"])

SECRET_KEY = "secret-key-change-in-production"
ALGORITHM = "HS256"

MOCK_USERS_DB = {
    "admin": "admin123",
    "user": "password123"
}

def create_access_token(data: dict, expires_delta: datetime.timedelta = datetime.timedelta(hours=1)) -> str:
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    username = request.username
    password = request.password
    
    stored_password = MOCK_USERS_DB.get(username)
    if not stored_password or stored_password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": username})
    return TokenResponse(access_token=access_token, token_type="bearer")
