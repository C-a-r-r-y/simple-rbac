from datetime import datetime
from typing import Optional
import jwt
from config import JWT_CONFIG
from schemas.auth import Token, TokenData

SECRET_KEY = JWT_CONFIG['secret_key']
ALGORITHM = JWT_CONFIG['algorithm']
ACCESS_TOKEN_EXPIRE = JWT_CONFIG['access_token_expire']
REFRESH_TOKEN_EXPIRE = JWT_CONFIG['refresh_token_expire']

def create_access_token(user_id: int, username: str, role: str) -> str:
    """创建access token"""
    expire = datetime.utcnow() + ACCESS_TOKEN_EXPIRE
    to_encode = {
        "id": user_id,
        "username": username,
        "role": role,
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int, username: str, role: str) -> str:
    """创建refresh token"""
    expire = datetime.utcnow() + REFRESH_TOKEN_EXPIRE
    to_encode = {
        "id": user_id,
        "username": username,
        "role": role,
        "exp": expire
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_tokens(user_id: int, username: str, role: str) -> Token:
    """创建access token和refresh token"""
    access_token = create_access_token(user_id, username, role)
    refresh_token = create_refresh_token(user_id, username, role)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=int(ACCESS_TOKEN_EXPIRE.total_seconds())
    )

def verify_token(token: str) -> Optional[TokenData]:
    """验证token有效性并返回payload，如果token无效则返回None"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(
            id=payload.get("id"),
            username=payload.get("username"),
            role=payload.get("role"),
            exp=payload.get("exp")
        )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def refresh_tokens(refresh_token: str) -> Optional[Token]:
    """使用refresh token刷新access token，如果refresh token无效则返回None"""
    token_data = verify_token(refresh_token)
    if token_data is None:
        return None
    return create_tokens(
        user_id=token_data.id,
        username=token_data.username,
        role=token_data.role
    )
