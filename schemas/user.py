from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, model_validator
from typing import Optional

# 用户角色枚举
class UserRole(str, Enum):
    SYSTEM_ADMIN = "system_admin"
    ADMIN = "admin"
    USER = "user"

# 基础用户模型
class UserBase(BaseModel):
    username: str = Field(..., max_length=50, description="用户名")
    role: UserRole = Field(default=UserRole.USER, description="用户角色")
    description: Optional[str] = Field(None, max_length=255, description="用户描述")

# 用户创建模型
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=255, description="用户密码")


# 用户更新模型
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=50, description="用户名")
    role: Optional[UserRole] = Field(None, description="用户角色")
    description: Optional[str] = Field(None, max_length=255, description="用户描述")

    # 可选：确保至少更新一个字段
    @model_validator(mode='before')
    def validate_at_least_one_field(cls, values):
        if not any(values.values()):
            raise ValueError("至少需要更新一个字段")
        return values

# 用户响应模型
class UserResponse(UserBase):
    id: int = Field(..., description="用户ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        orm_mode = True  # 允许从 ORM 对象加载数据