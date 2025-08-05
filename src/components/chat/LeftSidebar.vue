<!-- 左侧功能栏组件 -->
<template>
  <aside
    id="leftSidebar"
    class="w-64 bg-light border-r border-gray-200 flex-shrink-0 hidden lg:block overflow-y-auto transition-all duration-300 ease-in-out"
  >
    <!-- 模式切换 -->
    <div class="p-4 border-b border-gray-200">
      <h2 class="text-sm font-medium text-gray-500 mb-3">问答模式</h2>
      <div class="flex rounded-lg overflow-hidden border border-gray-200">
        <button
          :class="[
            'flex-1 py-2 px-3 text-sm font-medium transition-colors',
            modelValue === 'kb'
              ? 'bg-primary text-white'
              : 'bg-light text-gray-600 hover:bg-gray-100',
          ]"
          @click="updateMode('kb')"
        >
          知识库检索
        </button>
        <button
          :class="[
            'flex-1 py-2 px-3 text-sm font-medium transition-colors',
            modelValue === 'graph'
              ? 'bg-primary text-white'
              : 'bg-light text-gray-600 hover:bg-gray-100',
          ]"
          @click="updateMode('graph')"
        >
          复杂问答
        </button>
      </div>
    </div>

    <!-- 会话历史 -->
    <div class="p-4">
      <div class="flex justify-between items-center mb-3">
        <h2 class="text-sm font-medium text-gray-500">会话历史</h2>
        <!-- 更多菜单按钮 -->
        <div class="relative">
          <button
            class="p-2 text-gray-400 hover:text-primary transition-colors"
            @click.stop="toggleHistoryMenu"
          >
            <i class="fa fa-ellipsis-v"></i>
          </button>

          <!-- 历史记录菜单 -->
          <div
            v-if="showHistoryMenu"
            class="absolute right-0 top-full mt-1 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-50"
            @click.stop
          >
            <button
              class="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 transition-colors flex items-center space-x-2"
              @click="startSelectMode"
            >
              <i class="fa fa-check-square-o text-gray-400"></i>
              <span>选择删除</span>
            </button>
            <button
              class="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 transition-colors flex items-center space-x-2"
              @click="clearHistory"
            >
              <i class="fa fa-trash-o text-gray-400"></i>
              <span>清空全部记录</span>
            </button>
            <button
              class="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 transition-colors flex items-center space-x-2"
              @click="exportHistory"
            >
              <i class="fa fa-download text-gray-400"></i>
              <span>导出聊天记录</span>
            </button>
          </div>
        </div>
      </div>

      <!-- 批量操作栏 -->
      <div
        v-if="isEditMode"
        class="flex justify-between items-center px-3 py-2 bg-primary/5 rounded-lg mb-3"
      >
        <div class="flex items-center space-x-2">
          <span class="text-sm text-gray-600">
            {{ selectedChats.length ? `已选择 ${selectedChats.length} 项` : '请选择要删除的会话' }}
          </span>
        </div>
        <div class="flex items-center space-x-2">
          <button
            v-if="selectedChats.length > 0"
            class="px-3 py-1 text-sm text-danger hover:text-danger/80 transition-colors"
            @click="deleteSelectedChats"
          >
            删除
          </button>
          <button
            class="px-3 py-1 text-sm text-gray-600 hover:text-gray-900 transition-colors"
            @click="cancelSelectMode"
          >
            取消
          </button>
        </div>
      </div>

      <!-- 会话列表 -->
      <div class="space-y-1">
        <!-- 加载状态 -->
        <div v-if="isLoading" class="text-center py-4">
          <div
            class="inline-block animate-spin rounded-full h-6 w-6 border-b-2 border-primary"
          ></div>
          <p class="text-sm text-gray-500 mt-2">加载中...</p>
        </div>

        <!-- 空状态 -->
        <div v-else-if="chatHistory.length === 0" class="text-center py-8">
          <i class="fa fa-comments text-gray-300 text-3xl mb-3"></i>
          <p class="text-sm text-gray-500">暂无会话历史</p>
          <p class="text-xs text-gray-400 mt-1">点击下方按钮开始新对话</p>
        </div>

        <!-- 会话列表 -->
        <div
          v-else
          v-for="chat in chatHistory"
          :key="chat.id"
          :class="[
            'group relative rounded-lg transition-colors',
            currentChatId === chat.id ? 'bg-primary/10' : 'hover:bg-gray-50',
            isEditMode ? 'pl-10' : '',
          ]"
        >
          <!-- 选择框 -->
          <div v-if="isEditMode" class="absolute left-3 top-1/2 -translate-y-1/2">
            <input
              type="checkbox"
              :checked="selectedChats.includes(chat.id)"
              @change="toggleChatSelection(chat.id)"
              class="w-4 h-4 rounded border-gray-300 text-primary focus:ring-primary"
            />
          </div>

          <!-- 会话内容 -->
          <div
            class="p-3 cursor-pointer"
            :class="{ 'border-l-4 border-primary': currentChatId === chat.id && !isEditMode }"
            @click="isEditMode ? toggleChatSelection(chat.id) : selectChat(chat.id)"
          >
            <div class="flex-1 min-w-0">
              <p
                class="text-sm font-medium truncate"
                :class="currentChatId === chat.id ? 'text-primary' : 'text-gray-700'"
              >
                {{ chat.title }}
              </p>
              <p class="text-xs text-gray-500 mt-1">{{ formatTime(chat.updatedAt) }}</p>
              <p v-if="chat.lastMessage" class="text-xs text-gray-500 mt-1 truncate">
                {{ chat.lastMessage }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- 新建会话按钮 -->
      <button
        class="w-full mt-4 py-2 border border-dashed border-gray-300 rounded-lg text-sm text-gray-500 hover:bg-gray-50 transition-colors"
        @click="createNewChat"
      >
        <i class="fa fa-plus mr-1"></i> 新建会话
      </button>
    </div>

    <!-- 确认对话框 -->
    <div
      v-if="showConfirmDialog"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      @click="showConfirmDialog = false"
    >
      <div class="bg-white rounded-lg shadow-xl max-w-sm mx-4 w-full" @click.stop>
        <div class="p-6">
          <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ confirmDialogTitle }}</h3>
          <p class="text-gray-600">{{ confirmDialogMessage }}</p>
        </div>
        <div class="px-6 py-4 bg-gray-50 rounded-b-lg flex justify-end space-x-3">
          <button
            class="px-4 py-2 text-sm text-gray-600 hover:text-gray-900 transition-colors"
            @click="showConfirmDialog = false"
          >
            取消
          </button>
          <button
            class="px-4 py-2 text-sm bg-danger text-white rounded-lg hover:bg-danger/90 transition-colors"
            @click="handleConfirmAction"
          >
            确认
          </button>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as chatApi from '@/api/chat'
