from sqlalchemy.ext.asyncio import AsyncEngine
from .user import Base, User, UserRole
from sqlalchemy import select
from .auth import get_password_hash

async def init_db(engine: AsyncEngine):
    """Initialize database"""
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

        # Check if system admin exists
        result = await conn.execute(
            select(User).where(User.role == UserRole.SYSTEM_ADMIN)
        )
        if not result.scalars().first():
            # Create default system admin
            admin = User(
                username="admin",
                password=get_password_hash("password"),
                role=UserRole.SYSTEM_ADMIN,
                description="default system admin"
            )
            conn.add(admin)
            await conn.commit()
