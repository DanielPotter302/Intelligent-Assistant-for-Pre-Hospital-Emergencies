import request from '@/utils/request'
import { emergencyScenarios } from '@/config/emergency'
import type {
  ApiResponse,
  EmergencySessionRequest,
  EmergencySessionResponse,
  EmergencyMessageRequest,
  EmergencyMessageResponse,
  EmergencyEquipment,
  EmergencyScenario,
} from '@/types/api'

// 重新导出类型以保持向后兼容
export interface EmergencyMessage {
  id: string | number
  role: 'user' | 'assistant'
  content: string
  steps?: string[]
  createdAt: string
}

export interface EmergencyResponse {
  message: EmergencyMessage
  references?: Array<{
    id: string
    title: string
    content: string
  }>
}

export interface EmergencySession {
  id: string
  title: string
  scenario: string
  lastMessage: string
  createdAt: string
  updatedAt: string
}

// 流式消息事件类型
export interface EmergencyStreamEvent {
  type:
    | 'thinking'
    | 'answer_start'
    | 'answer'
    | 'done'
    | 'error'
    | 'user_message'
    | 'assistant_message'
    | 'usage'
  content?: string
  message_id?: string
  data?: any
  message?: string
}

// 创建紧急会话
export async function createEmergencySession(
  data: EmergencySessionRequest,
): Promise<EmergencySession> {
  const response = await request.post('/api/emergency/sessions', data)
  return response.data
}

// 发送紧急指导消息
export function sendEmergencyMessage(
  sessionId: string,
  data: EmergencyMessageRequest,
): Promise<ApiResponse<EmergencyMessageResponse>> {
  return request.post(`/api/emergency/sessions/${sessionId}/messages`, data)
}

// 获取附近医疗设备
export async function getNearbyEquipment(params: {
  latitude: number
  longitude: number
  radius?: number
  type?: string
}): Promise<ApiResponse<EmergencyEquipment[]>> {
  return request.get('/api/emergency/equipment/nearby', { params })
}

// 获取紧急场景列表
export async function getEmergencyScenarios(): Promise<ApiResponse<EmergencyScenario[]>> {
  return request.get('/api/emergency/scenarios')
}

// 发送应急指导消息（流式）
export const sendMessageStream = (
  sessionId: string,
  content: string,
  scenario: keyof typeof emergencyScenarios,
  onMessage: (event: EmergencyStreamEvent) => void,
  onError?: (error: Error) => void,
  onComplete?: () => void,
): Promise<{ close: () => void }> => {
  const token = localStorage.getItem('token')

  return new Promise((resolve, reject) => {
    // 发送POST请求并处理流式响应
    fetch(
      `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/emergency/sessions/${sessionId}/messages`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ content, scenario }),
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
                    const data: EmergencyStreamEvent = JSON.parse(line.slice(6))
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

/**
 * 发送应急指导消息（保持向后兼容）
 */
export async function sendMessage(
  sessionId: string,
  content: string,
  _scenario: keyof typeof emergencyScenarios,
): Promise<EmergencyResponse> {
  // 调用后端API，为AI响应设置更长的超时时间
  const response = await request.post(
    `/api/emergency/sessions/${sessionId}/messages`,
    {
      content,
    },
    {
      timeout: 60000, // 60秒超时，给AI足够的响应时间
    },
  )

  // 转换后端响应格式为前端期望的格式
  if (response.data && response.data.assistant_message) {
    const assistantMsg = response.data.assistant_message
    return {
      message: {
        id: assistantMsg.id,
        role: assistantMsg.role,
        content: assistantMsg.content,
        steps: assistantMsg.steps,
        createdAt: assistantMsg.created_at,
      },
    }
  }

  throw new Error('Invalid response format')
}

/**
 * 获取历史消息
 */
export async function getMessages(sessionId: string): Promise<EmergencyMessage[]> {
  const response = await request.get(`/api/emergency/sessions/${sessionId}`)

  // 转换后端响应格式为前端期望的格式
  if (response.data && Array.isArray(response.data)) {
    return response.data.map((msg: any) => ({
      id: msg.id,
      role: msg.role,
      content: msg.content,
      steps: msg.steps,
      createdAt: msg.created_at || msg.createdAt,
    }))
  }

  return []
}

/**
 * 获取会话列表
 */
export async function getSessions(): Promise<EmergencySession[]> {
  const response = await request.get('/api/emergency/sessions')

  // 转换后端响应格式为前端期望的格式
  if (response.data && Array.isArray(response.data)) {
    return response.data.map((session: any) => ({
      id: session.id,
      title: session.title,
      scenario: session.scenario_type,
      lastMessage: session.last_message || '',
      createdAt: session.created_at,
      updatedAt: session.updated_at,
    }))
  }

  return []
}

/**
 * 创建新会话
 */
export async function createSession(
  scenario: keyof typeof emergencyScenarios,
): Promise<EmergencySession> {
  const sessionData = {
    scenario_type: scenario,
    title: emergencyScenarios[scenario].title,
  }
  const response = await request.post('/api/emergency/sessions', sessionData, {
    timeout: 30000, // 30秒超时，创建会话可能需要生成初始消息
  })

  // 转换后端响应格式为前端期望的格式
  if (response.data) {
    const sessionData = response.data
    return {
      id: sessionData.id,
      title: sessionData.title,
      scenario: sessionData.scenario_type,
      lastMessage: sessionData.last_message || '',
      createdAt: sessionData.created_at,
      updatedAt: sessionData.updated_at,
    }
  }

  throw new Error('Invalid response format')
}

/**
 * 删除会话
 */
export async function deleteSession(sessionId: string): Promise<void> {
  await request.delete(`/api/emergency/sessions/${sessionId}`)
}

/**
 * 语音识别
 */
export async function speechToText(audioBlob: Blob): Promise<{ text: string }> {
  const formData = new FormData()
  formData.append('audio', audioBlob)
  return await request.post('/api/emergency/speech-to-text', formData)
}

// 获取附近医疗设备（向后兼容版本）
export async function getNearbyEquipmentLegacy(
  type: string,
  latitude: number,
  longitude: number,
): Promise<
  Array<{
    id: string
    name: string
    type: string
    location: string
    distance: number
    coordinates: [number, number]
  }>
> {
  const response = await getNearbyEquipment({ type, latitude, longitude })
  return response.data.map((item) => ({
    id: item.id,
    name: item.name,
    type: item.type,
    location: item.location.name,
    distance: item.location.distance,
    coordinates: [item.location.longitude, item.location.latitude],
  }))
}