import type { ChatSession } from '@/api/chat'

const props = defineProps<{
  modelValue: 'kb' | 'graph'
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: 'kb' | 'graph'): void
  (e: 'select-chat', chatId: string): void
  (e: 'new-chat'): void
}>()

// 状态
const currentChatId = ref<string>('')
const showHistoryMenu = ref(false)

// 添加新的状态
const isEditMode = ref(false)
const selectedChats = ref<string[]>([])

// 示例聊天历史数据
const chatHistory = ref<ChatSession[]>([])

// 对话框状态
const showConfirmDialog = ref(false)
const confirmDialogTitle = ref('')
const confirmDialogMessage = ref('')
let confirmCallback: (() => void) | null = null

// 加载状态
const isLoading = ref(false)

// 方法
function formatTime(dateString: string): string {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  // 24小时内显示具体时间
  if (diff < 24 * 60 * 60 * 1000) {
    return new Intl.DateTimeFormat('zh-CN', {
      hour: '2-digit',
      minute: '2-digit',
    }).format(date)
  }

  // 7天内显示"x天前"
  if (diff < 7 * 24 * 60 * 60 * 1000) {
    const days = Math.floor(diff / (24 * 60 * 60 * 1000))
    return `${days}天前`
  }

  // 其他显示具体日期
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(date)
}

function updateMode(mode: 'kb' | 'graph') {
  emit('update:modelValue', mode)
}

async function selectChat(chatId: string) {
  currentChatId.value = chatId
  emit('select-chat', chatId)
}

async function createNewChat() {
  try {
    // 调用后端API创建新会话
    const response = await chatApi.createChatSession('新会话', props.modelValue)
    if (response.data) {
      const newChat: ChatSession = {
        id: response.data.id,
        title: response.data.title,
        createdAt: response.data.created_at || response.data.createdAt,
        updatedAt: response.data.updated_at || response.data.updatedAt,
      }
      chatHistory.value.unshift(newChat)
      currentChatId.value = newChat.id
      emit('select-chat', newChat.id)
      emit('new-chat')
    }
  } catch (error) {
    console.error('Create new chat error:', error)
    // 如果API调用失败，创建临时会话
    const newChat: ChatSession = {
      id: Date.now().toString(),
      title: '新会话',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }
    chatHistory.value.unshift(newChat)
    currentChatId.value = newChat.id
    emit('select-chat', newChat.id)
    emit('new-chat')
  }
}

