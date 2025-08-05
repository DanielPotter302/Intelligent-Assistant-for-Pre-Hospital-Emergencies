import request from '@/utils/request'
import type { SearchParams } from '@/types/knowledge'
import type { ApiResponse, PaginatedResponse } from '@/types/api'

// 知识库类别相关API
export const getKnowledgeCategories = () => {
  return request.get<ApiResponse<any[]>>('/api/knowledge/categories')
}

// 知识库内容相关API
export const getKnowledgeItems = (params: {
  category_id?: number
  content_type?: string
  search?: string
  page?: number
  page_size?: number
}) => {
  return request.get<ApiResponse<PaginatedResponse<any>>>('/api/knowledge/items', {
    params,
  })
}

export const getKnowledgeItem = (itemId: number) => {
  return request.get<ApiResponse<any>>(`/api/knowledge/items/${itemId}`)
}

// 管理员API - 知识内容管理
export const createKnowledgeItem = (data: {
  category_id: number
  title: string
  content: string
  content_type: string
  author?: string
  publisher?: string
  publish_date?: string
  isbn?: string
  description?: string
  cover_url?: string
  file_url?: string
  file_size?: number
}) => {
  return request.post<ApiResponse<any>>('/api/knowledge/admin/items', data)
}

export const updateKnowledgeItem = (
  itemId: number,
  data: {
    category_id?: number
    title?: string
    content?: string
    content_type?: string
    author?: string
    publisher?: string
    publish_date?: string
    isbn?: string
    description?: string
    cover_url?: string
    file_url?: string
    file_size?: number
    status?: string
  },
) => {
  return request.put<ApiResponse<any>>(`/api/knowledge/admin/items/${itemId}`, data)
}

export const deleteKnowledgeItem = (itemId: number) => {
  return request.delete<ApiResponse<any>>(`/api/knowledge/admin/items/${itemId}`)
}

// 视频相关API
export const getVideoLinks = (categoryId?: number) => {
  return request.get<ApiResponse<any[]>>('/api/knowledge/videos', {
    params: { category_id: categoryId },
  })
}

export const getVideoLink = (videoId: number) => {
  return request.get<ApiResponse<any>>(`/api/knowledge/videos/${videoId}`)
}

// 管理员API - 视频链接管理
export const createVideoLink = (data: {
  title: string
  description?: string
  video_url: string
  category_id: number
  sort_order?: number
}) => {
  return request.post<ApiResponse<any>>('/api/knowledge/admin/videos', data)
}

export const updateVideoLink = (
  videoId: number,
  data: {
    title?: string
    description?: string
    video_url?: string
    category_id?: number
    sort_order?: number
    status?: string
  },
) => {
  return request.put<ApiResponse<any>>(`/api/knowledge/admin/videos/${videoId}`, data)
}

export const deleteVideoLink = (videoId: number) => {
  return request.delete<ApiResponse<any>>(`/api/knowledge/admin/videos/${videoId}`)
}

// 书籍相关API
export const getBookLinks = () => {
  return request.get<ApiResponse<any[]>>('/api/knowledge/books')
}

export const getBookLink = (bookId: number) => {
  return request.get<ApiResponse<any>>(`/api/knowledge/books/${bookId}`)
}

// 管理员API - 书籍链接管理
export const createBookLink = (data: {
  title: string
  author?: string
  description?: string
  cover_url?: string
  book_url: string
  sort_order?: number
}) => {
  return request.post<ApiResponse<any>>('/api/knowledge/admin/books', data)
}

export const updateBookLink = (
  bookId: number,
  data: {
    title?: string
    author?: string
    description?: string
    cover_url?: string
    book_url?: string
    sort_order?: number
    status?: string
  },
) => {
  return request.put<ApiResponse<any>>(`/api/knowledge/admin/books/${bookId}`, data)
}

export const deleteBookLink = (bookId: number) => {
  return request.delete<ApiResponse<any>>(`/api/knowledge/admin/books/${bookId}`)
}

// 搜索相关API
export const searchKnowledge = (params: SearchParams) => {
  return request.get<ApiResponse<PaginatedResponse<any>>>('/api/knowledge/search', { params })
}

// 收藏相关API
export const addFavorite = (type: string, itemId: number) => {
  return request.post<ApiResponse<any>>('/api/knowledge/favorites', {
    favorite_type: type,
    favorite_id: itemId,
  })
}

export const removeFavorite = (favoriteId: number) => {
  return request.delete<ApiResponse<any>>(`/api/knowledge/favorites/${favoriteId}`)
}

export const getFavorites = (page = 1, pageSize = 10) => {
  return request.get<ApiResponse<PaginatedResponse<any>>>('/api/knowledge/favorites', {
    params: { page, page_size: pageSize },
  })
}

// 分享相关API
export const getShareLink = (resourceType: 'CHAPTER' | 'VIDEO', resourceId: number) => {
  return Promise.resolve({
    url: `https://example.com/${resourceType.toLowerCase()}/${resourceId}`,
  })
}

// 兼容旧API的别名
export const getBooksByCategory = (categoryId: number, page = 1, pageSize = 10) => {
  return getKnowledgeItems({
    category_id: categoryId,
    content_type: 'book',
    page,
    page_size: pageSize,
  })
}

export const getVideosByCategory = (categoryId: number, page = 1, pageSize = 10) => {
  return getVideoLinks(categoryId)
}

export const getVideoDetail = (id: number) => {
  return getVideoLink(id)
}

export const search = (params: SearchParams) => {
  return searchKnowledge(params)
}
