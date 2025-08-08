import request from '@/utils/request'

export interface LLMConfig {
  id: string
  module_name: string
  display_name: string
  api_key: string
  base_url: string
  model_name: string
  temperature: string
  max_tokens: string
  is_enabled: boolean
  enable_thinking: boolean
  description?: string
  created_at: string
  updated_at: string
}

export interface LLMConfigCreate {
  module_name: string
  display_name: string
  api_key: string
  base_url: string
  model_name: string
  temperature: string
  max_tokens: string
  is_enabled: boolean
  enable_thinking: boolean
  description?: string
}

export interface LLMConfigUpdate {
  display_name?: string
  api_key?: string
  base_url?: string
  model_name?: string
  temperature?: string
  max_tokens?: string
  is_enabled?: boolean
  enable_thinking?: boolean
  description?: string
}

export const llmConfigApi = {
  // 获取所有LLM配置
  getConfigs: () => {
    return request.get<{ data: LLMConfig[] }>('/api/admin/llm/configs')
  },

  // 获取单个LLM配置
  getConfig: (id: string) => {
    return request.get<LLMConfig>(`/api/admin/llm/configs/${id}`)
  },

  // 创建LLM配置
  createConfig: (data: LLMConfigCreate) => {
    return request.post<LLMConfig>('/api/admin/llm/configs', data)
  },

  // 更新LLM配置
  updateConfig: (id: string, data: LLMConfigUpdate) => {
    return request.put<LLMConfig>(`/api/admin/llm/configs/${id}`, data)
  },

  // 删除LLM配置
  deleteConfig: (id: string) => {
    return request.delete(`/api/admin/llm/configs/${id}`)
  },

  // 初始化默认配置
  initDefaultConfigs: () => {
    return request.post('/api/admin/llm/configs/init-default')
  },
}
