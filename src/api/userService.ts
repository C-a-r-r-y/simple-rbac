import apiClient from './axiosInstance';
import type { UserResponse, UserCreate, UserUpdate } from './types';

const API_BASE_URL = '/users';

export const userService = {
  async getUsers(page = 1, limit = 100, role?: string): Promise<UserResponse[]> {
    const response = await apiClient.get(API_BASE_URL, {
      params: { page, limit, role }
    });
    return response.data;
  },

  async createUser(userData: UserCreate): Promise<UserResponse> {
    const response = await apiClient.post(API_BASE_URL, userData);
    return response.data;
  },

  async updateUser(userId: number, userData: UserUpdate): Promise<UserResponse> {
    const response = await apiClient.put(`${API_BASE_URL}/${userId}`, userData);
    return response.data;
  },

  async deleteUser(userId: number): Promise<void> {
    await apiClient.delete(`${API_BASE_URL}/${userId}`);
  }
};