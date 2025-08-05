<template>
  <div class="symptom-form">
    <!-- 关键症状评估卡片 -->
    <div class="medical-card critical-info">
      <div class="medical-card-header">
        <el-icon class="medical-card-icon critical"><Warning /></el-icon>
        <h3 class="medical-card-title">关键症状评估</h3>
        <div class="ml-auto">
          <span class="status-indicator" :class="getSymptomSeverity()"></span>
          <span class="text-sm text-gray-500">{{ getSeverityText() }}</span>
        </div>
      </div>

      <!-- 主诉描述 -->
      <div class="priority-section">
        <div class="section-header">
          <el-icon class="section-icon"><ChatDotSquare /></el-icon>
          <h4 class="section-title">患者主诉</h4>
          <span class="required-badge">必填</span>
        </div>
        <el-input
          v-model="localSymptomInfo.chiefComplaint"
          type="textarea"
          :rows="3"
          placeholder="请详细描述患者的主要症状和不适..."
          maxlength="200"
          show-word-limit
          class="priority-textarea"
        />
        <div class="hint-text">
          <el-icon class="mr-1"><InfoFilled /></el-icon>
          请尽量详细描述症状的性质、部位、程度等
        </div>
      </div>

      <!-- 症状选择器 -->
      <div class="priority-section">
        <div class="section-header">
          <el-icon class="section-icon"><List /></el-icon>
          <h4 class="section-title">症状清单</h4>
          <span class="required-badge">必填</span>
        </div>

        <!-- 已选症状展示 -->
        <div v-if="localSymptomInfo.symptoms.length > 0" class="selected-symptoms">
          <h5 class="selected-title">已选择的症状：</h5>
          <div class="symptoms-tags">
            <el-tag
              v-for="(symptom, index) in localSymptomInfo.symptoms"
              :key="symptom"
              closable
              type="danger"
              size="large"
              class="symptom-tag"
              @close="removeSymptom(index)"
            >
              {{ symptom }}
            </el-tag>
          </div>
        </div>

        <!-- 症状分类选择 -->
        <div class="symptom-categories">
          <el-collapse v-model="activeSymptomCategory" accordion>
            <!-- 紧急症状 -->
            <el-collapse-item title="🚨 紧急危险症状" name="emergency" class="emergency-category">
              <div class="symptoms-grid">
                <el-button
                  v-for="symptom in emergencySymptoms"
                  :key="symptom"
                  @click="toggleSymptom(symptom)"
                  :type="localSymptomInfo.symptoms.includes(symptom) ? 'danger' : 'default'"
                  :plain="!localSymptomInfo.symptoms.includes(symptom)"
                  size="large"
                  class="symptom-button emergency-symptom"
                >
                  {{ symptom }}
                </el-button>
              </div>
            </el-collapse-item>

            <!-- 常见症状 -->
            <el-collapse-item title="🔍 常见症状" name="common">
              <div class="symptoms-grid">
                <el-button
                  v-for="symptom in commonSymptoms"
                  :key="symptom"
                  @click="toggleSymptom(symptom)"
                  :type="localSymptomInfo.symptoms.includes(symptom) ? 'primary' : 'default'"
                  :plain="!localSymptomInfo.symptoms.includes(symptom)"
                  size="default"
                  class="symptom-button"
                >
                  {{ symptom }}
                </el-button>
              </div>
            </el-collapse-item>

            <!-- 其他症状 -->
            <el-collapse-item title="📝 其他症状" name="other">
              <div class="custom-symptom-input">
                <el-input
                  v-model="customSymptom"
                  placeholder="输入其他症状..."
                  @keypress.enter="addCustomSymptom"
                  class="mr-4"
                >
                  <template #append>
                    <el-button @click="addCustomSymptom" type="primary" icon="Plus">添加</el-button>
                  </template>
                </el-input>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>
      </div>
    </div>

    <!-- 补充信息卡片 -->
    <div class="medical-card secondary-info">
      <div class="medical-card-header">
        <el-icon class="medical-card-icon"><Document /></el-icon>
        <h3 class="medical-card-title">补充信息</h3>
        <div class="ml-auto">
          <span class="status-indicator status-info"></span>
          <span class="text-sm text-gray-500">详细描述</span>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 疼痛评分 -->
        <div class="info-item">
          <label class="medical-label">
            <el-icon class="mr-2 text-red-500"><Warning /></el-icon>
            疼痛程度 (0-10分)
          </label>
          <div class="pain-assessment">
            <el-slider
              v-model="localSymptomInfo.painLevel"
              :max="10"
              :marks="painMarks"
              show-tooltip
              :format-tooltip="formatPainLevel"
              class="pain-slider"
            />
            <div class="pain-description">
              {{ getPainDescription(localSymptomInfo.painLevel) }}
            </div>
          </div>
        </div>

        <!-- 持续时间 -->
        <div class="info-item">
          <label class="medical-label">
            <el-icon class="mr-2 text-blue-500"><Clock /></el-icon>
            症状持续时间
          </label>
          <el-select
            v-model="localSymptomInfo.duration"
            placeholder="选择症状持续时间"
            size="large"
            class="w-full"
          >
            <el-option-group label="急性期">
              <el-option label="刚刚发生 (< 5分钟)" value="<5分钟" />
              <el-option label="5-30分钟" value="5-30分钟" />
              <el-option label="30分钟-1小时" value="30分钟-1小时" />
            </el-option-group>
            <el-option-group label="亚急性期">
              <el-option label="1-6小时" value="1-6小时" />
              <el-option label="6-24小时" value="6-24小时" />
            </el-option-group>
            <el-option-group label="慢性期">
              <el-option label="1-7天" value="1-7天" />
              <el-option label="超过1周" value=">1周" />
            </el-option-group>
          </el-select>
        </div>

        <!-- 受伤机制 -->
        <div class="info-item">
          <label class="medical-label">
            <el-icon class="mr-2 text-orange-500"><Tools /></el-icon>
            受伤机制
          </label>
          <el-select
            v-model="localSymptomInfo.mechanism"
            placeholder="选择受伤机制"
            size="large"
            class="w-full"
            filterable
            allow-create
          >
            <el-option-group label="外伤">
              <el-option label="车祸碰撞" value="车祸碰撞" />
              <el-option label="高处跌落" value="高处跌落" />
              <el-option label="运动损伤" value="运动损伤" />
              <el-option label="刀切伤" value="刀切伤" />
              <el-option label="烧烫伤" value="烧烫伤" />
            </el-option-group>
            <el-option-group label="内科">
              <el-option label="突然发病" value="突然发病" />
              <el-option label="逐渐加重" value="逐渐加重" />
              <el-option label="反复发作" value="反复发作" />
            </el-option-group>
          </el-select>
        </div>

        <!-- 诱发因素 -->
        <div class="info-item">
          <label class="medical-label">
            <el-icon class="mr-2 text-purple-500"><Lightning /></el-icon>
            诱发因素 (记录在其他描述中)
          </label>
          <el-input
            placeholder="如：活动后、进食后、情绪激动等"
            size="large"
            class="w-full"
            disabled
          />
        </div>
      </div>

      <!-- 其他描述 -->
      <div class="mt-6">
        <label class="medical-label">
          <el-icon class="mr-2 text-gray-500"><EditPen /></el-icon>
          其他症状描述
        </label>
        <el-input
          v-model="localSymptomInfo.additionalInfo"
          type="textarea"
          :rows="3"
          placeholder="补充说明其他相关症状、伴随症状等..."
          maxlength="300"
          show-word-limit
        />
      </div>
    </div>

    <!-- 症状严重程度警告 -->
    <div v-if="hasEmergencySymptoms" class="emergency-warning">
      <div class="warning-content">
        <el-icon class="warning-icon"><Warning /></el-icon>
        <div>
          <h4 class="warning-title">检测到紧急症状！</h4>
          <p class="warning-message">患者存在危险症状，建议立即寻求医疗帮助</p>
        </div>
        <el-button type="danger" size="large" @click="$emit('emergency-detected')">
          立即呼叫急救
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed, watch, ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Warning,
  ChatDotSquare,
  InfoFilled,
  List,
  Document,
  Clock,
  Tools,
  Lightning,
  EditPen,
  Plus,
} from '@element-plus/icons-vue'
import type { SymptomInfo } from '@/api/triage'

