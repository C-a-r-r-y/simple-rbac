# 使用Node.js作为基础镜像
FROM node:18-alpine as build-stage

# 设置工作目录
WORKDIR /app

# 复制package.json和package-lock.json
COPY package*.json ./

# 安装依赖
RUN npm config set registry https://registry.npmmirror.com && \
    npm install

# 复制项目文件
COPY . .

# 构建项目
RUN npm run build

# 使用Nginx作为生产环境
FROM nginx:stable-alpine as production-stage

# 复制构建好的文件到Nginx目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 暴露80端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]
