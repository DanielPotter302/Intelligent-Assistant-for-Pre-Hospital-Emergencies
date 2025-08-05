import axios from 'axios'

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 5000,
})

// 获取功能总览
export const getFeatures = () => {
  return api.get('/api/features')
}

// 获取工作流程
export const getWorkflows = () => {
  return api.get('/api/workflows')
}

// 获取价值与优势
export const getAdvantages = () => {
  return api.get('/api/advantages')
}

// 获取联系方式
export const getContactInfo = () => {
  return api.get('/api/contact-info')
}

// 提交留言
export interface MessageForm {
  name: string
  email: string
  content: string
}

export const submitMessage = (data: MessageForm) => {
  return api.post('/api/messages', data)
}
