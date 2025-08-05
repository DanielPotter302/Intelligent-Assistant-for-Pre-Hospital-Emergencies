// API统一响应格式
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
  timestamp: string
}

// 分页响应格式
export interface PaginatedResponse<T> {
  total: number
  page: number
  pageSize: number
  records: T[]
}

// 用户相关类型
export interface User {
  id: string
  username: string
  email: string
  role: string
  realName?: string
  phone?: string
  department?: string
  profileAvatar?: string
  status: string
  emailVerified: boolean
  lastLoginAt: string
  createdAt: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user: User
}

export interface RefreshTokenRequest {
  refreshToken: string
}

export interface RefreshTokenResponse {
  token: string
  refreshToken: string
  expiresIn: number
}

// 分诊相关类型
export interface PatientInfo {
  name: string
  idCard?: string
  age: number
  gender: 'male' | 'female' | 'other'
  weight?: number
  height?: number
  allergies?: string[]
  medications?: string[]
  medicalHistory?: string[]
}

export interface VitalSigns {
  heartRate: number
  bloodPressure: {
    systolic: number
    diastolic: number
  }
  respiratoryRate: number
  temperature: number
  oxygenSaturation?: number
  glucoseLevel?: number
}

export interface SymptomInfo {
  chiefComplaint: string
  symptoms: string[]
  painLevel?: number
  duration?: string
  mechanism?: string
  additionalInfo?: string
}

export interface TriageRequest {
  patientInfo: PatientInfo
  vitalSigns: VitalSigns
  symptomInfo: SymptomInfo
  emergencyContext?: string
}

// 后端API格式的分诊请求
export interface BackendTriageRequest {
  patient_info: {
    name: string
    id_card?: string
    age: number
    gender: string
    weight?: number
    height?: number
    allergies?: string[]
    medications?: string[]
    medical_history?: string[]
  }
  vital_signs: {
    heart_rate?: number
    blood_pressure_systolic?: number
    blood_pressure_diastolic?: number
    respiratory_rate?: number
    temperature?: number
    oxygen_saturation?: number
    blood_glucose?: number
  }
  symptom_info: {
    chief_complaint: string
    symptoms?: string[]
    pain_level?: number
    symptom_duration?: string
  }
}

export interface TriageResult {
  level: 'red' | 'orange' | 'yellow' | 'green'
  levelDescription: string
  severity: string
  recommendations: string[]
  immediateActions: string[]
  calculatedScores: Array<{
    name: string
    score: number
    interpretation: string
  }>
  referenceGuidelines: string[]
  callEmergency: boolean
  estimatedWaitTime: string
}

export interface TriageResponse {
  analysis: string
  triageResult: TriageResult
  confidence: number
  riskFactors: string[]
  followUpAdvice: string
  reasoning?: string[]
}

export interface TriageHistoryItem {
  id: string
  patientName: string
  chiefComplaint: string
  triageLevel: string
  severity: string
  confidence: number
  createdAt: string
}

// 医疗计算器类型
export interface CalculatorRequest {
  [key: string]: any
}

export interface CalculatorResponse {
  type: string
  score: number
  interpretation: string
  riskLevel: string
  recommendations: string[]
}

export interface CalculatorInfo {
  type: string
  name: string
  description: string
  category: string
}

// 紧急情况相关类型
export interface EmergencySessionRequest {
  emergencyType: string
  location?: string
  patientInfo?: {
    age?: number
    gender?: string
    consciousness?: string
  }
  description: string
}

export interface EmergencyStep {
  stepNumber: number
  instruction: string
  duration: number
  critical: boolean
}

export interface EmergencyGuidance {
  priority: string
  steps: EmergencyStep[]
}

export interface EmergencySessionResponse {
  sessionId: string
  emergencyType: string
  status: string
  initialGuidance: EmergencyGuidance
  createdAt: string
}

export interface EmergencyMessageRequest {
  message: string
  messageType?: string
  urgency?: string
}

export interface EmergencyMessageResponse {
  messageId: string
  guidance: {
    response: string
    steps: EmergencyStep[]
    nextActions: string[]
    warnings: string[]
  }
  createdAt: string
}

export interface EmergencyEquipment {
  id: string
  type: string
  name: string
  location: {
    name: string
    address: string
    latitude: number
    longitude: number
    distance: number
  }
  status: string
  contact: string
  instructions: string
  availability: string
}

export interface EmergencyScenario {
  type: string
  name: string
  description: string
  category: string
  severity: string
  keywords: string[]
}

// 聊天相关类型
export interface ChatSessionRequest {
  title?: string
  mode?: 'kb' | 'general'
}

export interface ChatSessionResponse {
  sessionId: string
  title: string
  mode: string
  status: string
  createdAt: string
}

export interface ChatMessageRequest {
  content: string
  mode?: string
}

export interface ChatReference {
  id: string
  citation: string
  title: string
  content?: string
  url?: string
}

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  mode: string
  references?: ChatReference[]
  aiConfidence?: number
  aiModelVersion?: string
  responseTime?: number
  createdAt: string
}

