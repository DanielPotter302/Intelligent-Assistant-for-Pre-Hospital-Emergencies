<!-- 聊天面板组件 -->
<template>
  <section class="flex-1 flex flex-col bg-neutral overflow-hidden">
    <!-- 移动端侧边栏控制按钮 -->
    <div class="lg:hidden flex justify-between p-3 bg-light border-b border-gray-200">
      <button
        class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center ripple"
        @click="toggleLeftSidebar"
      >
        <i class="fa fa-history text-gray-600"></i>
      </button>
      <button
        class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center ripple"
        @click="toggleRightSidebar"
      >
        <i class="fa fa-book text-gray-600"></i>
      </button>
    </div>

    <!-- 聊天内容区 -->
    <div ref="chatMessagesRef" class="flex-1 p-4 overflow-y-auto scrollbar-hide">
      <!-- 系统提示 -->
      <div class="text-center mb-6">
        <span class="inline-block bg-gray-200 text-gray-500 text-xs px-3 py-1 rounded-full">
          {{ currentTime }}
        </span>
      </div>

      <!-- 空状态 - 当没有消息时显示 -->
      <div
        v-if="messages.length === 0"
        class="flex flex-col items-center justify-center h-full min-h-[400px] text-center"
      >
        <div class="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center mb-6">
          <i class="fa fa-robot text-primary text-3xl"></i>
        </div>
        <h3 class="text-xl font-semibold text-gray-700 mb-2">
          {{ mode === 'kb' ? '知识库检索' : '复杂问答' }}
        </h3>
        <p class="text-gray-500 mb-6 max-w-md">
          {{
            mode === 'kb'
              ? '我可以帮您快速检索院前急救相关知识，为您提供准确的医疗指导。'
              : '我会深入思考您的问题，为您提供详细的分析和专业建议。'
          }}
        </p>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-lg">
          <button
            v-for="example in exampleQuestions"
            :key="example"
            @click="messageInput = example"
            class="p-3 text-left bg-white border border-gray-200 rounded-lg hover:border-primary hover:bg-primary/5 transition-colors text-sm"
          >
            {{ example }}
          </button>
        </div>
      </div>

      <!-- 消息列表 -->
      <MessageTransition v-else>
        <template v-for="message in messages" :key="message.id">
          <!-- 用户消息 -->
          <div v-if="message.role === 'user'" class="flex justify-end mb-4">
            <div class="max-w-[80%] bg-primary text-white p-4 rounded-lg rounded-tr-none shadow-sm">
              <p class="text-balance">{{ message.content }}</p>
              <div class="text-xs text-white/80 text-right mt-1">
                {{ formatMessageTime(message.createdAt) }}
              </div>
            </div>
          </div>

          <!-- 助手消息 -->
          <div v-else class="flex mb-4">
            <div
              class="w-10 h-10 rounded-lg bg-secondary flex-shrink-0 flex items-center justify-center mr-3"
            >
              <i class="fa fa-robot text-white text-lg"></i>
            </div>
            <div class="flex-1 max-w-[80%]">
              <div class="bg-white p-4 rounded-lg rounded-tl-none shadow-sm">
                <MarkdownRenderer :content="message.content" />
                <div v-if="message.references?.length" class="flex flex-wrap gap-1 mt-2">
                  <span
                    v-for="(ref, index) in message.references"
                    :key="index"
                    class="text-primary text-sm cursor-pointer hover:underline"
                    @click="highlightReference(ref.id)"
                  >
                    {{ ref.citation }}
                  </span>
                </div>
                <div class="text-xs text-gray-400 mt-1">
                  {{ formatMessageTime(message.createdAt) }}
                </div>
              </div>
            </div>
          </div>
        </template>
      </MessageTransition>

      <!-- 正在输入提示 -->
      <div v-if="isTyping" class="flex mt-4">
        <div
          class="w-10 h-10 rounded-lg bg-secondary flex-shrink-0 flex items-center justify-center mr-3"
        >
          <i class="fa fa-robot text-white text-lg"></i>
        </div>
        <div class="bg-white p-3 rounded-lg rounded-tl-none shadow-sm">
          <LoadingDots />
        </div>
      </div>

      <!-- 思考过程显示 -->
      <div v-if="isShowingThinking && thinkingContent" class="flex mt-4">
        <div
          class="w-10 h-10 rounded-lg bg-yellow-500 flex-shrink-0 flex items-center justify-center mr-3"
        >
          <i class="fa fa-brain text-white text-lg"></i>
        </div>
        <div class="flex-1 max-w-[80%]">
          <div class="bg-yellow-50 border border-yellow-200 p-4 rounded-lg rounded-tl-none">
            <div class="text-xs text-yellow-600 font-medium mb-2">
              <i class="fa fa-cog fa-spin mr-1"></i>
              正在思考...
            </div>
            <div class="text-sm text-yellow-800 whitespace-pre-wrap">{{ thinkingContent }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 底部输入区 -->
    <div class="bg-light p-4 border-t border-gray-200">
      <form @submit.prevent="sendMessage" class="relative">
        <textarea
          v-model="messageInput"
          rows="2"
          placeholder="请输入您的问题..."
          class="w-full pr-20 pl-4 py-3 rounded-xl border border-gray-200 focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none resize-none transition-all"
          @focus="handleInputFocus"
          @blur="handleInputBlur"
          @input="autoResizeTextarea"
          ref="textareaRef"
        ></textarea>

        <div class="absolute right-4 bottom-4">
          <button
            v-show="!messageInput"
            type="button"
            class="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white shadow-md ripple"
            :class="{ 'bg-danger': isRecording }"
            @click="toggleVoiceRecording"
          >
            <i class="fa" :class="isRecording ? 'fa-stop' : 'fa-microphone'"></i>
            <span
              v-if="isRecording"
              class="absolute inset-0 rounded-full bg-white/30 animate-ping opacity-75"
            ></span>
          </button>

          <button
            v-show="messageInput"
            type="submit"
            class="w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white shadow-md ripple"
            :disabled="isTyping"
          >
            <i class="fa fa-paper-plane"></i>
          </button>
        </div>
      </form>
    </div>

    <!-- 错误提示 -->
    <ErrorMessage :show="!!errorMessage" :message="errorMessage" />
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue'
import { SpeechRecorder, SpeechRecognizer } from '@/utils/speech'
import * as chatApi from '@/api/chat'
import type { ChatMessage, StreamEvent } from '@/api/chat'
import MessageTransition from './MessageTransition.vue'
import LoadingDots from './LoadingDots.vue'
import ErrorMessage from './ErrorMessage.vue'
import MarkdownRenderer from './MarkdownRenderer.vue'

const emit = defineEmits<{
  (e: 'toggle-left-sidebar'): void
  (e: 'toggle-right-sidebar'): void
  (e: 'highlight-reference', refId: string): void
  (e: 'update-references', refs: Array<{ id: string; title: string; content: string }>): void
  (e: 'session-created', sessionId: string): void
  (e: 'session-updated'): void
}>()

const props = defineProps<{
  sessionId: string
  mode: 'kb' | 'graph'
}>()

// 状态
const isTyping = ref(false)
const isRecording = ref(false)
const messageInput = ref('')
const currentTime = ref(formatTime(new Date()))
// 移除硬编码的测试消息，新用户应该看到空界面
const messages = ref<ChatMessage[]>([])
const errorMessage = ref('')

// 示例问题
const exampleQuestions = ref([
  '婴儿心肺复苏的正确步骤是什么？',
  '成人气道梗阻如何处理？',
  '如何判断患者的意识状态？',
  '外伤出血的止血方法有哪些？',
])

// 流式响应状态
const currentStreamingMessage = ref<ChatMessage | null>(null)
const isShowingThinking = ref(false)
const thinkingContent = ref('')

// refs
const chatMessagesRef = ref<HTMLElement | null>(null)
const textareaRef = ref<HTMLTextAreaElement | null>(null)

// 语音识别
const speechRecorder = new SpeechRecorder()
const speechRecognizer = new SpeechRecognizer()

// 方法
function formatTime(date: Date): string {
  return new Intl.DateTimeFormat('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

function toggleLeftSidebar() {
  emit('toggle-left-sidebar')
}

function toggleRightSidebar() {
  emit('toggle-right-sidebar')
}

function highlightReference(refId: string) {
  emit('highlight-reference', refId)
}

function handleInputFocus() {
  // 输入框获得焦点时的处理
}

function handleInputBlur() {
  // 输入框失去焦点时的处理
}

function autoResizeTextarea() {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
    const newHeight = Math.min(textareaRef.value.scrollHeight, 120)
    textareaRef.value.style.height = `${newHeight}px`
  }
}

const showError = (message: string) => {
  errorMessage.value = message
  setTimeout(() => {
    errorMessage.value = ''
  }, 3000)
}

async function toggleVoiceRecording() {
  if (isRecording.value) {
    // 停止录音
    isRecording.value = false
    if (speechRecognizer.isAvailable()) {
      speechRecognizer.stop()
    } else {
      try {
        const audioBlob = await speechRecorder.stop()
        isTyping.value = true
        const { text } = await chatApi.speechToText(audioBlob)
        messageInput.value = text
        isTyping.value = false
      } catch (error) {
        console.error('Speech to text error:', error)
        showError('语音识别失败，请重试')
      }
    }
  } else {
    // 开始录音
    isRecording.value = true
    if (speechRecognizer.isAvailable()) {
      speechRecognizer.start(
        (text, isFinal) => {
          if (isFinal) {
            messageInput.value = text
            isRecording.value = false
          }
        },
        (error) => {
          console.error('Speech recognition error:', error)
          isRecording.value = false
          showError('语音识别失败，请检查麦克风权限')
        },
      )
    } else {
      try {
        await speechRecorder.start()
      } catch (error) {
        console.error('Recording error:', error)
        isRecording.value = false
        showError('无法启动录音，请检查麦克风权限')
      }
    }
  }
}

async function sendMessage() {
  const content = messageInput.value.trim()
  if (!content || isTyping.value) return

  // 添加用户消息
  const userMessage: ChatMessage = {
    id: Date.now(),
    role: 'user',
    content,
    createdAt: new Date().toISOString(),
  }
  messages.value.push(userMessage)

  // 清空输入框
  messageInput.value = ''
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto'
  }

  // 滚动到底部
  await nextTick()
  scrollToBottom()

  // 显示正在输入状态
  isTyping.value = true
  isShowingThinking.value = false
  thinkingContent.value = ''

  try {
    // 创建临时的助手消息用于流式显示
    currentStreamingMessage.value = {
      id: `temp-${Date.now()}`,
      role: 'assistant',
      content: '',
      createdAt: new Date().toISOString(),
    }

    // 选择合适的API接口
    const useAutoSession = !props.sessionId || props.sessionId === ''

    if (useAutoSession) {
      // 自动创建会话
      await chatApi.sendMessageAutoSession(
        content,
        props.mode,
        handleStreamEvent,
        handleStreamError,
        handleStreamComplete,
      )
    } else {
      // 使用现有会话
      await chatApi.sendMessageStream(
        props.sessionId,
        content,
        props.mode,
        handleStreamEvent,
        handleStreamError,
        handleStreamComplete,
      )
    }
  } catch (error) {
    console.error('Send message error:', error)
    showError('发送消息失败，请重试')
    isTyping.value = false
  }
}

// 处理流式事件
function handleStreamEvent(event: StreamEvent) {
  switch (event.type) {
    case 'session_info':
      // 处理会话信息，通知父组件更新会话列表
      if (event.data) {
        emit('session-created', event.data.id)
        emit('session-updated')
      }
      break

    case 'thinking':
      if (props.mode === 'graph') {
        isShowingThinking.value = true
        thinkingContent.value += event.content || ''
      }
      break

    case 'answer_start':
      isShowingThinking.value = false
      isTyping.value = false // 开始回复时隐藏"正在输入"指示器
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
      isShowingThinking.value = false
      thinkingContent.value = ''
      currentStreamingMessage.value = null
      nextTick(() => scrollToBottom())
      break

    case 'assistant_message':
      // 更新最终的助手消息
      if (event.data && currentStreamingMessage.value) {
        const finalMessage: ChatMessage = {
          id: event.data.id,
          role: 'assistant',
          content: event.data.content,
          createdAt: event.data.created_at || event.data.createdAt,
          references: event.data.references,
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
function handleStreamError(error: Error) {
  console.error('Stream error:', error)
  showError('连接中断，请重试')
  isTyping.value = false
  isShowingThinking.value = false
  currentStreamingMessage.value = null
}

// 处理流式完成
function handleStreamComplete() {
  isTyping.value = false
  isShowingThinking.value = false
  currentStreamingMessage.value = null
  nextTick(() => scrollToBottom())
}

// 滚动到底部的辅助方法
function scrollToBottom() {
  if (chatMessagesRef.value) {
    chatMessagesRef.value.scrollTop = chatMessagesRef.value.scrollHeight
  }
}

// 加载历史消息
async function loadMessages() {
  if (!props.sessionId) {
    console.log('没有会话ID，显示空界面')
    messages.value = []
    return
  }

  console.log('开始加载会话消息:', props.sessionId)

  try {
    const response = await chatApi.getChatMessages(props.sessionId)
    // 处理后端响应格式
    if (response.data && Array.isArray(response.data)) {
      messages.value = response.data.map((msg: any) => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
        createdAt: msg.created_at || msg.createdAt,
        references: msg.references,
      }))
      console.log('成功加载', messages.value.length, '条消息')
    } else {
      console.log('没有找到历史消息，显示空界面')
      messages.value = []
    }
    // 滚动到底部
    await nextTick()
    scrollToBottom()
  } catch (error) {
    console.error('Load messages error:', error)
    // 如果加载失败，显示空界面
    messages.value = []
  }
}

// 添加消息时间格式化函数
function formatMessageTime(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  // 1分钟内
  if (diff < 60 * 1000) {
    return '刚刚'
  }

  // 1小时内
  if (diff < 60 * 60 * 1000) {
    const minutes = Math.floor(diff / (60 * 1000))
    return `${minutes}分钟前`
  }

  // 24小时内
  if (diff < 24 * 60 * 60 * 1000) {
    const hours = Math.floor(diff / (60 * 60 * 1000))
    return `${hours}小时前`
  }

  // 7天内
  if (diff < 7 * 24 * 60 * 60 * 1000) {
    const days = Math.floor(diff / (24 * 60 * 60 * 1000))
    return `${days}天前`
  }

  // 其他显示具体日期
  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

// 监听会话ID变化
watch(
  () => props.sessionId,
  () => {
    loadMessages()
  },
)

// 生命周期钩子
onMounted(() => {
  loadMessages()
})

// 暴露方法给父组件
defineExpose({
  setInputMessage: (text: string) => {
    messageInput.value = text
    if (textareaRef.value) {
      nextTick(() => {
        textareaRef.value?.focus()
        autoResizeTextarea()
      })
    }
  },
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

.ripple {
  position: relative;
  overflow: hidden;
}
.ripple:after {
  content: '';
  display: block;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  background-image: radial-gradient(circle, #000 10%, transparent 10.01%);
  background-repeat: no-repeat;
  background-position: 50%;
  transform: scale(10, 10);
  opacity: 0;
  transition:
    transform 0.5s,
    opacity 1s;
}
.ripple:active:after {
  transform: scale(0, 0);
  opacity: 0.3;
  transition: 0s;
}
</style>
