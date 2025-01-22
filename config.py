import os
from datetime import timedelta

# 数据库配置
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '3306')),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'database': os.getenv('DB_NAME', 'user_manage'),
    'charset': 'utf8mb4'
}

# JWT配置
JWT_CONFIG = {
    'secret_key': os.getenv('JWT_SECRET_KEY', 'your-secret-key'),
    'algorithm': 'HS256',
    'access_token_expire': timedelta(minutes=int(os.getenv('JWT_ACCESS_EXPIRE_MINUTES', '10'))),
    'refresh_token_expire': timedelta(days=int(os.getenv('JWT_REFRESH_EXPIRE_DAYS', '3')))
}

# 日志配置
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'filename': os.getenv('LOG_FILE', 'app.log')
}

# 系统管理员初始配置
SYSTEM_ADMIN_CONFIG = {
    'username': os.getenv('ADMIN_USERNAME', 'admin'),
    'password': os.getenv('ADMIN_PASSWORD', 'password'),
    'role': os.getenv('ADMIN_ROLE', 'system_admin'),
    'description': os.getenv('ADMIN_DESCRIPTION', 'default system admin')
}
