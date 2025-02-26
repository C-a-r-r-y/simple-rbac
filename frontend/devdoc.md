## 项目概述

本项目是一个用户管理系统，前端部分使用 Vue.js 作为主要框架，结合 Vue Router 进行路由管理，Pinia 进行状态管理，Element Plus 作为 UI 组件库。前端需要实现登录页面和用户管理页面，并根据用户角色控制页面元素的显示与隐藏，特别是对修改和删除按钮的权限控制。

## 技术栈

* Typescript
* Vue.js：前端框架，用于构建用户界面。
* Vue Router：用于管理前端路由。
* Pinia：用于状态管理，存储用户登录状态、角色信息等。
* Element Plus：UI 组件库，提供丰富的 UI 组件。
* Axios：用于与后端 API 进行通信。
* Vite：构建工具，用于快速开发和打包项目。
* npm：包管理工具
* pinia-plugin-persistedstate：用于状态持久化存储
* jwt-decode：用于解析JWT令牌

## 项目结构

```
frontend/
├── src/
│   ├── api/            # API 服务相关
│   ├── components/     # 公共组件
│   ├── router/         # 路由配置
│   ├── store/          # 状态管理
│   ├── views/          # 页面视图
│   ├── App.vue         # 根组件
│   ├── main.ts         # 入口文件
│   └── style.css       # 全局样式
├── index.html          # 主页面
├── package.json        # 项目依赖
├── vite.config.ts      # Vite 配置
└── tsconfig.json       # TypeScript 配置
```

## 页面设计

### 1. 登录页面 (`loginPage`)

#### UI 组件安排

* 用户名输入框：使用 Element Plus 的 `el-input` 组件，用于输入用户名。
* 密码输入框：使用 Element Plus 的 `el-input` 组件，类型为 `password`，用于输入密码。
* 登录按钮：使用 Element Plus 的 `el-button` 组件，点击后触发登录逻辑。

#### 功能描述

* 用户输入用户名和密码后，点击登录按钮，前端通过 Axios 发送登录请求到后端 `/api/auth/login` 接口。
* 登录成功后，前端将获取到的 `access_token` 和 `refresh_token` 存储在 Pinia 状态管理中，并跳转到用户管理页面。
* 登录失败时，前端显示错误提示。

### 2. 用户管理页面 (`managePage`)

#### UI 组件安排

* 导航栏：使用 Element Plus 的 `el-menu` 组件，显示欢迎信息和当前用户信息
* 登出按钮：使用 Element Plus 的 `el-button` 组件，位于页面右上角，点击后触发登出逻辑。
* 用户列表：使用 Element Plus 的 `el-table` 组件，展示用户信息，包括 `ID`、`用户名`、`角色`、`描述` 等字段。
* 创建用户按钮：使用 Element Plus 的 `el-button` 组件，仅管理员可见，点击后弹出创建用户对话框。
* 修改按钮：使用 Element Plus 的 `el-button` 组件，位于每一行的操作列中，点击后弹出修改对话框。
* 删除按钮：使用 Element Plus 的 `el-button` 组件，位于每一行的操作列中，点击后触发删除逻辑。
* 修改对话框：使用 Element Plus 的 `el-dialog` 组件，用于修改用户信息。

#### 功能描述

* 用户列表展示：前端通过 Axios 发送请求到 `/api/users` 接口，获取用户列表数据，并在表格中展示。
* 创建用户：管理员点击创建用户按钮后，弹出创建用户对话框，填写信息后提交。
* 修改按钮的显示与隐藏：根据当前登录用户的角色，动态控制修改按钮的显示与隐藏。只有 `系统管理员` 和 `管理员` 可以看到并操作修改按钮。
* 删除按钮的显示与隐藏：根据当前登录用户的角色，动态控制删除按钮的显示与隐藏。只有 `系统管理员` 和 `管理员` 可以看到并操作删除按钮。
* 修改用户信息：点击修改按钮后，弹出修改对话框，用户可以在对话框中修改用户名、角色和描述信息。修改完成后，前端通过 Axios 发送请求到 `/api/users/{user_id}` 接口，更新用户信息。
* 删除用户：点击删除按钮后，前端通过 Axios 发送请求到 `/api/users/{user_id}` 接口，删除对应用户。

## 权限控制

### 1. 修改和删除按钮的权限控制

* 系统管理员、管理员：可以看到并操作所有用户的修改和删除按钮。
* 普通用户：无法看到修改和删除按钮，只能查看用户列表。

#### 实现逻辑

* 前端在用户登录成功后，从后端获取用户角色信息，并存储在 Pinia 状态管理中。
* 在用户管理页面中，前端根据当前用户的角色动态渲染表格中的操作列。如果当前用户是 `普通用户`，则不渲染修改和删除按钮；如果是 `系统管理员` 或 `管理员`，则渲染这些按钮。

### 2. 路由权限控制

* 登录页面：所有用户都可以访问。
* 用户管理页面：只有登录成功的用户才能访问。如果用户未登录，尝试访问用户管理页面时，前端应自动跳转到登录页面。

#### 实现逻辑

* 使用 Vue Router 的导航守卫（`beforeEach`）进行路由权限控制。在每次路由跳转前，检查 Pinia 中是否存储了有效的 `access_token`。如果没有，则跳转到登录页面。

## Token 管理

### 1. Access Token 和 Refresh Token 的存储

* 登录成功后，前端将 `access_token` 和 `refresh_token` 存储在 Pinia 状态管理中，并设置 `access_token` 的过期时间。
* 每次发送 API 请求时，前端从 Pinia 中获取 `access_token` 并添加到请求头中。
* 使用 pinia-plugin-persistedstate 插件将 token 存储在 localStorage 中，实现状态持久化

### 2. Token 自动刷新

* 前端在每次发送 API 请求前，检查 `access_token` 是否即将过期（例如，剩余有效期小于 5 分钟）。如果即将过期，前端使用 `refresh_token` 调用 `/api/auth/refresh` 接口，获取新的 `access_token` 和 `refresh_token`，并更新 Pinia 中的存储。
* 使用 Axios 的拦截器统一处理 token 刷新逻辑，避免在每个请求中重复编写代码。

## 状态管理

### 用户登录状态

* 使用 Pinia 存储用户登录状态，包括 `access_token`、`refresh_token`、用户角色、用户名、用户ID等信息。
* 在用户登出时，清除 Pinia 中的登录状态。
* 使用 pinia-plugin-persistedstate 插件进行状态持久化，在应用启动时自动从 localStorage 恢复状态

## 开发环境配置

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