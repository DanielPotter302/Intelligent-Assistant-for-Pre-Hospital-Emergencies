<template>
  <div class="bg-white border-r border-gray-200 w-80 flex flex-col">
    <!-- 头部 -->
    <div class="p-4 border-b border-gray-200">
      <h2 class="text-xl font-bold text-gray-800">应急会话</h2>
      <p class="text-sm text-gray-500 mt-1">管理您的应急指导对话</p>
    </div>

    <!-- 新建会话按钮 -->
    <div class="p-4 border-b border-gray-200">
      <button 
        class="w-full px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors flex items-center justify-center"
        @click="createNewSession"
      >
        <i class="fas fa-plus mr-2"></i>
        新建会话
      </button>
    </div>

    <!-- 会话列表 -->
    <div class="flex-1 overflow-y-auto">
      <div v-if="sessions.length === 0" class="p-4 text-center text-gray-500">
        <i class="fas fa-comments text-3xl mb-2"></i>
        <p>暂无会话记录</p>
      </div>
      
      <div v-else class="p-2">
        <div 
          v-for="session in sessions" 
          :key="session.id"
          class="p-3 rounded-lg hover:bg-gray-50 cursor-pointer transition-colors mb-2"
          :class="{ 'bg-primary/10 border border-primary': currentSessionId === session.id }"
          @click="selectSession(session)"
        >
          <div class="flex items-center justify-between">
            <div class="flex-1 min-w-0">
              <h3 class="font-medium text-gray-800 truncate">{{ session.title }}</h3>
              <p class="text-sm text-gray-500 truncate">{{ session.lastMessage }}</p>
              <p class="text-xs text-gray-400 mt-1">
                {{ formatTime(session.updatedAt) }}
              </p>
            </div>
            <div class="flex items-center space-x-2">
              <span class="text-xs px-2 py-1 rounded-full" :class="getScenarioColor(session.scenario)">
                {{ getScenarioLabel(session.scenario) }}
              </span>
              <button 
                class="text-gray-400 hover:text-red-500 transition-colors"
                @click.stop="deleteSession(session.id)"
              >
                <i class="fas fa-trash text-sm"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { EmergencySession } from '@/api/emergency'

const props = defineProps<{
  currentSessionId?: string
}>()

const emit = defineEmits<{
  (e: 'select-session', session: EmergencySession): void
  (e: 'create-session'): void
}>()

const sessions = ref<EmergencySession[]>([])

// 格式化时间
const formatTime = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  if (diff < 60 * 1000) return '刚刚'
  if (diff < 60 * 60 * 1000) return `${Math.floor(diff / (60 * 1000))}分钟前`
  if (diff < 24 * 60 * 60 * 1000) return `${Math.floor(diff / (60 * 60 * 1000))}小时前`
  return new Intl.DateTimeFormat('zh-CN', {
    month: '2-digit',
    day: '2-digit'
  }).format(date)
}

// 获取场景标签
const getScenarioLabel = (scenario: string) => {
  const labels = {
    equipment: '设备操作',
    firstAid: '急救步骤',
    location: '设备定位',
    emergency: '应急处置'
  }
  return labels[scenario as keyof typeof labels] || scenario
}

// 获取场景颜色
const getScenarioColor = (scenario: string) => {
  const colors = {
    equipment: 'bg-blue-100 text-blue-800',
    firstAid: 'bg-red-100 text-red-800',
    location: 'bg-green-100 text-green-800',
    emergency: 'bg-orange-100 text-orange-800'
  }
  return colors[scenario as keyof typeof colors] || 'bg-gray-100 text-gray-800'
}

// 选择会话
const selectSession = (session: EmergencySession) => {
  emit('select-session', session)
}

// 创建新会话
const createNewSession = () => {
  emit('create-session')
}

// 删除会话
const deleteSession = async (sessionId: string) => {
  if (confirm('确定要删除这个会话吗？')) {
    try {
      // TODO: 调用删除会话的 API
      sessions.value = sessions.value.filter(s => s.id !== sessionId)
    } catch (error) {
      console.error('删除会话失败:', error)
    }
  }
}

// 加载会话列表
const loadSessions = async () => {
  try {
    // TODO: 调用获取会话列表的 API
    sessions.value = [
      {
        id: '1',
        title: 'AED使用指导',
        scenario: 'equipment',
        lastMessage: '如何正确使用AED设备？',
        createdAt: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
        updatedAt: new Date(Date.now() - 1000 * 60 * 5).toISOString()
      },
      {
        id: '2',
        title: '心肺复苏操作',
        scenario: 'firstAid',
        lastMessage: '成人CPR的正确步骤是什么？',
        createdAt: new Date(Date.now() - 1000 * 60 * 60).toISOString(),
        updatedAt: new Date(Date.now() - 1000 * 60 * 15).toISOString()
      }
    ]
  } catch (error) {
    console.error('加载会话列表失败:', error)
  }
}

onMounted(() => {
  loadSessions()
})
</script> 