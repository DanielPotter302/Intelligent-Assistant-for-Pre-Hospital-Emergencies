<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-semibold mb-4 flex items-center">
      <el-icon class="mr-2 text-green-500"><List /></el-icon>
      常见症状预设
    </h3>

    <div class="space-y-4">
      <!-- 症状分类 -->
      <div v-for="category in symptomCategories" :key="category.name" class="border rounded-lg p-4">
        <h4 class="font-medium text-gray-700 mb-3 flex items-center">
          <el-icon class="mr-2" :class="category.iconClass">
            <component :is="category.icon" />
          </el-icon>
          {{ category.name }}
        </h4>

        <div class="grid grid-cols-2 sm:grid-cols-3 gap-2">
          <el-button
            v-for="symptom in category.symptoms"
            :key="symptom"
            size="small"
            plain
            @click="selectSymptom(symptom)"
            class="symptom-button text-left justify-start"
          >
            <el-icon class="mr-1"><Plus /></el-icon>
            {{ symptom }}
          </el-button>
        </div>
      </div>

      <!-- 快速模板 -->
      <div class="border-t pt-4">
        <h4 class="font-medium text-gray-700 mb-3">快速模板</h4>
        <div class="grid grid-cols-1 gap-2 template-container">
          <el-button
            v-for="template in quickTemplates"
            :key="template.name"
            size="small"
            type="primary"
            plain
            @click="useTemplate(template)"
            class="w-full text-left justify-start template-button"
          >
            <el-icon class="mr-2"><MagicStick /></el-icon>
            {{ template.name }}
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { List, Plus, MagicStick, CircleCheck, Warning, Cpu } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// Emits
const emit = defineEmits<{
  'select-symptom': [symptom: string]
}>()

// 症状分类
const symptomCategories = [
  {
    name: '心血管系统',
    icon: CircleCheck,
    iconClass: 'text-red-500',
    symptoms: ['胸痛', '心悸', '呼吸困难', '晕厥', '下肢水肿', '紫绀'],
  },
  {
    name: '神经系统',
    icon: Cpu,
    iconClass: 'text-blue-500',
    symptoms: ['头痛', '头晕', '昏迷', '抽搐', '肢体无力', '意识障碍'],
  },
  {
    name: '呼吸系统',
    icon: Warning,
    iconClass: 'text-cyan-500',
    symptoms: ['咳嗽', '咳痰', '胸闷', '喘息', '呼吸急促', '胸痛'],
  },
  {
    name: '消化系统',
    icon: Warning,
    iconClass: 'text-orange-500',
    symptoms: ['腹痛', '恶心', '呕吐', '腹泻', '便血', '吞咽困难'],
  },
  {
    name: '外伤急症',
    icon: Warning,
    iconClass: 'text-red-600',
    symptoms: ['外伤出血', '骨折疑似', '烧伤', '溺水', '中毒', '电击伤'],
  },
  {
    name: '全身症状',
    icon: Warning,
    iconClass: 'text-purple-500',
    symptoms: ['发热', '寒战', '乏力', '体重下降', '盗汗', '皮疹'],
  },
]

// 快速模板
const quickTemplates = [
  {
    name: '胸痛综合征',
    symptoms: ['胸痛', '呼吸困难', '出冷汗', '恶心'],
  },
  {
    name: '急性腹痛',
    symptoms: ['腹痛', '恶心', '呕吐', '发热'],
  },
  {
    name: '外伤评估',
    symptoms: ['外伤出血', '疼痛', '肿胀', '活动受限'],
  },
  {
    name: '呼吸困难',
    symptoms: ['呼吸困难', '胸闷', '咳嗽', '紫绀'],
  },
  {
    name: '意识障碍',
    symptoms: ['意识障碍', '头痛', '恶心', '呕吐'],
  },
  {
    name: '发热伴症状',
    symptoms: ['发热', '寒战', '头痛', '乏力'],
  },
]

// 选择症状
const selectSymptom = (symptom: string) => {
  emit('select-symptom', symptom)
  ElMessage.success(`已添加症状：${symptom}`)
}

