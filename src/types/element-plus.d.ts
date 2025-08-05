declare module 'element-plus' {
  import type { Component } from 'vue'
  
  export const ElMessage: {
    success(message: string): void
    warning(message: string): void
    info(message: string): void
    error(message: string): void
  }

  export const ElMessageBox: {
    confirm(message: string, title?: string): Promise<void>
    alert(message: string, title?: string): Promise<void>
  }

  export const ElNotification: {
    success(options: { title?: string; message: string }): void
    warning(options: { title?: string; message: string }): void
    info(options: { title?: string; message: string }): void
    error(options: { title?: string; message: string }): void
  }
} 