# 使用Nginx作为基础镜像
FROM nginx:stable-alpine

# 复制Nginx配置文件
COPY nginx.conf /etc/nginx/nginx.conf

# 暴露80端口
EXPOSE 80

# 启动Nginx
CMD ["nginx", "-g", "daemon off;"]