// Props 和 Emits
const props = defineProps<{
  modelValue: SymptomInfo
}>()

const emit = defineEmits<{
  'update:modelValue': [value: SymptomInfo]
  'emergency-detected': []
}>()

// 本地状态
const localSymptomInfo = reactive<SymptomInfo>({
  chiefComplaint: '',
  symptoms: [],
  painLevel: undefined,
  duration: '',
  mechanism: '',
  additionalInfo: '',
})

// 应用 props 的值
Object.assign(localSymptomInfo, props.modelValue)

const activeSymptomCategory = ref(['emergency'])
const customSymptom = ref('')

// 症状数据
const emergencySymptoms = [
  '胸痛',
  '呼吸困难',
  '意识障碍',
  '大出血',
  '严重外伤',
  '窒息',
  '心跳停止',
  '抽搐',
  '严重头痛',
  '剧烈腹痛',
  '高热',
  '过敏性休克',
]

const commonSymptoms = [
  '头痛',
  '发热',
  '咳嗽',
  '恶心',
  '呕吐',
  '腹痛',
  '腹泻',
  '头晕',
  '乏力',
  '失眠',
  '关节痛',
  '肌肉痛',
  '皮疹',
  '瘙痒',
]

// 疼痛评分标记
const painMarks = {
  0: '无痛',
  2: '轻微',
  4: '轻度',
  6: '中度',
  8: '重度',
  10: '剧痛',
}

