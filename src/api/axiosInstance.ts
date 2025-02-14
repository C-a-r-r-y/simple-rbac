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
    const accessToken = store.accessToken;
    
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
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
    const originalRequest = error.config;
    
    // 如果401错误且不是刷新token的请求
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const store = userStore();
        await store.refreshTokenMethod();
        
        // 重试原始请求
        originalRequest.headers.Authorization = `Bearer ${store.accessToken}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // 刷新token失败，使用router跳转到登录页
        router.push({ name: 'login' });
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

export default apiClient;