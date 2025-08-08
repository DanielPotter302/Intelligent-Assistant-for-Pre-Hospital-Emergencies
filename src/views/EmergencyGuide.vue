<!-- 应急指导页面 -->
<template>
  <div class="flex flex-col h-screen pt-16">
    <!-- 主内容区 -->
    <main class="flex-1 flex overflow-hidden">
      <!-- 左侧场景选择栏 -->
      <div
        id="leftSidebar"
        class="w-80 bg-white border-r border-gray-200 flex flex-col overflow-hidden lg:relative"
      >
        <div class="p-4 border-b border-gray-200">
          <h2 class="text-xl font-bold text-gray-800">应急场景</h2>
          <p class="text-sm text-gray-500 mt-1">请选择您需要帮助的场景类型</p>
        </div>

        <!-- 场景类别列表 -->
        <div class="flex-1 overflow-y-auto p-4">
          <div class="space-y-4">
            <div
              v-for="scenario in Object.values(emergencyScenarios)"
              :key="scenario.id"
              class="p-4 rounded-lg border border-gray-200 hover:border-primary cursor-pointer transition-all"
              :class="{ 'border-primary bg-primary/5': selectedScenario === scenario.id }"
              @click="selectScenario(scenario.id as keyof typeof emergencyScenarios)"
            >
              <h3 class="font-semibold text-gray-800">
                <i :class="[scenario.icon, 'mr-2']"></i>
                {{ scenario.title }}
              </h3>
              <p class="text-sm text-gray-500 mt-1">{{ scenario.description }}</p>

              <!-- 聊天历史记录 -->
              <div v-if="scenarioSessions[scenario.id]?.length" class="mt-3 space-y-1" @click.stop>
                <div class="flex items-center justify-between">
                  <div class="text-xs text-gray-400 mb-1">历史记录</div>
                  <button
                    class="text-xs text-primary hover:text-primary-dark"
                    @click="createNewSession(scenario.id as keyof typeof emergencyScenarios)"
                  >
                    + 新建聊天
                  </button>
                </div>
                <div
                  v-for="session in scenarioSessions[scenario.id]"
                  :key="session.id"
                  class="text-xs p-2 bg-gray-50 rounded hover:bg-gray-100 transition-colors group"
                >
                  <div class="flex items-start justify-between">
                    <div class="flex-1 cursor-pointer" @click="loadSession(session)">
                      <div class="font-medium text-gray-700 truncate">{{ session.title }}</div>
                      <div class="text-gray-500 truncate">{{ session.lastMessage }}</div>
                      <div class="text-gray-400">{{ formatTime(session.updatedAt) }}</div>
                    </div>
                    <button
                      class="ml-2 opacity-0 group-hover:opacity-100 text-red-500 hover:text-red-700 transition-all"
                      @click="deleteSession(session.id)"
                      title="删除对话"
                    >
                      <i class="fas fa-trash text-xs"></i>
                    </button>
                  </div>
                </div>
              </div>

              <!-- 新建聊天按钮（当没有历史记录时） -->
              <div v-else-if="selectedScenario === scenario.id" class="mt-3" @click.stop>
                <button
                  class="text-xs text-primary hover:text-primary-dark"
                  @click="createNewSession(scenario.id as keyof typeof emergencyScenarios)"
                >
                  + 新建聊天
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 聊天面板 -->
      <div class="flex-1 flex flex-col bg-neutral overflow-hidden">
        <!-- 当前场景提示 -->
        <div class="bg-white border-b border-gray-200 p-4">
          <div class="flex items-center">
            <button
              class="lg:hidden w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center mr-3"
              @click="toggleLeftSidebar"
            >
              <i class="fas fa-bars text-gray-600"></i>
            </button>
            <div>
              <h2 class="text-xl font-bold text-gray-800">{{ currentScenarioTitle }}</h2>
              <p class="text-sm text-gray-500 mt-1">{{ currentScenarioDescription }}</p>
            </div>
          </div>
        </div>

        <!-- 消息列表区域 -->
        <div ref="chatMessagesRef" class="flex-1 p-4 overflow-y-auto scrollbar-hide">
          <!-- 安全提示 -->
          <SafetyTips />

          <!-- 引导提示 -->
          <div v-if="!messages.length" class="text-center py-8">
            <div
              class="w-20 h-20 mx-auto mb-4 rounded-full bg-primary/10 flex items-center justify-center"
            >
              <i class="fas fa-comment-medical text-3xl text-primary"></i>
            </div>
            <h3 class="text-lg font-semibold text-gray-800">{{ scenarioPrompt }}</h3>
            <p class="text-gray-500 mt-2 max-w-md mx-auto">{{ scenarioDescription }}</p>
          </div>

          <!-- 消息列表 -->
          <template v-else>
            <div v-for="message in messages" :key="message.id" class="mb-4">
              <!-- 用户消息 -->
              <div v-if="message.role === 'user'" class="flex justify-end">
                <div class="max-w-[80%] bg-primary text-white p-4 rounded-lg rounded-tr-none">
                  <p class="text-balance">{{ message.content }}</p>
                  <div class="text-xs text-white/80 text-right mt-1">
                    {{ formatMessageTime(message.createdAt) }}
                  </div>
                </div>
              </div>

              <!-- 助手消息 -->
              <div v-else class="flex">
                <div
                  class="w-10 h-10 rounded-lg bg-secondary flex-shrink-0 flex items-center justify-center mr-3"
                >
                  <i class="fas fa-robot text-white"></i>
                </div>
                <div class="flex-1 max-w-[80%]">
                  <div class="bg-white p-4 rounded-lg rounded-tl-none">
                    <MarkdownRenderer :content="message.content" />
                    <!-- 如果有操作步骤，显示为列表 -->
                    <div v-if="message.steps?.length" class="mt-3 space-y-2">
                      <div
                        v-for="(step, index) in message.steps"
                        :key="index"
                        class="flex items-start space-x-2 p-2 rounded bg-gray-50"
                      >
                        <div
                          class="w-6 h-6 rounded-full bg-primary/10 flex-shrink-0 flex items-center justify-center text-primary text-sm"
                        >
                          {{ index + 1 }}
                        </div>
                        <p class="text-sm text-gray-700">{{ step }}</p>
                      </div>
                    </div>
                    <div class="text-xs text-gray-400 mt-1">
                      {{ formatMessageTime(message.createdAt) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </template>

          <!-- 正在输入提示 -->
          <div v-if="isTyping" class="flex mt-4">
            <div
              class="w-10 h-10 rounded-lg bg-secondary flex-shrink-0 flex items-center justify-center mr-3"
            >
              <i class="fas fa-robot text-white"></i>
            </div>
            <div class="bg-white p-3 rounded-lg rounded-tl-none">
              <LoadingDots />
            </div>
          </div>
        </div>

        <!-- 输入区域 -->
        <div class="bg-white border-t border-gray-200 p-4">
          <form @submit.prevent="sendMessage" class="relative">
            <textarea
              v-model="messageInput"
              rows="2"
              :placeholder="inputPlaceholder"
              class="w-full pr-20 pl-4 py-3 rounded-xl border border-gray-200 focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none resize-none transition-all"
              @keydown.enter.prevent="handleEnterPress"
              ref="textareaRef"
            ></textarea>

            <div class="absolute right-4 bottom-4">
              <!-- 语音输入按钮 -->
              <button
                v-show="!messageInput"
                type="button"
                class="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white shadow-md hover:bg-primary-dark transition-colors"
                :class="{ 'bg-red-500': isRecording }"
                @click="toggleVoiceRecording"
              >
                <i class="fas" :class="isRecording ? 'fa-stop' : 'fa-microphone'"></i>
                <span
                  v-if="isRecording"
                  class="absolute inset-0 rounded-full bg-white/30 animate-ping"
                ></span>
              </button>

              <!-- 发送按钮 -->
              <button
                v-show="messageInput"
                type="submit"
                :disabled="isTyping"
                class="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white shadow-md hover:bg-primary-dark transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                <i class="fas fa-paper-plane"></i>
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>

    <!-- 错误提示 -->
    <ErrorMessage :show="!!errorMessage" :message="errorMessage" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { SpeechRecorder, SpeechRecognizer } from '@/utils/speech'
import * as emergencyApi from '@/api/emergency'
import type { EmergencyMessage, EmergencySession, EmergencyStreamEvent } from '@/api/emergency'
import { emergencyScenarios, type EmergencyScenario } from '@/config/emergency'
import ErrorMessage from '@/components/chat/ErrorMessage.vue'
import LoadingDots from '@/components/chat/LoadingDots.vue'
import MarkdownRenderer from '@/components/chat/MarkdownRenderer.vue'
import SafetyTips from '@/components/emergency/SafetyTips.vue'

// 状态
const selectedScenario = ref<keyof typeof emergencyScenarios | null>(null)
const currentSession = ref<EmergencySession | null>(null)
const messageInput = ref('')
const isTyping = ref(false)
const isRecording = ref(false)
const messages = ref<EmergencyMessage[]>([])
const errorMessage = ref('')
const scenarioSessions = ref<Record<string, EmergencySession[]>>({})
const currentStreamingMessage = ref<EmergencyMessage | null>(null)
const chatMessagesRef = ref<HTMLElement | null>(null)
const textareaRef = ref<HTMLTextAreaElement | null>(null)

// 语音识别相关
const speechRecorder = new SpeechRecorder()
const speechRecognizer = new SpeechRecognizer()

// 场景相关的计算属性
const currentScenarioConfig = computed<EmergencyScenario | null>(() => {
  if (!selectedScenario.value) return null
  return emergencyScenarios[selectedScenario.value]
})

const currentScenarioTitle = computed(() => {
  return currentScenarioConfig.value?.title || '请选择应急场景'
})

const currentScenarioDescription = computed(() => {
  return currentScenarioConfig.value?.description || '选择一个场景开始对话'
})

const scenarioPrompt = computed(() => {
  return currentScenarioConfig.value?.prompts[0] || '请先选择左侧的应急场景'
})

const scenarioDescription = computed(() => {
  return currentScenarioConfig.value?.prompts[1] || '选择左侧的应急场景类型，开始获取专业指导'
})

const inputPlaceholder = computed(() => {
  if (!selectedScenario.value) return '请先选择左侧的应急场景...'

  switch (selectedScenario.value) {
    case 'equipment':
      return '请输入您想了解的医疗设备名称...'
    case 'firstAid':
      return '请输入您需要的急救操作步骤...'
    case 'location':
      return '请输入您要查找的医疗设备...'
    case 'emergency':
      return '请描述现场情况，包括伤者状况、环境等信息...'
    default:
      return '请输入您的问题...'
  }
})

// 显示错误信息
const showError = (message: string) => {
  errorMessage.value = message
  setTimeout(() => {
    errorMessage.value = ''
  }, 3000)
}

// 滚动到底部
const scrollToBottom = () => {
  if (chatMessagesRef.value) {
    chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
  }
}

// 加载所有场景的会话历史
const loadAllSessions = async () => {
  try {
    const sessions = await emergencyApi.getSessions()
    const groupedSessions: Record<string, EmergencySession[]> = {}

    sessions.forEach((session) => {
      if (!groupedSessions[session.scenario]) {
        groupedSessions[session.scenario] = []
      }
      groupedSessions[session.scenario].push(session)
    })

    // 按更新时间排序
    Object.keys(groupedSessions).forEach((scenario) => {
      groupedSessions[scenario].sort(
        (a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime(),
      )
    })

    scenarioSessions.value = groupedSessions
  } catch (error) {
    console.error('加载会话历史失败:', error)
  }
}

// 加载指定会话
const loadSession = async (session: EmergencySession) => {
  try {
    currentSession.value = session
    selectedScenario.value = session.scenario as keyof typeof emergencyScenarios

    // 加载会话消息
    const sessionMessages = await emergencyApi.getMessages(session.id)
    messages.value = sessionMessages

    // 滚动到底部
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('加载会话失败:', error)
    showError('加载会话失败')
  }
}

// 删除会话
const deleteSession = async (sessionId: string) => {
  if (!confirm('确定要删除此对话吗？')) {
    return
  }
  try {
    await emergencyApi.deleteSession(sessionId)

    // 如果删除的是当前会话，清空消息和当前会话
    if (currentSession.value?.id === sessionId) {
      currentSession.value = null
      messages.value = []
    }

    // 重新加载会话历史
    await loadAllSessions()

    showError('对话已删除')
  } catch (error) {
    console.error('删除会话失败:', error)
    showError('删除会话失败，请重试')
  }
}

// 格式化时间
const formatTime = (dateString: string): string => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  if (diff < 60 * 1000) return '刚刚'
  if (diff < 60 * 60 * 1000) return `${Math.floor(diff / (60 * 1000))}分钟前`
  if (diff < 24 * 60 * 60 * 1000) return `${Math.floor(diff / (60 * 60 * 1000))}小时前`
  if (diff < 7 * 24 * 60 * 60 * 1000) return `${Math.floor(diff / (24 * 60 * 60 * 1000))}天前`

  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

// 格式化消息时间
const formatMessageTime = (dateString: string): string => {
  return formatTime(dateString)
}

// 方法
const selectScenario = async (scenario: keyof typeof emergencyScenarios) => {
  selectedScenario.value = scenario
  messages.value = [] // 清空消息历史
  currentSession.value = null

  // 不自动创建会话，让用户手动点击"新建聊天"或选择历史记录
}

const createNewSession = async (scenario: keyof typeof emergencyScenarios) => {
  try {
    selectedScenario.value = scenario
    messages.value = [] // 清空消息历史
    currentSession.value = null

    // 创建新会话
    const session = await emergencyApi.createSession(scenario)
    currentSession.value = session

    // 重新加载会话历史
    await loadAllSessions()
  } catch (error) {
    console.error('创建新会话失败:', error)
    showError('创建新会话失败，请重试')
  }
}

const toggleLeftSidebar = () => {
  const leftSidebar = document.querySelector('#leftSidebar') as HTMLElement
  if (leftSidebar) {
    leftSidebar.classList.toggle('fixed')
    leftSidebar.classList.toggle('inset-0')
    leftSidebar.classList.toggle('z-50')
  }
}

const handleEnterPress = (e: KeyboardEvent) => {
  if (e.shiftKey) return // 允许换行
  sendMessage()
}

const toggleVoiceRecording = async () => {
  if (isRecording.value) {
    isRecording.value = false
    try {
      const audioBlob = await speechRecorder.stop()
      isTyping.value = true
      const { text } = await emergencyApi.speechToText(audioBlob)
      messageInput.value = text
      isTyping.value = false
    } catch (error) {
      console.error('语音识别错误:', error)
      showError('语音识别失败，请重试')
    }
  } else {
    isRecording.value = true
    try {
      await speechRecorder.start()
    } catch (error) {
      console.error('录音错误:', error)
      isRecording.value = false
      showError('无法启动录音，请检查麦克风权限')
    }
  }
}

// 处理流式事件
const handleStreamEvent = (event: EmergencyStreamEvent) => {
  switch (event.type) {
    case 'answer_start':
      isTyping.value = false
      if (currentStreamingMessage.value) {
        currentStreamingMessage.value.id = event.message_id || currentStreamingMessage.value.id
        currentStreamingMessage.value.content = ''
        // 添加到消息列表中开始显示
        if (!messages.value.find((m) => m.id === currentStreamingMessage.value?.id)) {
          messages.value.push(currentStreamingMessage.value)
        }
      }
      break

    case 'answer':
      if (currentStreamingMessage.value) {
        currentStreamingMessage.value.content += event.content || ''
        // 滚动到底部
        nextTick(() => scrollToBottom())
      }
      break

    case 'done':
      // 流式响应完成，确保消息已保存
      if (currentStreamingMessage.value) {
        // 确保消息在列表中
        const existingIndex = messages.value.findIndex(
          (m) => m.id === currentStreamingMessage.value?.id,
        )
        if (existingIndex === -1) {
          // 如果消息不在列表中，添加它
          messages.value.push(currentStreamingMessage.value)
        } else {
          // 更新现有消息的内容
          messages.value[existingIndex] = { ...currentStreamingMessage.value }
        }
      }
      // 完成后清理状态
      isTyping.value = false
      currentStreamingMessage.value = null
      nextTick(() => scrollToBottom())
      // 重新加载会话历史
      loadAllSessions()
      break

    case 'assistant_message':
      // 更新最终的助手消息
      if (event.data && currentStreamingMessage.value) {
        const finalMessage: EmergencyMessage = {
          id: event.data.id,
          role: 'assistant',
          content: event.data.content,
          steps: event.data.steps,
          createdAt: event.data.created_at || event.data.createdAt,
        }

        // 替换临时消息
        const index = messages.value.findIndex((m) => m.id === currentStreamingMessage.value?.id)
        if (index !== -1) {
          messages.value[index] = finalMessage
        } else {
          // 如果找不到临时消息，直接添加
          messages.value.push(finalMessage)
        }
      }
      break

    case 'user_message':
      // 更新用户消息ID（如果需要）
      if (event.data) {
        const lastUserMessage = messages.value[messages.value.length - 1]
        if (lastUserMessage && lastUserMessage.role === 'user') {
          lastUserMessage.id = event.data.id
        }
      }
      break

    case 'error':
      showError(event.message || '发送消息失败')
      break
  }
}

// 处理流式错误
const handleStreamError = (error: Error) => {
  console.error('Stream error:', error)
  showError('连接中断，请重试')
  isTyping.value = false
  currentStreamingMessage.value = null
}

// 处理流式完成
const handleStreamComplete = () => {
  // done事件已经处理了大部分逻辑，这里只做最后的清理
  isTyping.value = false
  if (currentStreamingMessage.value) {
    currentStreamingMessage.value = null
  }
  nextTick(() => scrollToBottom())
}

const sendMessage = async () => {
  const content = messageInput.value.trim()
  if (!content || isTyping.value || !selectedScenario.value) return

  // 如果没有当前会话，先创建一个新会话
  if (!currentSession.value) {
    try {
      const session = await emergencyApi.createSession(selectedScenario.value)
      currentSession.value = session
      // 重新加载会话历史
      await loadAllSessions()
    } catch (error) {
      console.error('创建会话失败:', error)
      showError('创建会话失败，请重试')
      return
    }
  }

  // 添加用户消息
  const userMessage: EmergencyMessage = {
    id: Date.now(),
    role: 'user',
    content,
    createdAt: new Date().toISOString(),
  }
  messages.value.push(userMessage)

  // 清空输入
  messageInput.value = ''

  // 滚动到底部
  await nextTick()
  scrollToBottom()

  // 显示正在输入状态
  isTyping.value = true

  try {
    // 创建临时的助手消息用于流式显示
    currentStreamingMessage.value = {
      id: `temp-${Date.now()}`,
      role: 'assistant',
      content: '',
      createdAt: new Date().toISOString(),
    }

    // 发送流式消息
    await emergencyApi.sendMessageStream(
      currentSession.value.id,
      content,
      selectedScenario.value,
      handleStreamEvent,
      handleStreamError,
      handleStreamComplete,
    )
  } catch (error) {
    console.error('发送消息失败:', error)
    showError('发送消息失败，请重试')
    isTyping.value = false
  }
}

// 如果是位置相关的场景，获取用户位置
const getLocation = () => {
  if (selectedScenario.value === 'location' && 'geolocation' in navigator) {
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        try {
          const equipment = await emergencyApi.getNearbyEquipment({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            type: 'aed',
          })
          // TODO: 在地图上显示设备位置
          console.log('附近的设备:', equipment)
        } catch (error) {
          console.error('获取设备位置失败:', error)
          showError('获取设备位置失败')
        }
      },
      (error) => {
        console.error('获取位置失败:', error)
        showError('无法获取您的位置，请检查位置权限')
      },
    )
  }
}

// 监听场景变化
watch(
  () => selectedScenario.value,
  () => {
    if (selectedScenario.value === 'location') {
      getLocation()
    }
  },
)

// 页面挂载时加载会话历史
onMounted(() => {
  loadAllSessions()
})
</script>

<style scoped>
.scrollbar-hide {
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>
