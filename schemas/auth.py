from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    """
    表示一个JWT令牌的模型类。
    
    Attributes:
        access_token (str): 访问令牌，用于身份验证和授权。
        refresh_token (str): 刷新令牌，用于获取新的访问令牌。
        token_type (str): 令牌类型，通常是"Bearer"。
        expires_in (int): 访问令牌的有效期，以秒为单位。
    """
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    """
    表示JWT令牌中存储的数据的模型类。
    
    Attributes:
        id (int): 用户的唯一标识符。
        username (str): 用户的用户名。
        role (str): 用户的角色或权限。
        exp (datetime): 令牌的过期时间。
    """
    id: int
    username: str
    role: str
    exp: datetime

class LoginRequest(BaseModel):
    """
    表示用户登录请求的模型类。
    
    Attributes:
        username (str): 用户登录时输入的用户名。
        password (str): 用户登录时输入的密码。
    """
    username: str
    password: str

class RefreshTokenRequest(BaseModel):
    """
    表示刷新令牌请求的模型类。
    
    Attributes:
        refresh_token (str): 用于刷新访问令牌的刷新令牌。
    """
    refresh_token: str