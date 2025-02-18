# 用户管理系统

## 项目概述

本项目是一个基于现代 Web 技术栈开发的用户管理系统，支持三种用户角色：**系统管理员**、**管理员** 和 **普通用户**。系统通过角色权限控制，实现对用户数据的安全管理和操作。

### 核心功能
1. **用户管理**：
   - 系统管理员在项目启动时自动生成，且唯一。
   - 所有账户必须由管理员手动创建。
   - 用户表包含密码、ID、角色、描述等信息。
   - 管理员可以对用户表进行增删改查操作。
   - 普通用户仅能读取用户列表。

2. **权限控制**：
   - 基于角色的权限管理（RBAC），确保不同角色只能访问其权限范围内的功能。
   - 系统管理员和管理员可操作修改和删除按钮，普通用户仅能查看用户列表。

3. **安全认证**：
   - 使用 JWT（JSON Web Token）实现身份验证和权限控制。
   - Access Token 和 Refresh Token 的自动刷新机制，保障用户会话的安全性和连续性。
   - 密码使用 bcrypt 加密存储，确保数据安全。

4. **前后端分离架构**：
   - 前端采用 Vue.js 框架，结合 Vue Router、Pinia 和 Element Plus，提供响应式和交互性强的用户界面。
   - 后端基于 FastAPI 框架，提供 RESTful API 接口，与 MySQL 数据库交互，完成用户认证、权限管理和数据操作。

5. **容器化部署**：
   - 支持 Docker 容器化部署，简化开发和生产环境配置。
   - 包括前端、后端、数据库和 Nginx 反向代理服务，便于快速搭建和扩展。

### 技术亮点
- **现代化技术栈**：涵盖前端、后端、数据库和安全认证等多个领域。
- **完整的开发流程**：从数据库设计到 API 开发，从前端页面到生产部署，覆盖全生命周期。
- **高可扩展性**：模块化设计，易于扩展新功能或集成第三方服务。


## 技术栈

### 后端技术栈
- FastAPI
- SQLAlchemy
- MySQL
- bcrypt
- PyJWT
- logging

### 前端技术栈
- Typescript
- Vue.js
- Vue Router
- Pinia
- Element Plus
- Axios
- Vite
- npm
- pinia-plugin-persistedstate
- jwt-decode

## 数据库设计

### 用户表结构

| 字段名 | 数据类型 | 约束条件 | 默认值 | 说明 |
| -------- | ---------- | ---------- | -------- | ---------------------------------------------------- |
| `id` | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | - | 用户ID，主键，自增 |
| `username` | `VARCHAR(50)` | `NOT NULL`, `UNIQUE` | - | 用户名，唯一 |
| `password` | `VARCHAR(255)` | `NOT NULL` | - | 用户密码，使用哈希加密存储 |
| `role` | `ENUM` | `NOT NULL` | `UserRole.USER` | 用户角色，枚举类型，可选值为 `UserRole.SYSTEM_ADMIN`, `UserRole.ADMIN`, `UserRole.USER` |
| `description` | `TEXT` | - | - | 用户描述，可选 |
| `created_at` | `DATETIME` | - | `当前UTC时间` | 用户创建时间，默认值为当前UTC时间 |
| `updated_at` | `DATETIME` | - | `当前UTC时间，更新时自动更新` | 用户信息更新时间，默认值为当前UTC时间，更新时自动更新 |

### 数据库初始化
- 系统初始化时，后端控制层会检查表是否存在，若不存在则自动创建表。
- 检查表中是否存在系统管理员，若不存在则创建一个名为`admin`、密码为`password`、描述为`default system admin`的系统管理员。

## 鉴权设计

### 角色权限
- **系统管理员、管理员**：可以访问所有 API，包括用户增删改查。
- **普通用户**：只能访问用户列表（只读）。

### JWT 鉴权
JWT（JSON Web Token）用于用户身份验证和权限控制。JWT 包含以下信息：
- **Payload**：用户 ID、用户名、角色、Token 过期时间、token_type等。
- **签名**：使用后端密钥对 Payload 进行签名，确保 Token 的完整性和安全性。

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
- **Access Token**：用于常规 API 请求，有效期较短（如 30 分钟）。
- **Refresh Token**：用于刷新 Access Token，有效期较长（如 7 天）。

#### Token 刷新流程
1. 客户端使用 Refresh Token 请求 `/api/auth/refresh` 接口。
2. 服务端验证 Refresh Token 的有效性。
3. 服务端生成新的 Access Token 和 Refresh Token，并返回给客户端。
4. 客户端更新本地存储的 Token。

### Token 验证
- **verify_access_token**：验证access token有效性并返回payload，如果token无效或类型不匹配则返回None
- **verify_refresh_token**：验证refresh token有效性并返回payload，如果token无效或类型不匹配则返回None

## 前端页面设计

### 1. 登录页面 (`loginPage`)
#### UI 组件安排
- 用户名输入框：使用 Element Plus 的 `el-input` 组件，用于输入用户名。
- 密码输入框：使用 Element Plus 的 `el-input` 组件，类型为 `password`，用于输入密码。
- 登录按钮：使用 Element Plus 的 `el-button` 组件，点击后触发登录逻辑。

#### 功能描述
- 用户输入用户名和密码后，点击登录按钮，前端通过 Axios 发送登录请求到后端 `/api/auth/login` 接口。
- 登录成功后，前端将获取到的 `access_token` 和 `refresh_token` 存储在 Pinia 状态管理中，并跳转到用户管理页面。
- 登录失败时，前端显示错误提示。

