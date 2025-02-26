from typing import Optional
import jwt
import time
from config import JWT_CONFIG
from schemas.auth import TokenResponse, TokenPayload

SECRET_KEY = JWT_CONFIG['secret_key']
ALGORITHM = JWT_CONFIG['algorithm']
ACCESS_TOKEN_EXPIRE = JWT_CONFIG['access_token_expire']
REFRESH_TOKEN_EXPIRE = JWT_CONFIG['refresh_token_expire']


def get_current_time() -> int:
    """获取当前UTC时间戳"""
    return int(time.time())

def create_token(user_id: int, username: str, role: str, token_type: str = "access") -> str:
    """创建JWT token"""
    expire_delta = ACCESS_TOKEN_EXPIRE if token_type == "access" else REFRESH_TOKEN_EXPIRE
    expire = get_current_time() + int(expire_delta.total_seconds())
    
    to_encode = {
        "id": user_id,
        "username": username,
        "role": role,
        "exp": expire,
        "token_type": token_type
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_tokens_response(user_id: int, username: str, role: str) -> TokenResponse:
    """创建access token和refresh token"""
    access_token = create_token(user_id, username, role, "access")
    refresh_token = create_token(user_id, username, role, "refresh")
    
    # 获取token的过期时间
    access_token_exp = get_current_time() + int(ACCESS_TOKEN_EXPIRE.total_seconds())
    refresh_token_exp = get_current_time() + int(REFRESH_TOKEN_EXPIRE.total_seconds())
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        access_token_exp=access_token_exp,
        refresh_token_exp=refresh_token_exp
    )

def verify_access_token(token: str) -> Optional[TokenPayload]:
    """验证access token有效性并返回payload，如果token无效或类型不匹配则返回None"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("token_type") != "access":
            return None
        return TokenPayload(
            id=payload.get("id"),
            username=payload.get("username"),
            role=payload.get("role"),
            exp=payload.get("exp"),
            token_type=payload.get("token_type")
        )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def verify_refresh_token(token: str) -> Optional[TokenPayload]:
    """验证refresh token有效性并返回payload，如果token无效或类型不匹配则返回None"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("token_type") != "refresh":
            return None
        return TokenPayload(
            id=payload.get("id"),
            username=payload.get("username"),
            role=payload.get("role"),
            exp=payload.get("exp"),
            token_type=payload.get("token_type")
        )
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def refresh_tokens(refresh_token: str) -> Optional[TokenResponse]:
    """使用refresh token刷新access token，如果refresh token无效则返回None"""
    token_data = verify_refresh_token(refresh_token)
    if token_data is None:
        return None
    else:
        return create_tokens_response(
            user_id=token_data.id,
            username=token_data.username,
            role=token_data.role
        )
