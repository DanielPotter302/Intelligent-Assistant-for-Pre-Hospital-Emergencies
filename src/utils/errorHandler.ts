import { ElMessage, ElNotification } from 'element-plus'

// 错误类型定义
export interface ApiError {
  code: number
  message: string
  data?: any
  timestamp?: string
}

export interface NetworkError {
  type: 'network'
  message: string
  originalError: Error
}

export interface ValidationError {
  type: 'validation'
  field: string
  message: string
}

export type AppError = ApiError | NetworkError | ValidationError

// 错误处理器类
export class ErrorHandler {
  // 处理API错误
  static handleApiError(error: any): void {
    if (!error.response) {
      // 网络错误
      this.handleNetworkError(error)
      return
    }

    const { status, data } = error.response
    const errorMessage = data?.message || this.getDefaultErrorMessage(status)

    switch (status) {
      case 400:
        ElMessage.error(`请求参数错误: ${errorMessage}`)
        break
      case 401:
        ElMessage.error('登录已过期，请重新登录')
        // 这里可以触发重新登录逻辑
        break
      case 403:
        ElMessage.error('权限不足，请联系管理员')
        break
      case 404:
        ElMessage.error('请求的资源不存在')
        break
      case 429:
        ElMessage.warning('请求过于频繁，请稍后再试')
        break
      case 500:
        ElMessage.error('服务器内部错误，请稍后再试')
        this.reportError(error)
        break
      case 502:
      case 503:
      case 504:
        ElMessage.error('服务暂时不可用，请稍后再试')
        break
      default:
        ElMessage.error(errorMessage || '请求失败')
    }
  }

  // 处理网络错误
  static handleNetworkError(error: Error): void {
    console.error('Network error:', error)

    if (error.message.includes('timeout')) {
      ElMessage.error('请求超时，请检查网络连接')
    } else if (error.message.includes('Network Error')) {
      ElMessage.error('网络连接失败，请检查网络设置')
    } else {
      ElMessage.error('网络错误，请稍后重试')
    }
  }

  // 处理表单验证错误
  static handleValidationError(errors: ValidationError[]): void {
    if (errors.length === 1) {
      ElMessage.error(errors[0].message)
    } else {
      ElNotification.error({
        title: '表单验证失败',
        message: errors.map((e) => `${e.field}: ${e.message}`).join('\n'),
      })
    }
  }

  // 处理业务逻辑错误
  static handleBusinessError(message: string, type: 'error' | 'warning' = 'error'): void {
    if (type === 'warning') {
      ElMessage.warning(message)
    } else {
      ElMessage.error(message)
    }
  }

  // 处理成功消息
  static handleSuccess(message: string, showNotification = false): void {
    if (showNotification) {
      ElNotification.success({
        title: '操作成功',
        message,
      })
    } else {
      ElMessage.success(message)
    }
  }

  // 获取默认错误消息
  private static getDefaultErrorMessage(status: number): string {
    const errorMessages: Record<number, string> = {
      400: '请求参数错误',
      401: '未授权访问',
      403: '权限不足',
      404: '资源不存在',
      405: '请求方法不允许',
      408: '请求超时',
      409: '资源冲突',
      422: '请求参数验证失败',
      429: '请求过于频繁',
      500: '服务器内部错误',
      502: '网关错误',
      503: '服务不可用',
      504: '网关超时',
    }

    return errorMessages[status] || '未知错误'
  }

  // 错误上报（可选）
  private static reportError(error: any): void {
    // 这里可以集成错误监控服务，如Sentry
    console.error('Error reported:', {
      message: error.message,
      stack: error.stack,
      url: window.location.href,
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString(),
    })
  }

  // 创建错误对象
  static createError(code: number, message: string, data?: any): ApiError {
    return {
      code,
      message,
      data,
      timestamp: new Date().toISOString(),
    }
  }

  // 检查是否为API错误
  static isApiError(error: any): error is ApiError {
    return error && typeof error.code === 'number' && typeof error.message === 'string'
  }

  // 检查是否为网络错误
  static isNetworkError(error: any): error is NetworkError {
    return error && error.type === 'network'
  }

  // 检查是否为验证错误
  static isValidationError(error: any): error is ValidationError {
    return error && error.type === 'validation'
  }
}

// 全局错误处理函数
export const handleGlobalError = (error: any): void => {
  console.error('Global error:', error)

  if (ErrorHandler.isApiError(error)) {
    ErrorHandler.handleApiError(error)
  } else if (ErrorHandler.isNetworkError(error)) {
    ErrorHandler.handleNetworkError(error.originalError)
  } else if (ErrorHandler.isValidationError(error)) {
    ErrorHandler.handleValidationError([error])
  } else {
    ErrorHandler.handleBusinessError('发生未知错误，请稍后重试')
  }
}

// 异步操作错误处理装饰器
export const withErrorHandling = <T extends (...args: any[]) => Promise<any>>(
  fn: T,
  customErrorHandler?: (error: any) => void
): T => {
  return (async (...args: any[]) => {
    try {
      return await fn(...args)
    } catch (error) {
      if (customErrorHandler) {
        customErrorHandler(error)
      } else {
        handleGlobalError(error)
      }
      throw error
    }
  }) as T
}

// 重试机制
export const withRetry = <T extends (...args: any[]) => Promise<any>>(
  fn: T,
  maxRetries = 3,
  delay = 1000
): T => {
  return (async (...args: any[]) => {
    let lastError: any

    for (let i = 0; i <= maxRetries; i++) {
      try {
        return await fn(...args)
      } catch (error) {
        lastError = error

        if (i === maxRetries) {
          break
        }

        // 只对特定错误进行重试
        if ((error as any).response?.status >= 400 && (error as any).response?.status < 500) {
          break // 客户端错误不重试
        }

        await new Promise((resolve) => setTimeout(resolve, delay * Math.pow(2, i)))
      }
    }

    throw lastError
  }) as T
}
