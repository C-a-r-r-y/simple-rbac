from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from schemas.auth import TokenPayload
from schemas.user import UserCreate, UserUpdate, UserResponse, UserRole
from routes.depends import get_current_user,get_current_admin
from services.user_services import get_user_by_id,get_users,create_user,update_user,delete_user
from services.db import get_db_session

router = APIRouter(tags=["users"])

@router.get("/", response_model=List[UserResponse])
async def get_users(
    page: int = 1,
    limit: int = 10,
    role: Optional[str] = None,
    current_user_token: TokenPayload = Depends(get_current_user)
):
    current_user = await get_user_by_id(current_user_token.id)
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    async with get_db_session() as session:
        skip = (page - 1) * limit
        users = await get_users(session, skip=skip, limit=limit)
        if role:
            users = [user for user in users if user.role == role]
        return users

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    current_user_token: TokenPayload = Depends(get_current_admin)
):
    async with get_db_session() as session:
        return await create_user(session, user_data)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user_token: TokenPayload = Depends(get_current_admin)
):
    async with get_db_session() as session:
        return await update_user(session, user_id, user_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user_token: TokenPayload = Depends(get_current_admin)
):
    async with get_db_session() as session:
        success = await delete_user(session, user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
