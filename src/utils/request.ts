import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'

interface RequestInstance extends AxiosInstance {
  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T>
  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T>
  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>
  put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>
}

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 60000, // 增加到60秒，因为LLM API可能需要更长时间
  headers: {
    'Content-Type': 'application/json',
  },
}) as RequestInstance

// 是否正在刷新Token
let isRefreshing = false
// 失败请求队列
let failedQueue: Array<{
  resolve: (value: any) => void
  reject: (reason: any) => void
}> = []

// 处理队列中的请求
const processQueue = (error: any, token: string | null = null) => {
  failedQueue.forEach(({ resolve, reject }) => {
    if (error) {
      reject(error)
    } else {
      resolve(token)
    }
  })

  failedQueue = []
}

// 刷新Token
const refreshAuthToken = async (): Promise<string | null> => {
  try {
    const refreshToken = localStorage.getItem('refreshToken')
    if (!refreshToken) {
      throw new Error('No refresh token available')
    }

    const response = await axios.post(`${service.defaults.baseURL}/auth/refresh`, {
      refreshToken,
    })

    const { token, refreshToken: newRefreshToken } = response.data.data
    localStorage.setItem('token', token)
    localStorage.setItem('refreshToken', newRefreshToken)

    return token
  } catch (error) {
    // 刷新失败，清除所有token并跳转到登录页
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    window.location.href = '/login'
    throw error
  }
}

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 添加token到请求头
    const token = localStorage.getItem('token')
    if (token) {
      config.headers = config.headers || {}
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  },
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    // 统一处理响应数据
    const res = response.data

    // 如果响应格式不符合预期，直接返回
    if (typeof res !== 'object' || res === null) {
      return res
    }

    // 处理业务错误
    if (res.code && res.code !== 200 && res.code !== 201) {
      const errorMessage = res.message || 'Unknown error'

      // 根据错误码进行不同处理
      switch (res.code) {
        case 401:
          // Token过期或无效，不显示错误消息，由Token刷新逻辑处理
          break
        case 403:
          ElMessage.error('权限不足，请联系管理员')
          break
        case 429:
          ElMessage.error('请求过于频繁，请稍后再试')
          break
        case 500:
          ElMessage.error('服务器错误，请稍后再试')
          break
        default:
          ElMessage.error(errorMessage)
      }

      return Promise.reject(new Error(errorMessage))
    }

    return res
  },
  async (error) => {
    const originalRequest = error.config

    // 处理网络错误
    if (!error.response) {
      ElMessage.error('网络错误，请检查网络连接')
      return Promise.reject(error)
    }

    const { status } = error.response

    // 处理401错误（Token过期）
    if (status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // 如果正在刷新Token，将请求加入队列
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            originalRequest.headers['Authorization'] = `Bearer ${token}`
            return service(originalRequest)
          })
          .catch((err) => {
            return Promise.reject(err)
          })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const newToken = await refreshAuthToken()
        processQueue(null, newToken)

        // 重新发送原始请求
        originalRequest.headers['Authorization'] = `Bearer ${newToken}`
        return service(originalRequest)
      } catch (refreshError) {
        processQueue(refreshError, null)
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    // 处理其他HTTP错误
    switch (status) {
      case 403:
        ElMessage.error('权限不足，请联系管理员')
        break
      case 404:
        ElMessage.error('请求的资源不存在')
        break
      case 429:
        ElMessage.error('请求过于频繁，请稍后再试')
        break
      case 500:
        ElMessage.error('服务器错误，请稍后再试')
        break
      default:
        ElMessage.error(error.response?.data?.message || '请求失败')
    }

    return Promise.reject(error)
  },
)

export default service