export interface ChatMessageResponse {
  message: ChatMessage
  references?: ChatReference[]
}

export interface ChatSession {
  id: string
  title: string
  mode: string
  status: string
  messageCount: number
  lastMessageAt: string
  createdAt: string
  updatedAt: string
}

export interface QuickQuestionRequest {
  question: string
  mode?: string
}

export interface QuickQuestionResponse {
  question: string
  answer: string
  references: ChatReference[]
  confidence: number
  responseTime: number
}

// 知识库相关类型
export interface KnowledgeCategory {
  id: number
  name: string
  description: string
  icon: string
  parentId?: number
  sortOrder: number
  status: string
  children?: KnowledgeCategory[]
}

export interface Book {
  id: number
  categoryId: number
  title: string
  author: string
  publisher: string
  publishDate: string
  isbn: string
  description: string
  coverUrl: string
  fileUrl: string
  fileSize: number
  chapterCount: number
  viewCount: number
  downloadCount: number
  status: string
  createdAt: string
}

export interface Chapter {
  id: number
  bookId: number
  title: string
  content?: string
  summary: string
  chapterNumber: number
  sortOrder: number
  viewCount: number
  status: string
  book?: {
    id: number
    title: string
    author: string
  }
}

export interface Video {
  id: number
  categoryId: number
  title: string
  description: string
  videoUrl: string
  thumbnailUrl: string
  tags: string[]
  duration: number
  fileSize: number
  resolution: string
  viewCount: number
  likeCount: number
  status: string
  createdAt: string
}

export interface KnowledgeSearchRequest {
  query: string
  type?: 'all' | 'book' | 'video' | 'chapter'
  limit?: number
}

export interface KnowledgeSearchResult {
  id: string
  type: string
  title: string
  content: string
  relevanceScore: number
  source: any
  url: string
}

export interface KnowledgeSearchResponse {
  query: string
  total: number
  results: KnowledgeSearchResult[]
}

export interface KnowledgeStatistics {
  totalBooks: number
  totalChapters: number
  totalVideos: number
  totalViews: number
  popularBooks: Array<{
    id: number
    title: string
    author: string
    viewCount: number
    description: string
  }>
  popularVideos: Array<{
    id: number
    title: string
    viewCount: number
    duration: number
    description: string
  }>
  recentlyAdded: Array<{
    type: string
    title: string
    createdAt: string
  }>
}

// 首页相关类型
export interface Feature {
  id: string
  title: string
  description: string
  icon: string
  features: string[]
}

export interface WorkflowStep {
  step: number
  title: string
  description: string
  icon: string
  details: string[]
}

export interface Advantage {
  title: string
  description: string
  icon: string
  metrics: Array<{
    label: string
    value: string
  }>
}

export interface ContactInfo {
  company: string
  address: string
  phone: string
  email: string
  website: string
  supportHours: string
  emergencyContact: string
  socialMedia: {
    wechat: string
    weibo: string
    linkedin: string
  }
}

export interface MessageRequest {
  name: string
  email: string
  phone?: string
  company?: string
  subject: string
  message: string
  type?: 'inquiry' | 'feedback' | 'support'
}

export interface MessageResponse {
  messageId: string
  status: string
  estimatedResponseTime: string
}

// 系统管理相关类型
export interface SystemStatistics {
  overview: {
    totalUsers: number
    activeUsers: number
    totalSessions: number
    totalTriages: number
  }
  userStats: {
    newUsersToday: number
    newUsersThisWeek: number
    newUsersThisMonth: number
    userGrowthRate: number
  }
  usageStats: {
    triagesToday: number
    triagesThisWeek: number
    triagesThisMonth: number
    averageResponseTime: number
  }
  systemHealth: {
    cpuUsage: number
    memoryUsage: number
    diskUsage: number
    uptime: string
  }
}

export interface AdminUser {
  id: string
  username: string
  email: string
  realName: string
  role: string
  status: string
  department: string
  lastLoginAt: string
  createdAt: string
  triageCount: number
  chatCount: number
}

export interface SystemLog {
  id: string
  level: 'INFO' | 'WARN' | 'ERROR'
  message: string
  module: string
  userId: string
  ip: string
  userAgent: string
  timestamp: string
  details: any
}

export interface DashboardData {
  overview: {
    totalUsers: number
    activeUsers: number
    totalSessions: number
    totalTriages: number
  }
  recentActivity: Array<{
    type: string
    message: string
    timestamp: string
  }>
  systemAlerts: Array<{
    level: string
    message: string
    timestamp: string
  }>
  performanceMetrics: {
    averageResponseTime: number
    errorRate: number
    throughput: number
  }
}

// 健康检查类型
export interface HealthStatus {
  status: string
  timestamp: string
  version: string
  services: {
    database: string
    redis: string
    ai_service: string
  }
  uptime: string
}
