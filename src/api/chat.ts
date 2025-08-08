import request from '@/utils/request'

export interface ChatMessage {
  id: string | number
  role: 'user' | 'assistant'
  content: string
  references?: Array<{
    id: string
    citation: string
  }>
  createdAt: string
  created_at?: string // 后端返回的字段名
}

export interface ChatSession {
  id: string
  title: string
  lastMessage?: string
  createdAt: string
  updatedAt: string
  created_at?: string // 后端返回的字段名
  updated_at?: string // 后端返回的字段名
}

export interface ChatResponse {
  code: number
  message: string
  data: {
    user_message: ChatMessage
    assistant_message: ChatMessage
    references?: Array<{
      id: string
      title: string
      content: string
    }>
  }
}

// 流式消息事件类型
export interface StreamEvent {
  type:
    | 'thinking'
    | 'answer_start'
    | 'answer'
    | 'done'
    | 'error'
    | 'user_message'
    | 'assistant_message'
    | 'usage'
    | 'session_info'
  content?: string
  message_id?: string
  data?: any
  message?: string
}

// 获取聊天历史
export const getChatHistory = (mode: string = 'kb') => {
  return request.get<{
    code: number
    message: string
    data: ChatSession[]
  }>('/api/chat/sessions', { params: { mode } })
}

// 获取单个会话的消息
export const getChatMessages = (sessionId: string) => {
  return request.get<{
    code: number
    message: string
    data: ChatMessage[]
  }>(`/api/chat/sessions/${sessionId}`)
}

// 发送消息（非流式，保留兼容性）
export const sendMessage = (sessionId: string, content: string, mode: 'kb' | 'graph' = 'kb') => {
  return request.post<ChatResponse>(`/api/chat/sessions/${sessionId}/messages`, {
    content,
    mode,
  })
}

// 发送消息（流式）
export const sendMessageStream = (
  sessionId: string,
  content: string,
  mode: 'kb' | 'graph' = 'kb',
  onMessage: (event: StreamEvent) => void,
  onError?: (error: Error) => void,
  onComplete?: () => void,
): Promise<{ close: () => void }> => {
  const token = localStorage.getItem('token')

  return new Promise((resolve, reject) => {
    // 发送POST请求并处理流式响应
    fetch(
      `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/chat/sessions/${sessionId}/messages`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ content, mode }),
      },
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`)
        }

        if (!response.body) {
          throw new Error('No response body')
        }

        const reader = response.body.getReader()
        const decoder = new TextDecoder()

        const readStream = () => {
          reader
            .read()
            .then(({ done, value }) => {
              if (done) {
                onComplete?.()
                return
              }

              const chunk = decoder.decode(value)
              const lines = chunk.split('\n')

              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  try {
                    const data: StreamEvent = JSON.parse(line.slice(6))
                    onMessage(data)

                    if (data.type === 'done' || data.type === 'error') {
                      onComplete?.()
                      return
                    }
                  } catch (error) {
                    console.error('Failed to parse stream data:', error)
                  }
                }
              }

              readStream()
            })
            .catch((error) => {
              console.error('Stream read error:', error)
              onError?.(error)
            })
        }

        readStream()

        // 返回控制对象
        const controller = {
          close: () => reader.cancel(),
        }

        resolve(controller)
      })
      .catch((error) => {
        console.error('Failed to start stream:', error)
        onError?.(error)
        reject(error)
      })
  })
}

// 自动创建会话并发送消息（流式）
export const sendMessageAutoSession = (
  content: string,
  mode: 'kb' | 'graph' = 'kb',
  onMessage: (event: StreamEvent) => void,
  onError?: (error: Error) => void,
  onComplete?: () => void,
): Promise<EventSource> => {
  const token = localStorage.getItem('token')

  return new Promise((resolve, reject) => {
    // 发送POST请求创建会话并开始流式响应
    fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/chat/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ content, mode }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`)
        }

        if (!response.body) {
          throw new Error('No response body')
        }

        const reader = response.body.getReader()
        const decoder = new TextDecoder()

        const readStream = () => {
          reader
            .read()
            .then(({ done, value }) => {
              if (done) {
                onComplete?.()
                return
              }

              const chunk = decoder.decode(value)
              const lines = chunk.split('\n')

              for (const line of lines) {
                if (line.startsWith('data: ')) {
                  try {
                    const data: StreamEvent = JSON.parse(line.slice(6))
                    onMessage(data)

                    if (data.type === 'done' || data.type === 'error') {
                      onComplete?.()
                      return
                    }
                  } catch (error) {
                    console.error('Failed to parse stream data:', error)
                  }
                }
              }

              readStream()
            })
            .catch((error) => {
              console.error('Stream read error:', error)
              onError?.(error)
            })
        }

        readStream()

        // 返回一个模拟的EventSource对象
        const mockEventSource = {
          close: () => reader.cancel(),
          readyState: 1,
          url: '',
          withCredentials: false,
          CONNECTING: 0,
          OPEN: 1,
          CLOSED: 2,
          onopen: null,
          onmessage: null,
          onerror: null,
          addEventListener: () => {},
          removeEventListener: () => {},
          dispatchEvent: () => false,
        } as unknown as EventSource

        resolve(mockEventSource)
      })
      .catch((error) => {
        console.error('Failed to start stream:', error)
        onError?.(error)
        reject(error)
      })
  })
}

// 创建新会话
export const createChatSession = (title: string = '新对话', mode: 'kb' | 'graph' = 'kb') => {
  return request.post<{
    code: number
    message: string
    data: ChatSession
  }>('/api/chat/sessions', {
    title,
    mode,
  })
}

// 删除会话
export const deleteChatSession = (sessionId: string) => {
  return request.delete(`/api/chat/sessions/${sessionId}`)
}

// 清空所有会话
export const clearAllChatSessions = (mode: string = 'kb') => {
  return request.delete('/api/chat/sessions', { params: { mode } })
}

// 批量删除会话
export const deleteChatSessions = async (sessionIds: string[]) => {
  const promises = sessionIds.map((id) => deleteChatSession(id))
  return Promise.all(promises)
}

// 语音识别
export const speechToText = (audioBlob: Blob) => {
  const formData = new FormData()
  formData.append('audio', audioBlob)
  return request.post<{ text: string }>('/api/speech-to-text', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
}
