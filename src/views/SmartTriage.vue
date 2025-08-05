<!-- 智能分诊页面 - 重新设计 -->
<template>
  <div class="min-h-screen medical-gradient-bg pt-16">
    <!-- 顶部导航栏（简化版） -->
    <div v-if="showTopBar" class="bg-white shadow-sm border-b border-gray-200">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <el-button @click="resetWizard" type="info" plain size="large" icon="Refresh">
              重新开始分诊
            </el-button>
            <div v-if="isAnalyzing" class="flex items-center text-blue-600">
              <el-icon class="animate-spin mr-2"><Loading /></el-icon>
              <span class="font-medium">AI正在分析患者信息...</span>
            </div>
          </div>

          <!-- 快速操作 -->
          <div class="flex items-center space-x-3">
            <el-button @click="showEmergencyDialog = true" type="danger" size="large" icon="Phone">
              紧急呼叫
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="container mx-auto px-4 py-8">
      <!-- 页面标题 -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-3">智能分诊系统</h1>
        <p class="text-lg text-gray-600 max-w-2xl mx-auto">
          基于国际分诊标准和人工智能技术，为您提供专业的医疗分诊建议
        </p>
      </div>

      <!-- 分步向导组件 -->
      <TriageWizard
        @call-emergency="handleEmergencyCall"
        @analysis-started="handleAnalysisStarted"
        @analysis-completed="handleAnalysisCompleted"
      />

      <!-- 侧边快速工具（桌面端） -->
      <div class="hidden lg:block fixed right-6 top-1/2 transform -translate-y-1/2 space-y-4 z-10">
        <el-tooltip content="紧急联系方式" placement="left">
          <el-button
            circle
            type="danger"
            size="large"
            @click="showEmergencyContacts = true"
            icon="Phone"
          />
        </el-tooltip>

        <el-tooltip content="医疗计算器" placement="left">
          <el-button
            circle
            type="primary"
            size="large"
            @click="showCalculators = true"
            icon="DataAnalysis"
          />
        </el-tooltip>

        <el-tooltip content="常见症状" placement="left">
          <el-button
            circle
            type="info"
            size="large"
            @click="showSymptomGuide = true"
            icon="Document"
          />
        </el-tooltip>
      </div>
    </div>

    <!-- 紧急呼叫确认对话框 -->
    <el-dialog
      v-model="showEmergencyDialog"
      title="紧急呼叫确认"
      width="400px"
      :close-on-click-modal="false"
      class="emergency-dialog"
    >
      <div class="text-center">
        <div
          class="bg-red-100 p-6 rounded-full w-20 h-20 mx-auto mb-4 flex items-center justify-center"
        >
          <el-icon class="text-4xl text-red-600"><Phone /></el-icon>
        </div>
        <h3 class="text-xl font-semibold text-gray-800 mb-2">确认拨打急救电话？</h3>
        <p class="text-sm text-gray-600 mb-6">紧急情况下请立即拨打120急救电话</p>
      </div>
      <template #footer>
        <div class="flex justify-center space-x-4">
          <el-button @click="showEmergencyDialog = false" size="large"> 取消 </el-button>
          <el-button type="danger" @click="callEmergency" size="large" class="px-8">
            <el-icon class="mr-2"><Phone /></el-icon>
            拨打 120
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 紧急联系方式抽屉 -->
    <el-drawer v-model="showEmergencyContacts" title="紧急联系方式" direction="rtl" size="400px">
      <EmergencyContacts />
    </el-drawer>

    <!-- 医疗计算器抽屉 -->
    <el-drawer v-model="showCalculators" title="医疗计算器" direction="rtl" size="500px">
      <MedicalCalculators />
    </el-drawer>

    <!-- 症状指南抽屉 -->
    <el-drawer v-model="showSymptomGuide" title="常见症状指南" direction="rtl" size="400px">
      <CommonSymptoms />
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage, ElNotification } from 'element-plus'
import { Loading, Phone, Refresh, DataAnalysis, Document } from '@element-plus/icons-vue'

// 组件导入
import TriageWizard from '../components/triage/TriageWizard.vue'
import MedicalCalculators from '../components/triage/MedicalCalculators.vue'
import CommonSymptoms from '../components/triage/CommonSymptoms.vue'
import EmergencyContacts from '../components/triage/EmergencyContacts.vue'

// 响应式数据
const isAnalyzing = ref(false)
const showEmergencyDialog = ref(false)
const showEmergencyContacts = ref(false)
const showCalculators = ref(false)
const showSymptomGuide = ref(false)

// 计算属性
const showTopBar = computed(() => {
  return isAnalyzing.value // 只在分析时显示顶部栏
})

// 方法
const handleEmergencyCall = () => {
  showEmergencyDialog.value = true
}

const handleAnalysisStarted = () => {
  isAnalyzing.value = true
}

const handleAnalysisCompleted = () => {
  isAnalyzing.value = false
}

const callEmergency = () => {
  showEmergencyDialog.value = false

  // 在移动设备上直接拨打电话
  if (navigator.userAgent.match(/iPhone|iPad|iPod|Android/i)) {
    window.location.href = 'tel:120'
  } else {
    ElMessage.info('请使用手机拨打急救电话：120')
  }

  ElNotification.warning({
    title: '紧急呼叫',
    message: '正在为您拨打120急救电话...',
  })
}

const resetWizard = () => {
  // 重置向导状态 - 通过刷新页面实现
  window.location.reload()
}
</script>

<style scoped>
/* 动画和过渡效果 */
.el-button {
  transition: all 0.3s ease;
}

.el-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(37, 99, 235, 0.2);
}

/* 紧急对话框样式 */
:deep(.emergency-dialog .el-dialog) {
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
}

:deep(.emergency-dialog .el-dialog__header) {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border-radius: 16px 16px 0 0;
  padding: 20px;
}

:deep(.emergency-dialog .el-dialog__title) {
  color: var(--medical-red);
  font-weight: 600;
}

/* 加载动画 */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* 渐变背景 */
.medical-gradient-bg {
  background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 30%, #e2e8f0 70%, #f8fafc 100%);
  min-height: 100vh;
}

/* 侧边工具栏样式 */
.fixed .el-button--large.is-circle {
  width: 56px;
  height: 56px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.fixed .el-button--large.is-circle:hover {
  transform: translateX(-4px) scale(1.05);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}

/* 页面标题样式 */
h1 {
  background: linear-gradient(135deg, var(--medical-gray-800) 0%, var(--el-color-primary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 抽屉样式优化 */
:deep(.el-drawer__header) {
  padding: 24px;
  border-bottom: 1px solid var(--medical-gray-200);
  margin-bottom: 0;
}

:deep(.el-drawer__body) {
  padding: 24px;
}

/* 响应式优化 */
@media (max-width: 1024px) {
  .fixed.right-6 {
    display: none;
  }
}

@media (max-width: 768px) {
  .container {
    padding-left: 16px;
    padding-right: 16px;
  }

  h1 {
    font-size: 24px;
  }

  .text-lg {
    font-size: 16px;
  }
}

/* 确保布局流畅 */
.container {
  max-width: 1200px;
}
</style>
