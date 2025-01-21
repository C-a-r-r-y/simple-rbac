import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import DATABASE_CONFIG, JWT_CONFIG, LOGGING_CONFIG, SYSTEM_ADMIN_CONFIG
from sqlalchemy.ext.asyncio import create_async_engine
from services.init_db import init_db
from routes.auth import auth_router
from routes.users import users_router

# 配置日志
logging.basicConfig(
    level=LOGGING_CONFIG['level'],
    format=LOGGING_CONFIG['format'],
    filename=LOGGING_CONFIG['filename']
)
logger = logging.getLogger(__name__)

# 初始化FastAPI应用
app = FastAPI(
    title="User Management System",
    description="API for managing users with role-based access control",
    version="1.0.0"
)

# 创建数据库引擎
engine = create_async_engine(
    f"mysql+asyncmy://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@"
    f"{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}",
    echo=True
)

# 初始化数据库
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database...")
    await init_db(engine)
    logger.info("Database initialized successfully")

# 注册路由
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