// 计算属性
const hasEmergencySymptoms = computed(() => {
  return localSymptomInfo.symptoms.some((symptom) => emergencySymptoms.includes(symptom))
})

// 方法
const getSymptomSeverity = () => {
  if (hasEmergencySymptoms.value) return 'status-danger'
  if (localSymptomInfo.symptoms.length > 3) return 'status-warning'
  if (localSymptomInfo.symptoms.length > 0) return 'status-info'
  return 'status-normal'
}

const getSeverityText = () => {
  if (hasEmergencySymptoms.value) return '危险症状'
  if (localSymptomInfo.symptoms.length > 3) return '症状较多'
  if (localSymptomInfo.symptoms.length > 0) return '有症状'
  return '无症状'
}

const toggleSymptom = (symptom: string) => {
  const index = localSymptomInfo.symptoms.indexOf(symptom)
  if (index >= 0) {
    localSymptomInfo.symptoms.splice(index, 1)
  } else {
    localSymptomInfo.symptoms.push(symptom)

    // 如果是紧急症状，发出警告
    if (emergencySymptoms.includes(symptom)) {
      ElMessage.warning(`已添加紧急症状：${symptom}`)
    }
  }
}

const removeSymptom = (index: number) => {
  localSymptomInfo.symptoms.splice(index, 1)
}

const addCustomSymptom = () => {
  if (
    customSymptom.value.trim() &&
    !localSymptomInfo.symptoms.includes(customSymptom.value.trim())
  ) {
    localSymptomInfo.symptoms.push(customSymptom.value.trim())
    customSymptom.value = ''
    ElMessage.success('症状已添加')
  }
}

const formatPainLevel = (value: number) => {
  const levels = [
    '无痛',
    '轻微',
    '轻微',
    '轻度',
    '轻度',
    '中度',
    '中度',
    '重度',
    '重度',
    '严重',
    '剧烈',
  ]
  return `${value}分`
}

const getPainDescription = (level: number | undefined) => {
  if (!level) return '请选择疼痛程度'
  const descriptions = [
    '无疼痛感觉',
    '轻微不适',
    '轻微不适',
    '轻度疼痛，不影响活动',
    '轻度疼痛，稍有影响',
    '中度疼痛，影响日常活动',
    '中度疼痛，明显不适',
    '重度疼痛，严重影响活动',
    '重度疼痛，难以忍受',
    '极重度疼痛，无法活动',
    '最高程度疼痛，无法忍受',
  ]
  return descriptions[level] || ''
}

