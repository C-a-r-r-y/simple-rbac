import { defineStore } from 'pinia';
import { ref } from 'vue';
import { authService } from '../api/authService';
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate';
import { createPinia } from 'pinia';

const pinia = createPinia();
pinia.use(piniaPluginPersistedstate);

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref('');
  const refreshToken = ref('');
  const role = ref('');
  const username = ref('');
  const userId = ref<number | null>(null);

  function setTokens(tokens: { access_token: string; refresh_token: string }) {
    accessToken.value = tokens.access_token;
    refreshToken.value = tokens.refresh_token;
  }

  function setRole(userRole: string) {
    role.value = userRole;
  }

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

  async function logout() {
    accessToken.value = '';
    refreshToken.value = '';
    role.value = '';
    username.value = '';
    userId.value = null;
  }

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

// 使用插件进行持久化
useAuthStore().$subscribe((mutation, state) => {
  localStorage.setItem('authStore', JSON.stringify(state));
});

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
