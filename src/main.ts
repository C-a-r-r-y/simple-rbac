import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './style.css'
import App from './App.vue'
import router from './router'
import apiClient from './api/axiosInstance'
import { userStore } from './store/userStore'

const pinia = createPinia()

const app = createApp(App)

// 配置路由和状态管理
app.use(router)
app.use(pinia)
app.use(ElementPlus)

// 初始化userStore
const store = userStore()

// 使用插件进行持久化，监听 store 变化并保存到本地存储
store.$subscribe((mutation, state) => {
  localStorage.setItem('authStore', JSON.stringify(state));
});

// 监听 action 执行，登录和刷新令牌后保存状态到本地存储
store.$onAction(({ name, store, args, after, onError }) => {
  if (name === 'login' || name === 'refreshTokenMethod') {
    after(() => {
      localStorage.setItem('authStore', JSON.stringify(store.$state));
    });
  }
});

// 初始化时从本地存储恢复状态
const persistedState = JSON.parse(localStorage.getItem('authStore') || '{}');
if (persistedState.accessToken && persistedState.refreshTokenToken && persistedState.role && persistedState.username && persistedState.userId !== null) {
  store.$patch(persistedState);
}

// 设置axios拦截器
apiClient

app.mount('#app')