### 2. 用户管理页面 (`managePage`)
#### UI 组件安排
- 导航栏：使用 Element Plus 的 `el-menu` 组件，显示欢迎信息和当前用户信息
- 登出按钮：使用 Element Plus 的 `el-button` 组件，位于页面右上角，点击后触发登出逻辑。
- 用户列表：使用 Element Plus 的 `el-table` 组件，展示用户信息，包括 `ID`、`用户名`、`角色`、`描述` 等字段。
- 创建用户按钮：使用 Element Plus 的 `el-button` 组件，仅管理员可见，点击后弹出创建用户对话框。
- 修改按钮：使用 Element Plus 的 `el-button` 组件，位于每一行的操作列中，点击后弹出修改对话框。
- 删除按钮：使用 Element Plus 的 `el-button` 组件，位于每一行的操作列中，点击后触发删除逻辑。
- 修改对话框：使用 Element Plus 的 `el-dialog` 组件，用于修改用户信息。

#### 功能描述
- 用户列表展示：前端通过 Axios 发送请求到 `/api/users` 接口，获取用户列表数据，并在表格中展示。
- 创建用户：管理员点击创建用户按钮后，弹出创建用户对话框，填写信息后提交。
- 修改按钮的显示与隐藏：根据当前登录用户的角色，动态控制修改按钮的显示与隐藏。只有 `系统管理员` 和 `管理员` 可以看到并操作修改按钮。
- 删除按钮的显示与隐藏：根据当前登录用户的角色，动态控制删除按钮的显示与隐藏。只有 `系统管理员` 和 `管理员` 可以看到并操作删除按钮。
- 修改用户信息：点击修改按钮后，弹出修改对话框，用户可以在对话框中修改用户名、角色和描述信息。修改完成后，前端通过 Axios 发送请求到 `/api/users/{user_id}` 接口，更新用户信息。
- 删除用户：点击删除按钮后，前端通过 Axios 发送请求到 `/api/users/{user_id}` 接口，删除对应用户。

## 权限控制

### 1. 修改和删除按钮的权限控制
- 系统管理员、管理员：可以看到并操作所有用户的修改和删除按钮。
- 普通用户：无法看到修改和删除按钮，只能查看用户列表。

#### 实现逻辑
- 前端在用户登录成功后，从后端获取用户角色信息，并存储在 Pinia 状态管理中。
- 在用户管理页面中，前端根据当前用户的角色动态渲染表格中的操作列。如果当前用户是 `普通用户`，则不渲染修改和删除按钮；如果是 `系统管理员` 或 `管理员`，则渲染这些按钮。

### 2. 路由权限控制
- 登录页面：所有用户都可以访问。
- 用户管理页面：只有登录成功的用户才能访问。如果用户未登录，尝试访问用户管理页面时，前端应自动跳转到登录页面。

#### 实现逻辑
- 使用 Vue Router 的导航守卫（`beforeEach`）进行路由权限控制。在每次路由跳转前，检查 Pinia 中是否存储了有效的 `access_token`。如果没有，则跳转到登录页面。

## Token 管理

### 1. Access Token 和 Refresh Token 的存储
- 登录成功后，前端将 `access_token` 和 `refresh_token` 存储在 Pinia 状态管理中，并设置 `access_token` 的过期时间。
- 每次发送 API 请求时，前端从 Pinia 中获取 `access_token` 并添加到请求头中。
- 使用 pinia-plugin-persistedstate 插件将 token 存储在 localStorage 中，实现状态持久化

### 2. Token 自动刷新
- 前端在每次发送 API 请求前，检查 `access_token` 是否即将过期（例如，剩余有效期小于 5 分钟）。如果即将过期，前端使用 `refresh_token` 调用 `/api/auth/refresh` 接口，获取新的 `access_token` 和 `refresh_token`，并更新 Pinia 中的存储。
- 使用 Axios 的拦截器统一处理 token 刷新逻辑，避免在每个请求中重复编写代码。

## 状态管理

### 用户登录状态
- 使用 Pinia 存储用户登录状态，包括 `access_token`、`refresh_token`、用户角色、用户名、用户ID等信息。
- 在用户登出时，清除 Pinia 中的登录状态。
- 使用 pinia-plugin-persistedstate 插件进行状态持久化，在应用启动时自动从 localStorage 恢复状态

## 开发环境配置

### 后端
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 启动开发服务器：
   ```bash
   uvicorn main:app --reload
   ```

### 前端
1. 安装依赖：
   ```bash
   npm install
   ```

2. 启动开发服务器：
   ```bash
   npm run dev
   ```

3. 构建生产环境：
   ```bash
   npm run build
   ```

## Docker 部署

### 1. 环境要求
- Docker 20.10.0 或更高版本
- Docker Compose 2.0.0 或更高版本

### 2. 部署步骤
1. 确保已安装 Docker 和 Docker Compose
2. 在项目根目录下运行以下命令：
   ```bash
   docker-compose up --build
   ```
3. 应用启动后，可以通过以下地址访问：
   - 前端：http://localhost
   - 后端API：http://localhost/api
4. 停止并移除容器：
   ```bash
   docker-compose down
   ```

### 3. 服务说明
- **frontend**: 前端服务，基于Vue.js构建
- **backend**: 后端服务，基于FastAPI构建
- **mysql**: MySQL数据库服务
- **nginx**: Nginx反向代理服务

### 4. 环境变量配置
所有环境变量配置在 `docker-compose.yml` 文件中，包括：
- 数据库连接信息
- JWT配置
- 日志配置
- 系统管理员初始配置

## 后续开发
- **CI/CD 流程**：自动化构建和部署流程
