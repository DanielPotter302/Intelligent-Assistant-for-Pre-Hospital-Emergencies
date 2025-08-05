<template>
  <div class="vital-signs-container">
    <div class="vital-signs-header">
      <div class="flex items-center">
        <el-icon class="vital-signs-icon"><TrendCharts /></el-icon>
        <h3 class="vital-signs-title">生命体征监测</h3>
      </div>
      <div class="vital-signs-status">
        <span class="status-indicator" :class="getOverallStatus()"></span>
        <span class="text-sm text-gray-500">{{ getStatusText() }}</span>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
      <!-- 心率 -->
      <div class="vital-sign-item">
        <label class="medical-label flex items-center">
          <el-icon class="mr-2 text-red-500"><TrendCharts /></el-icon>
          心率 (bpm)
        </label>
        <div class="relative">
          <el-input-number
            v-model="localVitalSigns.heartRate"
            :min="30"
            :max="250"
            placeholder="心率"
            size="large"
            class="w-full"
            controls-position="right"
          />
          <div class="vital-status-indicator" :class="getHeartRateStatus()"></div>
        </div>
        <div class="vital-hint">
          <span class="text-xs" :class="getHeartRateTextClass()"> 正常范围: 60-100 bpm </span>
        </div>
      </div>

      <!-- 血压 -->
      <div class="vital-sign-item">
        <label class="medical-label flex items-center">
          <el-icon class="mr-2 text-blue-500"><Monitor /></el-icon>
          血压 (mmHg)
        </label>
        <div class="blood-pressure-container">
          <div class="bp-input-group">
            <el-input-number
              v-model="systolicBP"
              :min="50"
              :max="300"
              placeholder="收缩压"
              size="large"
              class="bp-input"
              controls-position="right"
            />
            <div class="vital-status-indicator" :class="getSystolicBPStatus()"></div>
          </div>
          <div class="bp-separator">/</div>
          <div class="bp-input-group">
            <el-input-number
              v-model="diastolicBP"
              :min="30"
              :max="200"
              placeholder="舒张压"
              size="large"
              class="bp-input"
              controls-position="right"
            />
            <div class="vital-status-indicator" :class="getDiastolicBPStatus()"></div>
          </div>
        </div>
        <div class="vital-hint">
          <span class="text-xs" :class="getBloodPressureTextClass()">
            正常范围: 90-140 / 60-90 mmHg
          </span>
        </div>
      </div>

      <!-- 呼吸频率 -->
      <div class="vital-sign-item">
        <label class="medical-label flex items-center">
          <el-icon class="mr-2 text-cyan-500"><Monitor /></el-icon>
          呼吸频率 (次/分)
        </label>
        <div class="relative">
          <el-input-number
            v-model="localVitalSigns.respiratoryRate"
            :min="5"
            :max="60"
            placeholder="呼吸频率"
            size="large"
            class="w-full"
            controls-position="right"
          />
          <div class="vital-status-indicator" :class="getRespiratoryRateStatus()"></div>
        </div>
        <div class="vital-hint">
          <span class="text-xs" :class="getRespiratoryRateTextClass()">
            正常范围: 12-20 次/分
          </span>
        </div>
      </div>

      <!-- 体温 -->
      <div class="vital-sign-item">
        <label class="medical-label flex items-center">
          <el-icon class="mr-2 text-orange-500"><Warning /></el-icon>
          体温 (°C)
        </label>
        <div class="relative">
          <el-input-number
            v-model="localVitalSigns.temperature"
            :min="30"
            :max="45"
            :precision="1"
            :step="0.1"
            placeholder="体温"
            size="large"
            class="w-full"
            controls-position="right"
          />
          <div class="vital-status-indicator" :class="getTemperatureStatus()"></div>
        </div>
        <div class="vital-hint">
          <span class="text-xs" :class="getTemperatureTextClass()"> 正常范围: 36.0-37.3°C </span>
        </div>
      </div>

      <!-- 血氧饱和度 -->
      <div class="vital-sign-item">
        <label class="medical-label flex items-center">
          <el-icon class="mr-2 text-green-500"><CircleCheck /></el-icon>
          血氧饱和度 (%)
        </label>
        <div class="relative">
          <el-input-number
            v-model="localVitalSigns.oxygenSaturation"
            :min="70"
            :max="100"
            placeholder="血氧"
            size="large"
            class="w-full"
            controls-position="right"
          />
          <div class="vital-status-indicator" :class="getOxygenSaturationStatus()"></div>
        </div>
        <div class="vital-hint">
          <span class="text-xs" :class="getOxygenSaturationTextClass()"> 正常范围: 95-100% </span>
        </div>
      </div>

      <!-- 血糖 -->
      <div class="vital-sign-item">
        <label class="medical-label flex items-center">
          <el-icon class="mr-2 text-purple-500"><CircleCheck /></el-icon>
          血糖 (mmol/L)
        </label>
        <div class="relative">
          <el-input-number
            v-model="localVitalSigns.glucoseLevel"
            :min="1"
            :max="30"
            :precision="1"
            :step="0.1"
            placeholder="血糖"
            size="large"
            class="w-full"
            controls-position="right"
          />
          <div class="vital-status-indicator" :class="getGlucoseLevelStatus()"></div>
        </div>
        <div class="vital-hint">
          <span class="text-xs" :class="getGlucoseLevelTextClass()">
            正常范围: 3.9-6.1 mmol/L
          </span>
        </div>
      </div>
    </div>

    <!-- 异常指标警告 -->
    <div
      v-if="vitalWarnings.length > 0"
      class="mt-6 p-4 bg-red-50 border border-red-200 rounded-lg"
    >
      <h4 class="flex items-center text-red-800 font-semibold mb-2">
        <el-icon class="mr-2"><Warning /></el-icon>
        异常生命体征警告
      </h4>
      <ul class="space-y-1">
        <li
          v-for="warning in vitalWarnings"
          :key="warning"
          class="text-red-700 text-sm flex items-center"
        >
          <span class="status-indicator status-danger mr-2"></span>
          {{ warning }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed, watch } from 'vue'
