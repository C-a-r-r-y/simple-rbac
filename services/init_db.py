from sqlalchemy.ext.asyncio import AsyncEngine
from ..models.user import Base, User, UserRole
from sqlalchemy import select
from config import SYSTEM_ADMIN_CONFIG
from services.auth import get_password_hash

async def init_db(engine: AsyncEngine):
    """初始化数据库"""
    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)

        # 检查系统管理员是否存在
        result = await conn.execute(
            select(User).where(User.role == UserRole.SYSTEM_ADMIN)
        )
        if not result.scalars().first():
            # 创建默认系统管理员
            admin = User(
                username=SYSTEM_ADMIN_CONFIG['username'],
                password=get_password_hash(SYSTEM_ADMIN_CONFIG['password']),
                role=UserRole.SYSTEM_ADMIN,
                description=SYSTEM_ADMIN_CONFIG['description']
            )
            conn.add(admin)
            await conn.commit()
