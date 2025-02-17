from dotenv import load_dotenv
load_dotenv()

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import JWT_CONFIG, LOGGING_CONFIG, SYSTEM_ADMIN_CONFIG
from services.db import create_db_engine, init_db, close_db_connection
from routes.auth import router as auth_router
from routes.users import router as users_router

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

# 数据库初始化
@app.on_event("startup")
async def startup_event():
    logger.info("Initializing database...")
    engine = create_db_engine()
    await init_db(engine)
    logger.info("Database initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Closing database connections...")
    await close_db_connection()
    logger.info("Database connections closed")

# 注册路由
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(users_router, prefix="/api/users", tags=["users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