import { TrendCharts, Monitor, CircleCheck, Warning } from '@element-plus/icons-vue'
import type { VitalSigns } from '@/api/triage'

// Props 和 Emits
const props = defineProps<{
  modelValue: VitalSigns
}>()

const emit = defineEmits<{
  'update:modelValue': [value: VitalSigns]
}>()

// 本地状态
const localVitalSigns = reactive<VitalSigns>({
  ...{
    heartRate: undefined,
    bloodPressure: undefined,
    respiratoryRate: undefined,
    temperature: undefined,
    oxygenSaturation: undefined,
    glucoseLevel: undefined,
  },
  ...props.modelValue,
})

// 血压的分离处理
const systolicBP = computed({
  get: () => localVitalSigns.bloodPressure?.systolic,
  set: (value: number | undefined) => {
    if (!localVitalSigns.bloodPressure) {
      localVitalSigns.bloodPressure = { systolic: 0, diastolic: 0 }
    }
    localVitalSigns.bloodPressure.systolic = value || 0
  },
})

const diastolicBP = computed({
  get: () => localVitalSigns.bloodPressure?.diastolic,
  set: (value: number | undefined) => {
    if (!localVitalSigns.bloodPressure) {
      localVitalSigns.bloodPressure = { systolic: 0, diastolic: 0 }
    }
    localVitalSigns.bloodPressure.diastolic = value || 0
  },
})

// 生命体征状态判断
const getHeartRateStatus = () => {
  const hr = localVitalSigns.heartRate
  if (!hr) return ''
  if (hr < 60 || hr > 100) return 'vital-abnormal'
  return 'vital-normal'
}

const getSystolicBPStatus = () => {
  const sbp = systolicBP.value
  if (!sbp) return ''
  if (sbp < 90 || sbp > 140) return 'vital-abnormal'
  return 'vital-normal'
}

const getDiastolicBPStatus = () => {
  const dbp = diastolicBP.value
  if (!dbp) return ''
  if (dbp < 60 || dbp > 90) return 'vital-abnormal'
  return 'vital-normal'
}

