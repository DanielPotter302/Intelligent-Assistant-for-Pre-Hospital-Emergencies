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

            <!-- 快速操作面板 -->
            <div class="mt-8 max-w-md mx-auto">
              <QuickActions
                :scenario="selectedScenario || undefined"
                @send-message="handleQuickAction"
              />
            </div>
          </div>

          <!-- 消息列表 -->
          <template v-else>
            <div v-for="message in messages" :key="message.id" class="mb-4">
              <!-- 用户消息 -->
              <div v-if="message.role === 'user'" class="flex justify-end">
                <div class="max-w-[80%] bg-primary text-white p-4 rounded-lg rounded-tr-none">
                  <p class="text-balance">{{ message.content }}</p>
                </div>
              </div>

              <!-- 助手消息 -->
              <div v-else class="flex">
                <div
                  class="w-10 h-10 rounded-lg bg-secondary flex-shrink-0 flex items-center justify-center mr-3"
                >
                  <i class="fas fa-robot text-white"></i>
                </div>
                <div class="max-w-[80%] bg-white p-4 rounded-lg rounded-tl-none">
                  <p class="text-balance text-gray-700 whitespace-pre-line">
                    {{ message.content }}
                  </p>
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
                class="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white shadow-md hover:bg-primary-dark transition-colors"
                :disabled="isTyping"
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
import { ref, computed, watch } from 'vue'
import { SpeechRecorder, SpeechRecognizer } from '@/utils/speech'
import * as emergencyApi from '@/api/emergency'
import type { EmergencyMessage, EmergencySession } from '@/api/emergency'
import { emergencyScenarios, type EmergencyScenario } from '@/config/emergency'
import ErrorMessage from '@/components/chat/ErrorMessage.vue'
import LoadingDots from '@/components/chat/LoadingDots.vue'
import QuickActions from '@/components/emergency/QuickActions.vue'
import SafetyTips from '@/components/emergency/SafetyTips.vue'
import SessionManager from '@/components/emergency/SessionManager.vue'

// 状态
const selectedScenario = ref<keyof typeof emergencyScenarios | null>(null)
const currentSession = ref<EmergencySession | null>(null)
const messageInput = ref('')
const isTyping = ref(false)
const isRecording = ref(false)
const messages = ref<EmergencyMessage[]>([])
const errorMessage = ref('')

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

// 方法
const selectScenario = async (scenario: keyof typeof emergencyScenarios) => {
  try {
    selectedScenario.value = scenario
    messages.value = [] // 清空消息历史

    // 创建新会话
    const session = await emergencyApi.createSession(scenario)
    currentSession.value = session
  } catch (error) {
    console.error('创建会话失败:', error)
    showError('创建会话失败，请重试')
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

const sendMessage = async () => {
  const content = messageInput.value.trim()
  if (!content || isTyping.value || !selectedScenario.value || !currentSession.value) return

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

  // 发送消息到后端
  isTyping.value = true
  try {
    const response = await emergencyApi.sendMessage(
      currentSession.value.id,
      content,
      selectedScenario.value,
    )

    // 添加助手回复
    messages.value.push(response.message)
  } catch (error) {
    console.error('发送消息失败:', error)
    showError('发送消息失败，请重试')
  } finally {
    isTyping.value = false
  }
}

// 加载历史消息
const loadMessages = async () => {
  if (!currentSession.value) return

  try {
    const historyMessages = await emergencyApi.getMessages(currentSession.value.id)
    messages.value = historyMessages
  } catch (error) {
    console.error('加载历史消息失败:', error)
    showError('加载历史消息失败')
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

// 处理快速操作消息
const handleQuickAction = async (action: string) => {
  if (!selectedScenario.value || !currentSession.value) return

  const userMessage: EmergencyMessage = {
    id: Date.now(),
    role: 'user',
    content: action,
    createdAt: new Date().toISOString(),
  }
  messages.value.push(userMessage)

  isTyping.value = true
  try {
    const response = await emergencyApi.sendMessage(
      currentSession.value.id,
      action,
      selectedScenario.value,
    )
    messages.value.push(response.message)
  } catch (error) {
    console.error('发送快速操作消息失败:', error)
    showError('发送快速操作消息失败，请重试')
  } finally {
    isTyping.value = false
  }
}

// 处理会话选择
const handleSessionSelect = async (session: EmergencySession) => {
  currentSession.value = session
  selectedScenario.value = session.scenario
  await loadMessages()
}

// 处理创建新会话
const handleCreateSession = () => {
  // 重置状态，让用户重新选择场景
  selectedScenario.value = null
  currentSession.value = null
  messages.value = []
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
