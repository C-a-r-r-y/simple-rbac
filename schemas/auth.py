from pydantic import BaseModel
from datetime import datetime

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    access_token_exp: datetime
    refresh_token_exp: datetime

class TokenPayload(BaseModel):
    id: int
    username: str
    role: str
    exp: datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str
