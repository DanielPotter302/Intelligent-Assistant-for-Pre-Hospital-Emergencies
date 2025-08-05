import request from '@/utils/request'
import type { ApiResponse } from '@/types/api'

export interface ContactMessageCreate {
  name: string
  email: string
  content: string
}

export interface ContactMessage {
  id: string
  name: string
  email: string
  content: string
  status: string
  admin_reply?: string
  replied_at?: string
  created_at: string
  updated_at: string
}

export interface ContactMessageUpdate {
  admin_reply: string
  status?: string
}

export interface MessageListResponse {
  messages: ContactMessage[]
  total: number
  page: number
  size: number
  pages: number
}

// 提交联系留言
export const submitContactMessage = (data: ContactMessageCreate): Promise<ApiResponse> => {
  return request.post('/api/contact', data)
}

// 获取留言列表（管理员）
export const getContactMessages = (params?: {
  status_filter?: string
  page?: number
  size?: number
}): Promise<ApiResponse<MessageListResponse>> => {
  return request.get('/api/admin/messages', { params })
}

// 更新留言（管理员回复）
export const updateContactMessage = (
  messageId: string,
  data: ContactMessageUpdate,
): Promise<ApiResponse<ContactMessage>> => {
  return request.put(`/api/admin/messages/${messageId}`, data)
}

// 标记留言为已读
export const markMessageAsRead = (messageId: string): Promise<ApiResponse> => {
  return request.patch(`/api/admin/messages/${messageId}/read`)
}
