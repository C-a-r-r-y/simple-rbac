import { defineStore } from 'pinia';
import { ref } from 'vue';
import { authService } from '../api/authService';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { createPinia } from 'pinia';

// 创建 Pinia 实例并使用持久化插件
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

// 定义 auth store，包含用户认证相关状态和方法
export const useAuthStore = defineStore('auth', () => {
  // 用户访问令牌
  const accessToken = ref('');
  // 用户刷新令牌
  const refreshToken = ref('');
  // 用户角色
  const role = ref('');
  // 用户名
  const username = ref('');
  // 用户 ID
  const userId = ref<number | null>(null);

  // 设置访问和刷新令牌的方法
  function setTokens(tokens: { access_token: string; refresh_token: string }) {
    accessToken.value = tokens.access_token;
    refreshToken.value = tokens.refresh_token;
  }

  // 设置用户角色的方法
  function setRole(userRole: string) {
    role.value = userRole;
  }

  // 用户登录方法，调用 authService.login 获取令牌并设置状态
  async function login(usernameParam: string, password: string) {
    try {
      const { access_token, refresh_token, role: userRole, username: userUsername, id: userIdValue } = await authService.login(usernameParam, password);
      setTokens({ access_token, refresh_token });
      setRole(userRole);
      username.value = userUsername;
      userId.value = userIdValue;
    } catch (error) {
      console.error('Login failed:', error);
    }
  }

  // 用户登出方法，清空所有状态
  async function logout() {
    accessToken.value = '';
    refreshToken.value = '';
    role.value = '';
    username.value = '';
    userId.value = null;
  }

  // 刷新访问令牌的方法，调用 authService.refreshToken 获取新令牌并设置状态
  async function refreshTokenMethod() {
    try {
      const { access_token, refresh_token } = await authService.refreshToken(refreshToken.value);
      setTokens({ access_token, refresh_token });
    } catch (error) {
      console.error('Token refresh failed:', error);
    }
  }

  return { accessToken, refreshTokenToken: refreshToken, role, username, userId, login, logout, refreshTokenMethod };
}, {
  persist: true,
});

// 使用插件进行持久化，监听 store 变化并保存到本地存储
useAuthStore().$subscribe((mutation, state) => {
  localStorage.setItem('authStore', JSON.stringify(state));
});

// 监听 action 执行，登录和刷新令牌后保存状态到本地存储
useAuthStore().$onAction(({ name, store, args, after, onError }) => {
  if (name === 'login' || name === 'refreshTokenMethod') {
    after(() => {
      localStorage.setItem('authStore', JSON.stringify(store.$state));
    });
  }
});

// 初始化时从本地存储恢复状态
const persistedState = JSON.parse(localStorage.getItem('authStore') || '{}');
if (persistedState.accessToken && persistedState.refreshTokenToken && persistedState.role && persistedState.username && persistedState.userId !== null) {
  useAuthStore().$patch(persistedState);
}
