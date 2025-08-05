<template>
  <el-dialog
    v-model="visible"
    title="留言管理"
    width="90%"
    :close-on-click-modal="false"
    class="message-manager-dialog"
  >
    <div class="message-manager">
      <!-- 筛选和搜索 -->
      <div class="filter-bar">
        <div class="filter-left">
          <el-select v-model="statusFilter" placeholder="状态筛选" clearable @change="loadMessages">
            <el-option label="全部" value="" />
            <el-option label="未读" value="unread" />
            <el-option label="已读" value="read" />
          </el-select>
          <el-button type="primary" @click="loadMessages" :loading="loading">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
        <div class="filter-right">
          <span class="total-count">共 {{ total }} 条留言</span>
        </div>
      </div>

      <!-- 留言列表 -->
      <div class="message-list" v-loading="loading">
        <div v-if="messages.length === 0" class="empty-state">
          <el-empty description="暂无留言数据" />
        </div>
        <div v-else>
          <div
            v-for="message in messages"
            :key="message.id"
            class="message-item"
            :class="{ unread: message.status === 'unread' }"
          >
            <div class="message-header">
              <div class="message-info">
                <span class="sender-name">{{ message.name }}</span>
                <span class="sender-email">{{ message.email }}</span>
                <el-tag :type="getStatusType(message.status)" size="small" class="status-tag">
                  {{ getStatusText(message.status) }}
                </el-tag>
              </div>
              <div class="message-time">
                {{ formatTime(message.created_at) }}
              </div>
            </div>

            <div class="message-content">
              <p>{{ message.content }}</p>
            </div>

            <div class="message-actions">
              <el-button
                v-if="message.status === 'unread'"
                size="small"
                type="primary"
                @click="markAsRead(message.id)"
              >
                标记已读
              </el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div class="pagination" v-if="total > 0">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadMessages"
          @current-change="loadMessages"
        />
      </div>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import { getContactMessages, markMessageAsRead, type ContactMessage } from '@/api/message'

interface Props {
  modelValue: boolean
}

interface Emits {
  (e: 'update:modelValue', value: boolean): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

const visible = ref(false)
const loading = ref(false)

// 列表数据
const messages = ref<ContactMessage[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const statusFilter = ref('')

// 监听props变化
watch(
  () => props.modelValue,
  (newVal) => {
    visible.value = newVal
    if (newVal) {
      loadMessages()
    }
  },
)

watch(visible, (newVal) => {
  emit('update:modelValue', newVal)
})

// 加载留言列表
const loadMessages = async () => {
  loading.value = true
  try {
    const response = await getContactMessages({
      status_filter: statusFilter.value || undefined,
      page: currentPage.value,
      size: pageSize.value,
    })

    if (response.code === 200) {
      messages.value = response.data.messages
      total.value = response.data.total
    } else {
      ElMessage.error(response.message || '获取留言列表失败')
    }
  } catch (error: any) {
    console.error('获取留言列表失败:', error)
    ElMessage.error(error.message || '获取留言列表失败')
  } finally {
    loading.value = false
  }
}

// 标记为已读
const markAsRead = async (messageId: string) => {
  try {
    const response = await markMessageAsRead(messageId)
    if (response.code === 200) {
      ElMessage.success('已标记为已读')
      loadMessages()
    } else {
      ElMessage.error(response.message || '操作失败')
    }
  } catch (error: any) {
    console.error('标记已读失败:', error)
    ElMessage.error(error.message || '操作失败')
  }
}

// 获取状态类型
const getStatusType = (status: string) => {
  switch (status) {
    case 'unread':
      return 'danger'
    case 'read':
      return 'warning'
    default:
      return 'info'
  }
}

// 获取状态文本
const getStatusText = (status: string) => {
  switch (status) {
    case 'unread':
      return '未读'
    case 'read':
      return '已读'
    default:
      return '未知'
  }
}

// 格式化时间
const formatTime = (timeStr: string) => {
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  if (props.modelValue) {
    loadMessages()
  }
})
</script>

<style scoped>
.message-manager {
  max-height: 70vh;
  display: flex;
  flex-direction: column;
}

.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
}

.filter-left {
  display: flex;
  gap: 12px;
  align-items: center;
}

.filter-right {
  color: #666;
  font-size: 14px;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  max-height: 50vh;
}

.message-item {
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 12px;
  background: white;
  transition: all 0.2s ease;
}

.message-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.message-item.unread {
  border-left: 4px solid #f56565;
  background: #fef5e7;
}

.message-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.message-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sender-name {
  font-weight: 600;
  color: #2d3748;
}

.sender-email {
  color: #718096;
  font-size: 14px;
}

.status-tag {
  margin-left: 8px;
}

.message-time {
  color: #a0aec0;
  font-size: 12px;
}

.message-content {
  margin-bottom: 12px;
  line-height: 1.6;
  color: #4a5568;
}

.message-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

:deep(.message-manager-dialog .el-dialog) {
  max-height: 90vh;
  overflow: hidden;
}

:deep(.message-manager-dialog .el-dialog__body) {
  padding: 20px;
  max-height: calc(90vh - 120px);
  overflow: hidden;
}
</style>
