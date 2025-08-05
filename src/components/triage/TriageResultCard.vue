<template>
  <div class="bg-white rounded-lg shadow-lg border-l-4" :class="levelBorderClass">
    <div class="p-6">
      <!-- 分诊等级标题 -->
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center">
          <div
            class="w-12 h-12 rounded-full flex items-center justify-center mr-4"
            :class="levelBgClass"
          >
            <el-icon class="text-2xl text-white">
              <component :is="levelIcon" />
            </el-icon>
          </div>
          <div>
            <h2 class="text-2xl font-bold" :class="levelTextClass">
              {{ levelDisplayText }}
            </h2>
            <p class="text-gray-600">{{ result.levelDescription }}</p>
          </div>
        </div>

        <!-- 紧急呼叫按钮 -->
        <div v-if="result.callEmergency" class="flex space-x-3">
          <el-button
            type="danger"
            size="large"
            @click="$emit('call-emergency')"
            class="animate-pulse"
          >
            <el-icon class="mr-2"><Phone /></el-icon>
            拨打 120
          </el-button>
        </div>
      </div>

      <!-- 严重程度和置信度 -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <div class="bg-gray-50 rounded-lg p-4">
          <h4 class="font-semibold text-gray-700 mb-2">病情严重程度</h4>
          <p class="text-lg">{{ result.severity }}</p>
        </div>
        <div
          v-if="analysis && typeof analysis.confidence === 'number'"
          class="bg-gray-50 rounded-lg p-4"
        >
          <h4 class="font-semibold text-gray-700 mb-2">AI置信度</h4>
          <div class="flex items-center">
            <el-progress
              :percentage="Math.round(analysis.confidence * 100)"
              :color="getConfidenceColor(analysis.confidence)"
              class="flex-1 mr-3"
            />
            <span class="text-sm font-medium">{{ Math.round(analysis.confidence * 100) }}%</span>
          </div>
        </div>
      </div>

      <!-- 立即行动建议 -->
      <div v-if="result.immediateActions.length > 0" class="mb-6">
        <h4 class="font-semibold text-gray-700 mb-3 flex items-center">
          <el-icon class="mr-2 text-red-500"><Clock /></el-icon>
          立即行动
        </h4>
        <div class="bg-red-50 border border-red-200 rounded-lg p-4">
          <ul class="space-y-2">
            <li
              v-for="(action, index) in result.immediateActions"
              :key="index"
              class="flex items-start"
            >
              <span
                class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-red-500 text-white text-sm font-bold mr-3 mt-0.5 flex-shrink-0"
              >
                {{ index + 1 }}
              </span>
              <span class="text-red-800">{{ action }}</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- 治疗建议 -->
      <div v-if="result.recommendations.length > 0" class="mb-6">
        <h4 class="font-semibold text-gray-700 mb-3 flex items-center">
          <el-icon class="mr-2 text-blue-500"><Document /></el-icon>
          治疗建议
        </h4>
        <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <ul class="space-y-2">
            <li
              v-for="(recommendation, index) in result.recommendations"
              :key="index"
              class="flex items-start"
            >
              <el-icon class="text-blue-500 mr-2 mt-1 flex-shrink-0"><ArrowRight /></el-icon>
              <span class="text-blue-800">{{ recommendation }}</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- 计算评分 -->
      <div v-if="result.calculatedScores && result.calculatedScores.length > 0" class="mb-6">
        <h4 class="font-semibold text-gray-700 mb-3 flex items-center">
          <el-icon class="mr-2 text-purple-500"><DataAnalysis /></el-icon>
          医学评分
        </h4>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div
            v-for="score in result.calculatedScores"
            :key="score.name"
            class="bg-purple-50 border border-purple-200 rounded-lg p-4"
          >
            <div class="flex justify-between items-center mb-2">
              <h5 class="font-medium text-purple-800">{{ score.name }}</h5>
              <span class="text-lg font-bold text-purple-600">{{ score.score }}</span>
            </div>
            <p class="text-sm text-purple-700">{{ score.interpretation }}</p>
          </div>
        </div>
      </div>

      <!-- 参考指南 -->
      <div v-if="result.referenceGuidelines && result.referenceGuidelines.length > 0" class="mb-6">
        <h4 class="font-semibold text-gray-700 mb-3 flex items-center">
          <el-icon class="mr-2 text-green-500"><Reading /></el-icon>
          参考指南
        </h4>
        <div class="bg-green-50 border border-green-200 rounded-lg p-4">
          <div class="flex flex-wrap gap-2">
            <el-tag
              v-for="guideline in result.referenceGuidelines"
              :key="guideline"
              type="success"
              size="small"
            >
              {{ guideline }}
            </el-tag>
          </div>
        </div>
      </div>

      <!-- 预估等待时间 -->
      <div v-if="result.estimatedWaitTime" class="mb-6">
        <h4 class="font-semibold text-gray-700 mb-3 flex items-center">
          <el-icon class="mr-2 text-orange-500"><Timer /></el-icon>
          预估等待时间
        </h4>
        <div class="bg-orange-50 border border-orange-200 rounded-lg p-4">
          <p class="text-orange-800 font-medium">{{ result.estimatedWaitTime }}</p>
        </div>
      </div>

      <!-- AI分析详情 -->
      <div v-if="analysis && showAnalysisDetail" class="mb-6">
        <h4 class="font-semibold text-gray-700 mb-3 flex items-center">
          <el-icon class="mr-2 text-indigo-500"><Cpu /></el-icon>
          AI分析详情
        </h4>
        <div class="bg-indigo-50 border border-indigo-200 rounded-lg p-4">
          <p class="text-indigo-800 mb-3">{{ analysis.analysis }}</p>
          <div v-if="analysis.reasoning && analysis.reasoning.length > 0">
            <h5 class="font-medium text-indigo-700 mb-2">推理过程：</h5>
            <ul class="space-y-1">
              <li
                v-for="(reason, index) in analysis.reasoning"
                :key="index"
                class="text-sm text-indigo-700"
              >
                {{ index + 1 }}. {{ reason }}
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="flex justify-between items-center pt-4 border-t">
        <el-button
          @click="showAnalysisDetail = !showAnalysisDetail"
          type="info"
          plain
          v-if="analysis"
        >
          {{ showAnalysisDetail ? '隐藏' : '显示' }}AI分析详情
        </el-button>

        <div class="flex space-x-3">
          <el-button @click="printResult" type="success" plain>
            <el-icon class="mr-2"><Printer /></el-icon>
            打印报告
          </el-button>
          <el-button @click="shareResult" type="primary" plain>
            <el-icon class="mr-2"><Share /></el-icon>
            分享结果
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Phone,
  Clock,
  Document,
  ArrowRight,
  DataAnalysis,
  Reading,
  Timer,
  Cpu,
  Printer,
  Share,
  Warning,
  Check,
  InfoFilled,
} from '@element-plus/icons-vue'
import type { TriageResult, TriageResponse as AITriageResponse } from '@/types/api'

