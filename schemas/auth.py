from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    access_token_exp: int
    refresh_token_exp: int

class TokenPayload(BaseModel):
    id: int
    username: str
    role: str
    exp: int

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str