// 监听本地变化并向上传递
watch(
  () => localSymptomInfo,
  (newValue) => {
    emit('update:modelValue', { ...newValue })
  },
  { deep: true }
)

// 监听外部变化
watch(
  () => props.modelValue,
  (newValue) => {
    Object.assign(localSymptomInfo, newValue)
  },
  { deep: true }
)

// 监听紧急症状
watch(
  () => hasEmergencySymptoms.value,
  (hasEmergency) => {
    if (hasEmergency) {
      emit('emergency-detected')
    }
  }
)
</script>

<style scoped>
.symptom-form {
  space-y: 24px;
}

/* 关键信息卡片 */
.critical-info {
  border-left: 4px solid var(--medical-red);
  box-shadow: 0 4px 20px rgba(220, 38, 38, 0.1);
}

.critical-info .medical-card-icon.critical {
  color: var(--medical-red);
  animation: pulse 2s infinite;
}

/* 次要信息卡片 */
.secondary-info {
  border-left: 4px solid var(--medical-blue);
}

/* 优先级区域 */
.priority-section {
  background: linear-gradient(135deg, #fef2f2 0%, #fff 100%);
  border: 1px solid #fecaca;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.section-icon {
  width: 20px;
  height: 20px;
  color: var(--medical-red);
  margin-right: 8px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: var(--medical-gray-800);
  margin: 0;
  flex: 1;
}

.required-badge {
  background: var(--medical-red);
  color: white;
  font-size: 12px;
  padding: 4px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.priority-textarea {
  margin-bottom: 8px;
}

:deep(.priority-textarea .el-textarea__inner) {
  border: 2px solid #fca5a5 !important;
  background: #fef2f2 !important;
}

:deep(.priority-textarea .el-textarea__inner:focus) {
  border-color: var(--medical-red) !important;
}

.hint-text {
  font-size: 13px;
  color: var(--medical-gray-600);
  display: flex;
  align-items: center;
}

/* 已选症状展示 */
.selected-symptoms {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}

.selected-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--medical-gray-700);
  margin: 0 0 12px 0;
}

.symptoms-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.symptom-tag {
  margin: 0;
  font-weight: 500;
}

/* 症状分类 */
.symptom-categories {
  margin-top: 16px;
}

:deep(.emergency-category .el-collapse-item__header) {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border-color: #f87171;
  color: var(--medical-red);
  font-weight: 600;
}

/* 症状网格 */
.symptoms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.symptom-button {
  height: auto;
  padding: 12px 16px;
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.2s ease;
  white-space: normal;
  line-height: 1.4;
}

.emergency-symptom {
  border-color: var(--medical-red);
  color: var(--medical-red);
}

.emergency-symptom:hover {
  background: var(--medical-red);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
}

.symptom-button:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 自定义症状输入 */
.custom-symptom-input {
  margin-top: 16px;
}

/* 信息项 */
.info-item {
  margin-bottom: 20px;
}

/* 疼痛评估 */
.pain-assessment {
  margin-top: 8px;
}

.pain-slider {
  margin: 16px 0;
}

.pain-description {
  text-align: center;
  font-size: 14px;
  font-weight: 500;
  color: var(--medical-gray-700);
  background: #f8fafc;
  padding: 8px 16px;
  border-radius: 8px;
}

/* 紧急警告 */
.emergency-warning {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border: 2px solid var(--medical-red);
  border-radius: 16px;
  padding: 24px;
  margin-top: 24px;
}

.warning-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.warning-icon {
  width: 48px;
  height: 48px;
  color: var(--medical-red);
  flex-shrink: 0;
  animation: pulse 2s infinite;
}

.warning-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--medical-red);
  margin: 0 0 4px 0;
}

.warning-message {
  color: var(--medical-gray-700);
  margin: 0;
}

/* 动画 */
@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

/* 响应式优化 */
@media (max-width: 768px) {
  .symptoms-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 8px;
  }

  .symptom-button {
    padding: 10px 12px;
    font-size: 13px;
  }

  .warning-content {
    flex-direction: column;
    text-align: center;
  }

  .priority-section {
    padding: 16px;
  }
}
</style>