// Props 和 Emits
const props = defineProps<{
  result: TriageResult
  analysis?: AITriageResponse | null
}>()

const emit = defineEmits<{
  'call-emergency': []
}>()

// 本地状态
const showAnalysisDetail = ref(false)

// 计算属性：分诊等级样式
const levelBorderClass = computed(() => {
  const classMap = {
    red: 'border-red-500',
    orange: 'border-orange-500',
    yellow: 'border-yellow-500',
    green: 'border-green-500',
    blue: 'border-blue-500',
    white: 'border-gray-400',
  }
  return classMap[props.result.level] || 'border-gray-400'
})

const levelBgClass = computed(() => {
  const classMap = {
    red: 'bg-red-500',
    orange: 'bg-orange-500',
    yellow: 'bg-yellow-500',
    green: 'bg-green-500',
    blue: 'bg-blue-500',
    white: 'bg-gray-400',
  }
  return classMap[props.result.level] || 'bg-gray-400'
})

const levelTextClass = computed(() => {
  const classMap = {
    red: 'text-red-600',
    orange: 'text-orange-600',
    yellow: 'text-yellow-600',
    green: 'text-green-600',
    blue: 'text-blue-600',
    white: 'text-gray-600',
  }
  return classMap[props.result.level] || 'text-gray-600'
})

const levelDisplayText = computed(() => {
  const textMap = {
    red: '危重（红色）',
    orange: '严重（橙色）',
    yellow: '紧急（黄色）',
    green: '普通（绿色）',
    blue: '非紧急（蓝色）',
    white: '无需处理（白色）',
  }
  return textMap[props.result.level] || props.result.level
})

const levelIcon = computed(() => {
  const iconMap = {
    red: Warning,
    orange: Warning,
    yellow: Warning,
    green: Check,
    blue: InfoFilled,
    white: InfoFilled,
  }
  return iconMap[props.result.level] || InfoFilled
})

// 获取置信度颜色
const getConfidenceColor = (confidence: number): string => {
  if (confidence >= 0.8) return '#67c23a'
  if (confidence >= 0.6) return '#e6a23c'
  return '#f56c6c'
}

// 打印结果
const printResult = () => {
  window.print()
  ElMessage.success('准备打印分诊报告')
}

// 分享结果
const shareResult = () => {
  const shareText = `分诊结果：${levelDisplayText.value}\n严重程度：${
    props.result.severity
  }\n建议：${props.result.recommendations.join(', ')}`

  if (navigator.share) {
    navigator.share({
      title: '智能分诊结果',
      text: shareText,
    })
  } else {
    navigator.clipboard
      .writeText(shareText)
      .then(() => {
        ElMessage.success('分诊结果已复制到剪贴板')
      })
      .catch(() => {
        ElMessage.error('复制失败，请手动复制')
      })
  }
}
</script>

<style scoped>
/* 打印样式 */
@media print {
  .el-button {
    display: none !important;
  }
}

/* 动画效果 */
.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>
