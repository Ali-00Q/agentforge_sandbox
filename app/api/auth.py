import os
from fastapi import APIRouter, HTTPException, status
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/api", tags=["auth"])

_default_user = os.getenv("AUTH_USERNAME", "admin")
_default_email = os.getenv("AUTH_EMAIL", "admin@example.com")
_default_pass = os.getenv("AUTH_PASSWORD", "secret123")
_default_hash = os.getenv("AUTH_PASSWORD_HASH") or get_password_hash(_default_pass)

_users_db = {
    _default_user.lower(): {
        "id": 1,
        "username": _default_user,
        "email": _default_email,
        "hashed_password": _default_hash,
    }
}
if _default_email:
    _users_db[_default_email.lower()] = _users_db[_default_user.lower()]

@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest) -> TokenResponse:
    identifier = (credentials.username or credentials.email or "").strip().lower()
    if not identifier or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username/email and password are required",
        )

    user = _users_db.get(identifier)
    if not user or not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user["id"]), "username": user["username"]})
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(id=user["id"], username=user["username"], email=user["email"]),
    )
