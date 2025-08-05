<!-- 智能问答页面 -->
<template>
  <div class="flex flex-col h-screen pt-16">
    <!-- 主内容区 -->
    <main class="flex-1 flex overflow-hidden">
      <!-- 左侧功能栏 -->
      <LeftSidebar
        ref="leftSidebarRef"
        v-model="chatMode"
        @select-chat="handleChatSelect"
        @new-chat="handleNewChat"
      />

      <!-- 聊天面板 -->
      <ChatPanel
        ref="chatPanelRef"
        :session-id="currentSessionId"
        :mode="chatMode"
        @toggle-left-sidebar="toggleLeftSidebar"
        @toggle-right-sidebar="toggleRightSidebar"
        @highlight-reference="handleHighlightReference"
        @update-references="handleUpdateReferences"
      />

      <!-- 右侧参考栏 -->
      <RightSidebar ref="rightSidebarRef" @select-question="handleQuickQuestion" />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import LeftSidebar from '@/components/chat/LeftSidebar.vue'
import ChatPanel from '@/components/chat/ChatPanel.vue'
import RightSidebar from '@/components/chat/RightSidebar.vue'
import * as chatApi from '@/api/chat'

// 状态
const chatMode = ref<'kb' | 'graph'>('kb')
const currentSessionId = ref<string>('')
const chatPanelRef = ref<InstanceType<typeof ChatPanel> | null>(null)
const rightSidebarRef = ref<InstanceType<typeof RightSidebar> | null>(null)
const leftSidebarRef = ref<InstanceType<typeof LeftSidebar> | null>(null)

// 方法
const handleChatSelect = (chatId: string) => {
  currentSessionId.value = chatId
}

const handleNewChat = () => {
  // 新建会话时可以做一些额外的处理
  console.log('New chat created')
}

const handleQuickQuestion = (question: string) => {
  // 将问题发送到聊天面板
  chatPanelRef.value?.setInputMessage(question)
}

const handleHighlightReference = (refId: string) => {
  rightSidebarRef.value?.setActiveReference(refId)
}

const handleUpdateReferences = (refs: Array<{ id: string; title: string; content: string }>) => {
  // 更新右侧栏的参考资料
  rightSidebarRef.value?.updateReferences(refs)
}

// 初始化页面时自动创建会话
const initializeChat = async () => {
  try {
    // 首先尝试获取现有会话列表
    const historyResponse = await chatApi.getChatHistory()
    if (historyResponse.data && historyResponse.data.length > 0) {
      // 如果有现有会话，选择最新的一个
      const latestSession = historyResponse.data[0]
      currentSessionId.value = latestSession.id
      console.log('使用现有会话:', latestSession.id)
    } else {
      // 如果没有现有会话，创建一个新的
      const response = await chatApi.createChatSession('新对话', chatMode.value)
      if (response.data) {
        currentSessionId.value = response.data.id
        console.log('创建新会话:', response.data.id)
      }
    }
  } catch (error) {
    console.error('Failed to initialize chat session:', error)
    // 如果所有API调用都失败，使用临时ID
    currentSessionId.value = Date.now().toString()
  }
}

// 页面挂载时初始化
onMounted(async () => {
  console.log('AIChat页面挂载，开始初始化...')
  await initializeChat()
  console.log('初始化完成，当前会话ID:', currentSessionId.value)
})

const toggleLeftSidebar = () => {
  const leftSidebar = document.querySelector('#leftSidebar') as HTMLElement
  if (leftSidebar) {
    leftSidebar.classList.toggle('hidden')
    leftSidebar.classList.toggle('fixed')
    leftSidebar.classList.toggle('top-[60px]')
    leftSidebar.classList.toggle('left-0')
    leftSidebar.classList.toggle('bottom-0')
    leftSidebar.classList.toggle('z-40')
    leftSidebar.classList.toggle('w-[80%]')
    leftSidebar.classList.toggle('max-w-sm')
  }
}

const toggleRightSidebar = () => {
  const rightSidebar = document.querySelector('#rightSidebar') as HTMLElement
  if (rightSidebar) {
    rightSidebar.classList.toggle('hidden')
    rightSidebar.classList.toggle('fixed')
    rightSidebar.classList.toggle('top-[60px]')
    rightSidebar.classList.toggle('right-0')
    rightSidebar.classList.toggle('bottom-0')
    rightSidebar.classList.toggle('z-40')
    rightSidebar.classList.toggle('w-[80%]')
    rightSidebar.classList.toggle('max-w-sm')
  }
}
</script>

<style scoped>
.container {
  max-width: 1280px;
}
</style>
