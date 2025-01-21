from typing import List, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserResponse

# 创建一个密码上下文对象，指定使用 bcrypt 加密算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    
async def create_user(session: AsyncSession, user_data: UserCreate) -> UserResponse:
    """创建用户"""
    hashed_password = pwd_context.hash(user_data.password)
    user = User(
        username=user_data.username,
        password=hashed_password,
        role=user_data.role,
        description=user_data.description
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return UserResponse.from_orm(user)


async def get_user(session: AsyncSession, user_id: int) -> Optional[UserResponse]:
    """根据ID获取用户"""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    return UserResponse.from_orm(user) if user else None


async def get_users(session: AsyncSession, skip: int = 0, limit: int = 100) -> List[UserResponse]:
    """获取用户列表"""
    result = await session.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()
    return [UserResponse.from_orm(user) for user in users]


async def update_user(session: AsyncSession, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
    """更新用户信息"""
    await session.execute(
        update(User)
        .where(User.id == user_id)
        .values(**user_data.dict(exclude_unset=True))
    )
    await session.commit()
    return await get_user(session, user_id)


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    """删除用户"""
    result = await session.execute(delete(User).where(User.id == user_id))
    await session.commit()
    return result.rowcount > 0


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证输入的明文密码是否与存储的哈希密码匹配"""
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(session: AsyncSession, username: str, password: str) -> Optional[UserResponse]:
    """验证用户登录"""
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return UserResponse.from_orm(user)
