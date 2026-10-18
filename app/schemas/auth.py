from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str

class UserResponse(BaseModel):
    id: int | str
    username: str
    email: str | None = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse | None = None
