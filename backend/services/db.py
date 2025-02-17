from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models.user import Base, User, UserRole
from sqlalchemy import select
from contextlib import asynccontextmanager
from config import SYSTEM_ADMIN_CONFIG, DATABASE_CONFIG
from services.user import get_password_hash
from typing import AsyncGenerator

# 全局数据库引擎实例
_engine: AsyncEngine | None = None

def create_db_engine() -> AsyncEngine:
    """创建数据库引擎"""
    return create_async_engine(
        f"mysql+asyncmy://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
        f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}",
        echo=True
    )

def get_db_engine() -> AsyncEngine:
    """获取全局数据库引擎实例"""
    if _engine is None:
        raise RuntimeError("Database engine not initialized")
    return _engine

async def get_db_session() -> AsyncSession:
    """获取数据库会话"""
    async with AsyncSession(get_db_engine()) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def get_db_session_dep() -> AsyncSession:
    """FastAPI依赖注入使用的数据库会话获取函数"""
    async with AsyncSession(get_db_engine()) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def init_db(engine: AsyncEngine):
    """初始化数据库"""
    global _engine
    _engine = engine
    
    async with engine.begin() as conn:
        # 创建所有表
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        # 检查系统管理员是否存在
        result = await session.execute(
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
            session.add(admin)
            await session.commit()

async def close_db_connection():
    """关闭数据库连接"""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