function toggleHistoryMenu(event: Event) {
  event.stopPropagation()
  showHistoryMenu.value = !showHistoryMenu.value
}

function showConfirm(title: string, message: string, callback: () => void) {
  confirmDialogTitle.value = title
  confirmDialogMessage.value = message
  confirmCallback = callback
  showConfirmDialog.value = true
}

function handleConfirmAction() {
  if (confirmCallback) {
    confirmCallback()
  }
  showConfirmDialog.value = false
  confirmCallback = null
}

async function deleteChat(chatId: string) {
  showConfirm('删除会话', '确定要删除这个会话吗？此操作无法撤销。', () => {
    chatHistory.value = chatHistory.value.filter((chat) => chat.id !== chatId)
    if (currentChatId.value === chatId) {
      const nextChat = chatHistory.value[0]
      if (nextChat) {
        currentChatId.value = nextChat.id
        emit('select-chat', nextChat.id)
      } else {
        currentChatId.value = ''
        emit('select-chat', '')
      }
    }
  })
}

function clearHistory() {
  showConfirm('清空历史记录', '确定要清空所有会话记录吗？此操作无法撤销。', () => {
    chatHistory.value = []
    currentChatId.value = ''
    showHistoryMenu.value = false
  })
}

function exportHistory() {
  const data = JSON.stringify(chatHistory.value, null, 2)
  const blob = new Blob([data], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `chat-history-${new Date().toISOString()}.json`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  showHistoryMenu.value = false
}

// 添加新的方法
function toggleChatSelection(chatId: string) {
  const index = selectedChats.value.indexOf(chatId)
  if (index === -1) {
    selectedChats.value.push(chatId)
  } else {
    selectedChats.value.splice(index, 1)
  }
}

function deleteSelectedChats() {
  showConfirm(
    '删除选中会话',
    `确定要删除选中的 ${selectedChats.value.length} 个会话吗？此操作无法撤销。`,
    () => {
      chatHistory.value = chatHistory.value.filter((chat) => !selectedChats.value.includes(chat.id))
      if (selectedChats.value.includes(currentChatId.value)) {
        const nextChat = chatHistory.value[0]
        if (nextChat) {
          currentChatId.value = nextChat.id
          emit('select-chat', nextChat.id)
        } else {
          currentChatId.value = ''
          emit('select-chat', '')
        }
      }
      selectedChats.value = []
      isEditMode.value = false
    },
  )
}

function startSelectMode() {
  isEditMode.value = true
  selectedChats.value = []
  showHistoryMenu.value = false
}

function cancelSelectMode() {
  isEditMode.value = false
  selectedChats.value = []
}

// 加载会话历史
async function loadChatHistory() {
  try {
    isLoading.value = true
    const response = await chatApi.getChatHistory(props.modelValue)
    if (response.data && Array.isArray(response.data)) {
      chatHistory.value = response.data.map((session: any) => ({
        id: session.id,
        title: session.title,
        lastMessage: session.last_message || session.lastMessage || '',
        createdAt: session.created_at || session.createdAt,
        updatedAt: session.updated_at || session.updatedAt,
      }))

      // 如果有会话历史，选择第一个
      if (chatHistory.value.length > 0) {
        currentChatId.value = chatHistory.value[0].id
        emit('select-chat', currentChatId.value)
      } else {
        // 没有会话历史时，清空当前选择
        currentChatId.value = ''
        emit('select-chat', '')
      }
    }
  } catch (error) {
    console.error('Failed to load chat history:', error)
    // 如果加载失败，保持空数组
    chatHistory.value = []
    currentChatId.value = ''
    emit('select-chat', '')
  } finally {
    isLoading.value = false
  }
}

// 生命周期钩子
onMounted(async () => {
  await loadChatHistory()

  // 点击其他地方关闭菜单
  document.addEventListener('click', () => {
    showHistoryMenu.value = false
  })
})

// 监听模式变化，重新加载会话历史
watch(
  () => props.modelValue,
  async () => {
    await loadChatHistory()
  },
)
</script>

<style scoped>
/* 修复 @apply 错误 */
.group:hover .text-gray-300 {
  color: rgb(156 163 175);
}

@media (max-width: 1024px) {
  #leftSidebar.fixed {
    top: 4rem !important;
  }
}
</style>
