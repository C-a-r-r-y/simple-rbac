from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.auth import TokenResponse, LoginRequest, RefreshTokenRequest
from services.auth import create_tokens_response, verify_token, refresh_tokens
from services.user import authenticate_user
from services.db import get_db_session_dep

router = APIRouter(tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_db_session_dep)
):
    user = await authenticate_user(session, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_tokens_response(user.id, user.username, user.role)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_data: RefreshTokenRequest):
    tokens = refresh_tokens(refresh_data.refresh_token)
    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return tokens