// 使用模板
const useTemplate = (template: (typeof quickTemplates)[0]) => {
  template.symptoms.forEach((symptom) => {
    emit('select-symptom', symptom)
  })
  ElMessage.success(`已应用模板：${template.name}`)
}
</script>

<style scoped>
.symptom-button {
  transition: all 0.2s ease;
  min-height: 36px;
  font-size: 13px;
}

.symptom-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
  border-color: #3b82f6;
  color: #1d4ed8;
}

/* 分类容器样式 */
.border {
  border-color: #f3f4f6 !important;
  border-width: 2px;
}

/* Element Plus 按钮基础样式优化 */
:deep(.el-button) {
  border-radius: 6px !important;
  border-width: 2px !important;
  font-weight: 500 !important;
  display: flex !important;
  align-items: center !important;
  text-align: left !important;
  transition: all 0.2s ease !important;
}

/* 症状分类按钮样式 */
:deep(.el-button.is-plain:not(.el-button--primary)) {
  background-color: white !important;
  border-color: #e5e7eb !important;
  color: #374151 !important;
}

:deep(.el-button.is-plain:not(.el-button--primary):hover) {
  background-color: #eff6ff !important;
  border-color: #3b82f6 !important;
  color: #1d4ed8 !important;
}

/* 快速模板按钮统一样式 */
.template-button:deep(.el-button--primary.is-plain) {
  background-color: #fef7ff !important;
  border-color: #e879f9 !important;
  color: #a855f7 !important;
  height: 40px !important;
  min-height: 40px !important;
  max-height: 40px !important;
  padding: 8px 12px !important;
  margin: 0 !important;
  box-shadow: none !important;
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  line-height: 1.2 !important;
  text-align: left !important;
  width: 100% !important;
  border-radius: 6px !important;
  position: static !important;
  left: auto !important;
  right: auto !important;
  top: auto !important;
  bottom: auto !important;
  transform: none !important;
}

.template-button:deep(.el-button--primary.is-plain:hover) {
  background-color: #f3e8ff !important;
  border-color: #a855f7 !important;
  color: #7c3aed !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 2px 8px rgba(168, 85, 247, 0.15) !important;
}

.template-button:deep(.el-button--primary.is-plain:focus) {
  background-color: #fef7ff !important;
  border-color: #e879f9 !important;
  color: #a855f7 !important;
  box-shadow: 0 0 0 2px rgba(168, 85, 247, 0.2) !important;
  outline: none !important;
}

.template-button:deep(.el-button--primary.is-plain:active) {
  background-color: #f3e8ff !important;
  border-color: #a855f7 !important;
  color: #7c3aed !important;
  transform: translateY(0px) !important;
  box-shadow: none !important;
}

/* 确保模板按钮图标对齐 */
.template-button :deep(.el-icon) {
  font-size: 14px !important;
  margin-right: 8px !important;
}

/* 模板容器对齐修复 */
.template-container {
  margin: 0 !important;
  padding: 0 !important;
  display: grid !important;
  grid-template-columns: 1fr !important;
  gap: 8px !important;
  width: 100% !important;
  box-sizing: border-box !important;
  position: relative !important;
  left: 0 !important;
  right: 0 !important;
}

/* 强制所有模板按钮左边缘对齐 */
.template-container .template-button {
  margin-left: 0 !important;
  margin-right: 0 !important;
  padding-left: 0 !important;
  padding-right: 0 !important;
  position: relative !important;
  left: 0 !important;
  right: 0 !important;
}

.template-container .template-button:deep(.el-button) {
  margin: 0 !important;
  padding: 8px 12px !important;
  box-sizing: border-box !important;
  width: 100% !important;
  position: relative !important;
  left: 0 !important;
  transform: none !important;
}

.template-container .template-button:deep(.el-button:hover) {
  transform: translateY(-1px) !important;
  margin: 0 !important;
  left: 0 !important;
}

/* 重置第一个按钮的特殊样式 */
.template-container .template-button:first-child:deep(.el-button) {
  margin-top: 0 !important;
  margin-left: 0 !important;
  margin-bottom: 0 !important;
  margin-right: 0 !important;
}

.template-container .template-button:last-child:deep(.el-button) {
  margin-bottom: 0 !important;
}
</style>
