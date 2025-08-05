// 知识库类别
export interface KnowledgeCategory {
  id: number
  name: string
  description?: string
  parent_id?: number
  sort_order: number
  status: string
  created_at: string
  children?: KnowledgeCategory[]
}

// 知识库内容
export interface KnowledgeItem {
  id: number
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
  view_count: number
  download_count: number
  status: string
  created_at: string
  updated_at: string
}

// 视频链接
export interface VideoLink {
  id: number
  title: string
  description?: string
  video_url: string
  category_id: number
  sort_order: number
  status: string
  created_at: string
}

// 书籍链接
export interface BookLink {
  id: number
  title: string
  author?: string
  description?: string
  cover_url?: string
  book_url: string
  sort_order: number
  status: string
  created_at: string
}

// 用户收藏
export interface UserFavorite {
  id: number
  user_id: number
  favorite_type: string
  favorite_id: number
  created_at: string
}

// 收藏
export interface Favorite {
  id: number
  resourceType: 'CHAPTER' | 'VIDEO' | 'ITEM'
  resourceId: number
  title: string
  collectedAt: string
}

// 搜索结果
export interface SearchResult {
  id: number
  title: string
  content: string
  author?: string
  category_id: number
}

// 搜索参数
export interface SearchParams {
  keyword: string
  page?: number
  page_size?: number
}
