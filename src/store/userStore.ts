import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authService } from '../api/authService';
import { jwtDecode } from 'jwt-decode';

// 定义 store，包含用户认证相关状态和方法
export const userStore = defineStore('user', () => {
  const accessToken = ref('');
  const refreshToken = ref('');
  const role = ref('');
  const username = ref('');
  const userId = ref<number | null>(null);

  // 计算属性，用于快速判断用户是否登录
  const isLoggedIn = computed(() => !!accessToken.value);

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
      const { access_token, refresh_token } = await authService.login(usernameParam, password);
      const decoded = jwtDecode<{ sub: string; role: string; username: string }>(access_token);
      setTokens({ access_token, refresh_token });
      setRole(decoded.role);
      username.value = decoded.username;
      userId.value = parseInt(decoded.sub);
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

  return { accessToken, refreshTokenToken: refreshToken, role, username, userId, isLoggedIn, login, logout, refreshTokenMethod };
});