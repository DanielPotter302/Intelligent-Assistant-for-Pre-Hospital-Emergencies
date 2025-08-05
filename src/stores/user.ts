import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginRequest, RegisterRequest } from '@/types/api'
import { login, register, getCurrentUser, logout, tokenManager } from '@/api/auth'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref<User | null>(null)
  const isLoading = ref(false)

  // 计算属性
  const isLoggedIn = computed(() => !!user.value && tokenManager.hasToken())
  const userRole = computed(() => user.value?.role || '')
  const userName = computed(() => user.value?.realName || user.value?.username || '')

  // Actions

  // 登录
  const loginUser = async (loginData: LoginRequest): Promise<boolean> => {
    try {
      isLoading.value = true
      const response = await login(loginData)

      if (response.code === 200) {
        const { access_token, refresh_token, user: userData } = response.data

        // 保存token
        tokenManager.setToken(access_token)
        tokenManager.setRefreshToken(refresh_token)

        // 保存用户信息
        user.value = userData

        ElMessage.success('登录成功')
        return true
      } else {
        ElMessage.error(response.message || '登录失败')
        return false
      }
    } catch (error: any) {
      console.error('Login error:', error)
      ElMessage.error(error.message || '登录失败')
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 注册
  const registerUser = async (registerData: RegisterRequest): Promise<boolean> => {
    try {
      isLoading.value = true
      const response = await register(registerData)

      if (response.code === 200 || response.code === 201) {
        ElMessage.success('注册成功，请登录')
        return true
      } else {
        ElMessage.error(response.message || '注册失败')
        return false
      }
    } catch (error: any) {
      console.error('Register error:', error)
      ElMessage.error(error.message || '注册失败')
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 获取用户信息
  const fetchUserInfo = async (): Promise<boolean> => {
    try {
      if (!tokenManager.hasToken()) {
        return false
      }

      isLoading.value = true
      const response = await getCurrentUser()

      if (response.code === 200) {
        user.value = response.data
        return true
      } else {
        // 获取用户信息失败，清除token
        await logoutUser()
        return false
      }
    } catch (error: any) {
      console.error('Fetch user info error:', error)
      // 获取用户信息失败，清除token
      await logoutUser()
      return false
    } finally {
      isLoading.value = false
    }
  }

  // 登出
  const logoutUser = async (): Promise<void> => {
    try {
      // 调用登出接口
      if (tokenManager.hasToken()) {
        await logout()
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      // 清除本地数据
      user.value = null
      tokenManager.clearTokens()
      ElMessage.success('已退出登录')
    }
  }

  // 初始化用户状态（应用启动时调用）
  const initializeUser = async (): Promise<void> => {
    if (tokenManager.hasToken()) {
      await fetchUserInfo()
    }
  }

  // 检查用户权限
  const hasPermission = (requiredRole: string): boolean => {
    if (!user.value) return false

    // 简单的角色权限检查，可以根据需要扩展
    const roleHierarchy: Record<string, number> = {
      user: 1,
      admin: 2,
      super_admin: 3,
    }

    const userRoleLevel = roleHierarchy[user.value.role] || 0
    const requiredRoleLevel = roleHierarchy[requiredRole] || 0

    return userRoleLevel >= requiredRoleLevel
  }

  // 更新用户信息
  const updateUserInfo = (userData: Partial<User>): void => {
    if (user.value) {
      user.value = { ...user.value, ...userData }
    }
  }

  return {
    // 状态
    user,
    isLoading,

    // 计算属性
    isLoggedIn,
    userRole,
    userName,

    // Actions
    loginUser,
    registerUser,
    fetchUserInfo,
    logoutUser,
    initializeUser,
    hasPermission,
    updateUserInfo,
  }
})