const getRespiratoryRateStatus = () => {
  const rr = localVitalSigns.respiratoryRate
  if (!rr) return ''
  if (rr < 12 || rr > 20) return 'vital-abnormal'
  return 'vital-normal'
}

const getTemperatureStatus = () => {
  const temp = localVitalSigns.temperature
  if (!temp) return ''
  if (temp < 36.0 || temp > 37.3) return 'vital-abnormal'
  return 'vital-normal'
}

const getOxygenSaturationStatus = () => {
  const spo2 = localVitalSigns.oxygenSaturation
  if (!spo2) return ''
  if (spo2 < 95) return 'vital-abnormal'
  return 'vital-normal'
}

const getGlucoseLevelStatus = () => {
  const glucose = localVitalSigns.glucoseLevel
  if (!glucose) return ''
  if (glucose < 3.9 || glucose > 6.1) return 'vital-abnormal'
  return 'vital-normal'
}

// 文字颜色类
const getHeartRateTextClass = () =>
  getHeartRateStatus() === 'vital-abnormal' ? 'text-red-600' : 'text-gray-500'
const getBloodPressureTextClass = () =>
  getSystolicBPStatus() === 'vital-abnormal' || getDiastolicBPStatus() === 'vital-abnormal'
    ? 'text-red-600'
    : 'text-gray-500'
const getRespiratoryRateTextClass = () =>
  getRespiratoryRateStatus() === 'vital-abnormal' ? 'text-red-600' : 'text-gray-500'
const getTemperatureTextClass = () =>
  getTemperatureStatus() === 'vital-abnormal' ? 'text-red-600' : 'text-gray-500'
const getOxygenSaturationTextClass = () =>
  getOxygenSaturationStatus() === 'vital-abnormal' ? 'text-red-600' : 'text-gray-500'
const getGlucoseLevelTextClass = () =>
  getGlucoseLevelStatus() === 'vital-abnormal' ? 'text-red-600' : 'text-gray-500'

// 整体状态
const getOverallStatus = () => {
  const abnormalCount = [
    getHeartRateStatus(),
    getSystolicBPStatus(),
    getDiastolicBPStatus(),
    getRespiratoryRateStatus(),
    getTemperatureStatus(),
    getOxygenSaturationStatus(),
    getGlucoseLevelStatus(),
  ].filter((status) => status === 'vital-abnormal').length

  if (abnormalCount === 0) return 'status-normal'
  if (abnormalCount <= 2) return 'status-warning'
  return 'status-danger'
}

const getStatusText = () => {
  const status = getOverallStatus()
  if (status === 'status-normal') return '生命体征稳定'
  if (status === 'status-warning') return '需要关注'
  return '异常警告'
}

// 异常警告列表
const vitalWarnings = computed(() => {
  const warnings: string[] = []

  if (getHeartRateStatus() === 'vital-abnormal') {
    const hr = localVitalSigns.heartRate!
    if (hr < 60) warnings.push(`心率过缓: ${hr} bpm (正常: 60-100)`)
    if (hr > 100) warnings.push(`心率过速: ${hr} bpm (正常: 60-100)`)
  }

  if (getSystolicBPStatus() === 'vital-abnormal') {
    const sbp = systolicBP.value!
    if (sbp < 90) warnings.push(`收缩压过低: ${sbp} mmHg (正常: 90-140)`)
    if (sbp > 140) warnings.push(`收缩压过高: ${sbp} mmHg (正常: 90-140)`)
  }

  if (getDiastolicBPStatus() === 'vital-abnormal') {
    const dbp = diastolicBP.value!
    if (dbp < 60) warnings.push(`舒张压过低: ${dbp} mmHg (正常: 60-90)`)
    if (dbp > 90) warnings.push(`舒张压过高: ${dbp} mmHg (正常: 60-90)`)
  }

  if (getRespiratoryRateStatus() === 'vital-abnormal') {
    const rr = localVitalSigns.respiratoryRate!
    if (rr < 12) warnings.push(`呼吸过缓: ${rr} 次/分 (正常: 12-20)`)
    if (rr > 20) warnings.push(`呼吸过速: ${rr} 次/分 (正常: 12-20)`)
  }

  if (getTemperatureStatus() === 'vital-abnormal') {
    const temp = localVitalSigns.temperature!
    if (temp < 36.0) warnings.push(`体温过低: ${temp}°C (正常: 36.0-37.3)`)
    if (temp > 37.3) warnings.push(`发热: ${temp}°C (正常: 36.0-37.3)`)
  }

  if (getOxygenSaturationStatus() === 'vital-abnormal') {
    const spo2 = localVitalSigns.oxygenSaturation!
    warnings.push(`血氧饱和度低: ${spo2}% (正常: ≥95%)`)
  }

  if (getGlucoseLevelStatus() === 'vital-abnormal') {
    const glucose = localVitalSigns.glucoseLevel!
    if (glucose < 3.9) warnings.push(`血糖过低: ${glucose} mmol/L (正常: 3.9-6.1)`)
    if (glucose > 6.1) warnings.push(`血糖过高: ${glucose} mmol/L (正常: 3.9-6.1)`)
  }

  return warnings
})

