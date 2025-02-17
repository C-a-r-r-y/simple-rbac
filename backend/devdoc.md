## 项目概述

本项目是一个简单的用户管理系统，支持三种用户角色：系统管理员、管理员和普通用户。系统管理员在项目启动时自动生成，且唯一。所有账户必须由管理员手动创建。用户表包含密码、ID、角色、描述等信息，管理员可以对用户表进行增删改查，普通用户只能读取用户表。

## 技术栈

* **后端技术栈**：FastAPI、SQLAlchemy、MySQL、bcrypt、PyJWT、logging
* **前端技术栈**：Vue、Vue Router、Pinia、Vite、Axios、Element Plus

## 数据库设计

### 用户表结构

| 字段名 | 数据类型 | 约束条件 | 默认值 | 说明                                               |
| -------- | ---------- | ---------- | -------- | ---------------------------------------------------- |
| `id`       | `INT`         | `PRIMARY KEY`, `AUTO_INCREMENT`       | -      | 用户ID，主键，自增                                 |
| `username`       | `VARCHAR(50)`         | `NOT NULL`, `UNIQUE`       | -      | 用户名，唯一                                       |
| `password`       | `VARCHAR(255)`         | `NOT NULL`         | -      | 用户密码，使用哈希加密存储                         |
| `role`       | `ENUM`         | `NOT NULL`         | `UserRole.USER`       | 用户角色，枚举类型，可选值为 `UserRole.SYSTEM_ADMIN`, `UserRole.ADMIN`, `UserRole.USER`                  |
| `description`       | `TEXT`         | -        | -      | 用户描述，可选                                     |
| `created_at`       | `DATETIME`         | -        | `当前UTC时间`       | 用户创建时间，默认值为当前UTC时间                     |
| `updated_at`       | `DATETIME`         | -        | `当前UTC时间，更新时自动更新`       | 用户信息更新时间，默认值为当前UTC时间，更新时自动更新 |

### 数据库初始化

* 系统初始化时，后端控制层会检查表是否存在，若不存在则自动创建表。
* 检查表中是否存在系统管理员，若不存在则创建一个名为`admin`、密码为`password`、描述为`default system admin`的系统管理员。

## 鉴权设计

### 角色权限

* **系统管理员、管理员**：可以访问所有 API，包括用户增删改查。
* **普通用户**：只能访问用户列表（只读）。

### JWT 鉴权

JWT（JSON Web Token）用于用户身份验证和权限控制。JWT 包含以下信息：

* **Payload**：用户 ID、用户名、角色、Token 过期时间、token_type等。
* **签名**：使用后端密钥对 Payload 进行签名，确保 Token 的完整性和安全性。

### JWT Token 数据结构

```python
class TokenPayload:
    id: int  # 用户ID
    username: str  # 用户名
    role: str  # 用户角色
    exp: int  # Token过期时间
    token_type: str  # Token类型（access或refresh）
```

### JWT 自动过期机制

* **Access Token**：用于常规 API 请求，有效期较短（如 30 分钟）。
* **Refresh Token**：用于刷新 Access Token，有效期较长（如 7 天）。

#### Token 刷新流程

1. 客户端使用 Refresh Token 请求 `/api/auth/refresh` 接口。
2. 服务端验证 Refresh Token 的有效性。
3. 服务端生成新的 Access Token 和 Refresh Token，并返回给客户端。
4. 客户端更新本地存储的 Token。

### Token 验证

* **verify_access_token**：验证access token有效性并返回payload，如果token无效或类型不匹配则返回None
* **verify_refresh_token**：验证refresh token有效性并返回payload，如果token无效或类型不匹配则返回None

## 单元测试

### 测试框架

* 使用 `pytest` 进行单元测试。
* 使用 `requests` 库模拟 API 请求。

### 测试用例

1. **用户登录**：
    * 测试正确的用户名和密码。
    * 测试错误的用户名和密码。
2. **用户登出**：
    * 测试已登录用户登出。
    * 测试未登录用户登出。
3. **刷新 JWT Token**：
    * 测试有效的 Refresh Token。
    * 测试无效的 Refresh Token。
4. **获取用户列表**：
    * 测试不同角色的用户访问权限。
    * 测试分页和过滤功能。
5. **创建用户**：
    * 测试管理员创建用户。
    * 测试普通用户尝试创建用户。
6. **更新用户信息**：
    * 测试管理员更新用户信息。
    * 测试普通用户尝试更新用户信息。
7. **删除用户**：
    * 测试管理员删除用户。
    * 测试普通用户尝试删除用户。

## 日志记录

* 使用 `logging` 模块记录系统日志。
* 日志级别包括 `INFO`、`WARNING`、`ERROR`。
* 日志内容包括用户操作、API 请求、错误信息等。

## 后续开发
* **部署文档**：包括 Docker 容器化、CI/CD 流程、环境变量配置等。