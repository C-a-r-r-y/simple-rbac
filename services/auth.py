from passlib.context import CryptContext

# 创建一个密码上下文对象，指定使用 bcrypt 加密算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """生成密码的哈希值，使用 bcrypt 算法进行加密"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证输入的明文密码是否与存储的哈希密码匹配"""
    return pwd_context.verify(plain_password, hashed_password)
