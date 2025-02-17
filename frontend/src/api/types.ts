export interface UserResponse {
  id: number;
  username: string;
  role: UserRole;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  username: string;
  password: string;
  role?: UserRole;
  description?: string;
}

export interface UserUpdate {
  username?: string;
  role?: UserRole;
  description?: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  access_token_exp: number;
  refresh_token_exp: number;
}

export interface HTTPValidationError {
  detail: ValidationError[];
}

export interface ValidationError {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export type UserRole = 'system_admin' | 'admin' | 'user';