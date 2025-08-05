<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
    <h3 class="text-lg font-semibold text-gray-800 mb-4">快速操作</h3>
    
    <div class="grid grid-cols-2 gap-3">
      <template v-if="currentScenario">
        <button 
          v-for="action in currentScenario.quickActions"
          :key="action.id"
          class="flex items-center justify-center p-3 rounded-lg hover:bg-opacity-90 transition-colors"
          :class="getActionColorClass(action.color)"
          @click="handleAction(action)"
        >
          <i :class="[action.icon, 'mr-2']"></i>
          {{ action.title }}
        </button>
      </template>
      <template v-else>
        <div class="col-span-2 text-center text-gray-500 py-4">
          请先选择应急场景
        </div>
      </template>
    </div>

    <!-- 操作指南弹窗 -->
    <div v-if="showGuide" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg max-w-md w-full mx-4 max-h-[80vh] overflow-y-auto">
        <div class="p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-xl font-bold text-gray-800">{{ guideTitle }}</h3>
            <button 
              class="text-gray-400 hover:text-gray-600"
              @click="closeGuide"
            >
              <i class="fas fa-times"></i>
            </button>
          </div>
          
          <div class="space-y-4">
            <div v-for="(step, index) in guideSteps" :key="index" class="flex items-start space-x-3">
              <div class="w-6 h-6 rounded-full bg-primary text-white flex-shrink-0 flex items-center justify-center text-sm">
                {{ index + 1 }}
              </div>
              <p class="text-gray-700">{{ step }}</p>
            </div>
          </div>

          <div class="mt-6 flex space-x-3">
            <button 
              v-if="showEmergencyCall"
              class="flex-1 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors"
              @click="startEmergencyCall"
            >
              立即拨打120
            </button>
            <button 
              class="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              @click="closeGuide"
            >
              关闭
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { emergencyScenarios, type EmergencyScenario } from '@/config/emergency'

const props = defineProps<{
  scenario?: keyof typeof emergencyScenarios
}>()

const emit = defineEmits<{
  (e: 'send-message', message: string): void
}>()

const showGuide = ref(false)
const guideTitle = ref('')
const guideSteps = ref<string[]>([])
const showEmergencyCall = ref(false)

// 获取当前场景配置
const currentScenario = computed(() => {
  if (!props.scenario) return null
  return emergencyScenarios[props.scenario]
})

// 获取操作按钮的颜色类
const getActionColorClass = (color: string) => {
  const colorMap: Record<string, string> = {
    red: 'bg-red-500 text-white',
    blue: 'bg-blue-500 text-white',
    green: 'bg-green-500 text-white',
    yellow: 'bg-yellow-500 text-white',
    purple: 'bg-purple-500 text-white',
    orange: 'bg-orange-500 text-white'
  }
  return colorMap[color] || 'bg-gray-500 text-white'
}

// 处理快速操作
const handleAction = (action: EmergencyScenario['quickActions'][0]) => {
  switch (action.id) {
    case 'call-120':
      callEmergency()
      break
    case 'cpr':
      showCPRGuide()
      break
    case 'bleeding':
      showBleedingGuide()
      break
    case 'fracture':
      showFractureGuide()
      break
    case 'burn':
      showBurnGuide()
      break
    case 'poison':
      showPoisonGuide()
      break
    default:
      // 发送操作相关的消息
      emit('send-message', `请问${action.title}的具体步骤是什么？`)
  }
}

// 拨打急救电话
const callEmergency = () => {
  if ('navigator' in window && 'share' in navigator) {
    navigator.share({
      title: '紧急情况',
      text: '需要紧急医疗救助',
      url: 'tel:120'
    })
  } else {
    window.location.href = 'tel:120'
  }
}

// 显示心肺复苏指南
const showCPRGuide = () => {
  guideTitle.value = '心肺复苏操作步骤'
  guideSteps.value = [
    '确保现场安全，检查伤者意识',
    '呼叫120急救电话',
    '检查呼吸和脉搏',
    '开始胸外按压：30次按压，2次人工呼吸',
    '持续进行直到专业医护人员到达'
  ]
  showEmergencyCall.value = true
  showGuide.value = true
}

// 显示止血指南
const showBleedingGuide = () => {
  guideTitle.value = '止血处理步骤'
  guideSteps.value = [
    '直接压迫伤口',
    '抬高受伤部位',
    '使用清洁敷料包扎',
    '如果出血严重，立即拨打120',
    '保持伤者温暖和安静'
  ]
  showEmergencyCall.value = true
  showGuide.value = true
}

// 显示骨折固定指南
const showFractureGuide = () => {
  guideTitle.value = '骨折固定步骤'
  guideSteps.value = [
    '不要移动骨折部位',
    '使用夹板或硬物固定',
    '用绷带或布条固定',
    '保持受伤部位高于心脏',
    '立即就医处理'
  ]
  showEmergencyCall.value = true
  showGuide.value = true
}

// 显示烧伤处理指南
const showBurnGuide = () => {
  guideTitle.value = '烧伤处理步骤'
  guideSteps.value = [
    '立即用冷水冲洗15-20分钟',
    '不要使用冰块或冰水',
    '不要刺破水泡',
    '用清洁敷料覆盖',
    '严重烧伤立即就医'
  ]
  showEmergencyCall.value = true
  showGuide.value = true
}

// 显示中毒处理指南
const showPoisonGuide = () => {
  guideTitle.value = '中毒处理步骤'
  guideSteps.value = [
    '立即拨打120或中毒急救电话',
    '不要催吐（除非医生指导）',
    '保留毒物样本',
    '保持呼吸道通畅',
    '等待专业医护人员'
  ]
  showEmergencyCall.value = true
  showGuide.value = true
}

// 关闭指南
const closeGuide = () => {
  showGuide.value = false
  showEmergencyCall.value = false
}

// 开始紧急呼叫
const startEmergencyCall = () => {
  callEmergency()
  closeGuide()
}
</script> 