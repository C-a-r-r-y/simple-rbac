import axios from 'axios';

const API_BASE_URL = '/api/auth';

export const authService = {
  async login(username: string, password: string) {
    const response = await axios.post(`${API_BASE_URL}/login`, { username, password });
    return response.data;
  },

  async refreshToken(refreshToken: string) {
    const response = await axios.post(`${API_BASE_URL}/refresh`, { refresh_token: refreshToken });
    return response.data;
  }
};