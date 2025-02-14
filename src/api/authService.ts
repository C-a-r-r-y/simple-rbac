import apiClient from './axiosInstance';
import type { TokenResponse, HTTPValidationError } from './types';

const API_BASE_URL = '/auth';

export const authService = {
  async login(username: string, password: string): Promise<TokenResponse> {
    try {
      const response = await apiClient.post(`${API_BASE_URL}/login`, { username, password });
      return response.data;
    } catch (error: any) {
      if (error.response?.data?.detail?.[0]?.msg) {
        throw new Error(error.response.data.detail[0].msg);
      }
      throw new Error('Login failed');
    }
  },

  async refreshToken(refreshToken: string): Promise<TokenResponse> {
    try {
      const response = await apiClient.post(`${API_BASE_URL}/refresh`, { refresh_token: refreshToken });
      return response.data;
    } catch (error: any) {
      if (error.response?.data?.detail?.[0]?.msg) {
        throw new Error(error.response.data.detail[0].msg);
      }
      throw new Error('Token refresh failed');
    }
  }
};