// 监听本地变化并向上传递
watch(
  () => localVitalSigns,
  (newValue) => {
    emit('update:modelValue', { ...newValue })
  },
  { deep: true }
)

// 监听外部变化
watch(
  () => props.modelValue,
  (newValue) => {
    Object.assign(localVitalSigns, newValue)
  },
  { deep: true }
)
</script>

<style scoped>
.vital-sign-item {
  @apply bg-gray-50 p-4 rounded-lg border border-gray-200 transition-all duration-200;
}

.vital-sign-item:hover {
  @apply bg-white border-gray-300 shadow-sm;
}

.vital-status-indicator {
  position: absolute;
  top: 50%;
  right: 12px;
  transform: translateY(-50%);
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.vital-normal {
  background-color: var(--medical-green);
}

.vital-abnormal {
  background-color: var(--medical-red);
  animation: pulse 2s infinite;
}

.vital-hint {
  margin-top: 4px;
  text-align: center;
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

/* 血压输入容器 */
.blood-pressure-container {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
}

.bp-input-group {
  flex: 1;
  position: relative;
  min-width: 0; /* 确保flex子项能够收缩 */
}

.bp-input {
  width: 100%;
}

.bp-separator {
  font-weight: bold;
  color: var(--medical-gray-500);
  font-size: 16px;
  flex-shrink: 0;
  padding: 0 4px;
}

/* 数字输入框优化 */
:deep(.el-input-number .el-input__inner) {
  text-align: center !important;
  padding-right: 45px !important; /* 减少右边距，为控制按钮留出空间 */
}

:deep(.bp-input .el-input-number) {
  width: 100% !important;
}

:deep(.bp-input .el-input__inner) {
  padding-right: 40px !important; /* 血压输入框特殊处理 */
}

/* 响应式调整 */
@media (max-width: 1280px) {
  .xl\:grid-cols-3 {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* 生命体征容器样式 */
.vital-signs-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

.vital-signs-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 24px;
}

.vital-signs-icon {
  width: 24px;
  height: 24px;
  color: var(--medical-blue);
  margin-right: 12px;
}

.vital-signs-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--medical-gray-800);
  margin: 0;
}

.vital-signs-status {
  display: flex;
  align-items: center;
}

/* 确保最后一个元素没有多余的margin */
.vital-sign-item:last-child {
  margin-bottom: 0;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .md\:grid-cols-2 {
    grid-template-columns: 1fr;
  }

  .vital-sign-item {
    @apply p-3;
  }

  /* 移动端血压输入优化 */
  .blood-pressure-container {
    flex-direction: column;
    gap: 12px;
  }

  .bp-separator {
    order: 1;
    font-size: 18px;
  }

  .bp-input-group:first-child {
    order: 0;
  }

  .bp-input-group:last-child {
    order: 2;
  }
}
</style>
