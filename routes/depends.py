from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from schemas.auth import TokenData
from schemas.user import UserRole
from services.auth_service import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def _get_token_data(token: str) -> TokenData:
    """验证并返回TokenData"""
    token_data = verify_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """获取当前用户"""
    return await _get_token_data(token)

async def get_current_admin(token: str = Depends(oauth2_scheme)) -> TokenData:
    """获取当前管理员用户"""
    token_data = await _get_token_data(token)
    if token_data.role not in [UserRole.SYSTEM_ADMIN, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Insufficient privileges for this operation",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data