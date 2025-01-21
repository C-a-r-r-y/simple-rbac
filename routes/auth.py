from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.auth import Token, LoginRequest, RefreshTokenRequest
from services.auth_service import create_tokens, verify_token, refresh_tokens
from services.user_services import authenticate_user
from services.db import get_db

router = APIRouter(tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(session, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_tokens(user.id, user.username, user.role)

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(status_code=401, detail="Invalid token")
    # TODO: 实现token黑名单
    return {"message": "Successfully logged out"}

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_data: RefreshTokenRequest):
    tokens = refresh_tokens(refresh_data.refresh_token)
    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return tokens
