from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from schemas.auth import TokenPayload
from schemas.user import UserCreate, UserUpdate, UserResponse, UserRole
from routes.depends import get_current_user,get_current_admin
import services.user as user_service

from services.db import get_db_session_dep

router = APIRouter(tags=["users"])

@router.get("/", response_model=List[UserResponse])
async def get_users_list(
    page: int = 1,
    limit: int = 100,
    role: Optional[str] = None,
    current_user_token: TokenPayload = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session_dep)
):
    skip = (page - 1) * limit
    users = await user_service.get_users_list(session, skip=skip, limit=limit)
    if role:
        users = [user for user in users if user.role == role]
    return users

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user_token: TokenPayload = Depends(get_current_admin),
    session: AsyncSession = Depends(get_db_session_dep)
):
    return await user_service.create_user(session, user_data)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user_token: TokenPayload = Depends(get_current_admin),
    session: AsyncSession = Depends(get_db_session_dep)
):
    return await user_service.update_user(session, user_id, user_data)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user_token: TokenPayload = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session_dep)
):
    user = await user_service.get_user(session, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user_token: TokenPayload = Depends(get_current_admin),
    session: AsyncSession = Depends(get_db_session_dep)
):
    success = await user_service.delete_user(session, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
