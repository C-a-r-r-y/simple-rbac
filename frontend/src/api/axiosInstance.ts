import axios from 'axios';
import { userStore } from '../store/userStore';
import router from '../router';

// 创建axios实例
const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
apiClient.interceptors.request.use(
  async (config) => {
    const store = userStore();
    
    // 只有已登录状态才添加Authorization头
    if (store.isLoggedIn) {
      const accessToken = store.accessToken;
      if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`;
      }
    }
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const store = userStore(); // 获取用户状态

    // 如果未登录，直接返回错误
    if (!store.isLoggedIn) {
      return Promise.reject(error);
    }

    const originalRequest = error.config;

    // 如果401错误且不是刷新token的请求
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // 尝试刷新 token
        await store.refreshTokenMethod();

        // 更新请求头并重试原始请求
        originalRequest.headers.Authorization = `Bearer ${store.accessToken}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // 刷新 token 失败，清除登录状态并跳转登录页
        store.logout();
        router.push({ name: 'login' });
        return Promise.reject(refreshError);
      }
    }

    // 非 401 错误或已重试过，直接返回错误
    return Promise.reject(error);
  }
);

export default apiClient;