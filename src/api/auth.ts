import request from '@/utils/request'
import type {
  ApiResponse,
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  User,
  RefreshTokenRequest,
  RefreshTokenResponse,
} from '@/types/api'

// 用户注册
export function register(
  data: RegisterRequest,
): Promise<
  ApiResponse<{ userId: string; username: string; email: string; role: string; createdAt: string }>
> {
  return request.post('/api/auth/register', data)
}

// 用户登录
export function login(data: LoginRequest): Promise<ApiResponse<LoginResponse>> {
  return request.post('/api/auth/login', data)
}

// 获取当前用户信息
export function getCurrentUser(): Promise<ApiResponse<User>> {
  return request.get('/api/users/profile')
}

// 刷新Token
export function refreshToken(
  data: RefreshTokenRequest,
): Promise<ApiResponse<RefreshTokenResponse>> {
  return request.post('/api/auth/refresh', data)
}

// 用户登出（前端处理，清除本地token）
export function logout(): Promise<ApiResponse<null>> {
  // JWT登出通常在前端处理，直接返回成功响应
  return Promise.resolve({
    code: 200,
    message: 'Logout successful',
    data: null,
    timestamp: new Date().toISOString(),
  })
}

// Token管理工具函数
export const tokenManager = {
  // 获取Token
  getToken(): string | null {
    return localStorage.getItem('token')
  },

  // 设置Token
  setToken(token: string): void {
    localStorage.setItem('token', token)
  },

  // 获取RefreshToken
  getRefreshToken(): string | null {
    return localStorage.getItem('refreshToken')
  },

  // 设置RefreshToken
  setRefreshToken(refreshToken: string): void {
    localStorage.setItem('refreshToken', refreshToken)
  },

  // 清除所有Token
  clearTokens(): void {
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
  },

  // 检查Token是否存在
  hasToken(): boolean {
    return !!this.getToken()
  },
}
