<template>
  <div class="triage-wizard">
    <!-- 步骤指示器 -->
    <div class="wizard-header">
      <el-steps :active="currentStep" finish-status="success" align-center>
        <el-step title="基本信息" description="患者身份与体征" />
        <el-step title="症状评估" description="主诉与症状描述" />
        <el-step title="生命体征" description="关键医疗指标" />
        <el-step title="智能分诊" description="AI分析与建议" />
      </el-steps>
    </div>

    <!-- 步骤内容 -->
    <div class="wizard-content">
      <transition name="fade-slide" mode="out-in">
        <!-- 步骤1: 基本信息 -->
        <div v-if="currentStep === 0" key="step1" class="step-content">
          <div class="step-header">
            <el-icon class="step-icon"><User /></el-icon>
            <div>
              <h2 class="step-title">患者基本信息</h2>
              <p class="step-description">首先告诉我们一些基本的患者信息</p>
            </div>
          </div>

          <div class="step-form">
            <!-- 关键信息卡片 -->
            <div class="info-card highlighted">
              <h3 class="card-title">必填信息</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="form-group">
                  <label class="form-label required">患者姓名</label>
                  <el-input
                    v-model="formData.patientInfo.name"
                    placeholder="请输入患者姓名"
                    size="large"
                    maxlength="20"
                    class="w-full"
                    @input="validateStep1"
                  />
                </div>
                <div class="form-group">
                  <label class="form-label required">年龄</label>
                  <el-input-number
                    v-model="formData.patientInfo.age"
                    :min="0"
                    :max="150"
                    placeholder="岁"
                    size="large"
                    class="w-full"
                    @change="validateStep1"
                  />
                </div>
                <div class="form-group">
                  <label class="form-label required">性别</label>
                  <el-select
                    v-model="formData.patientInfo.gender"
                    placeholder="请选择性别"
                    size="large"
                    class="w-full"
                    @change="validateStep1"
                  >
                    <el-option label="男" value="male" />
                    <el-option label="女" value="female" />
                    <el-option label="其他" value="other" />
                  </el-select>
                </div>
                <div class="form-group">
                  <label class="form-label">身份证号</label>
                  <el-input
                    v-model="formData.patientInfo.idCard"
                    placeholder="可用于查询患者档案"
                    size="large"
                    maxlength="18"
                    class="w-full"
                  />
                </div>
              </div>
            </div>

            <!-- 可选信息卡片 -->
            <div class="info-card">
              <h3 class="card-title">可选信息</h3>
              <el-collapse v-model="activeCollapse">
                <el-collapse-item title="体格信息" name="physical">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="form-group">
                      <label class="form-label">体重 (kg)</label>
                      <el-input-number
                        v-model="formData.patientInfo.weight"
                        :min="1"
                        :max="300"
                        :precision="1"
                        placeholder="体重"
                        size="large"
                        class="w-full"
                      />
                    </div>
                    <div class="form-group">
                      <label class="form-label">身高 (cm)</label>
                      <el-input-number
                        v-model="formData.patientInfo.height"
                        :min="50"
                        :max="250"
                        placeholder="身高"
                        size="large"
                        class="w-full"
                      />
                    </div>
                  </div>
                </el-collapse-item>

                <el-collapse-item title="医疗史信息" name="medical">
                  <div class="space-y-4">
                    <div class="form-group">
                      <label class="form-label">过敏史</label>
                      <el-select
                        v-model="formData.patientInfo.allergies"
                        multiple
                        filterable
                        allow-create
                        placeholder="选择或输入过敏物质"
                        size="large"
                        class="w-full"
                      >
                        <el-option label="青霉素" value="青霉素" />
                        <el-option label="磺胺类" value="磺胺类" />
                        <el-option label="海鲜" value="海鲜" />
                        <el-option label="花生" value="花生" />
                      </el-select>
                    </div>
                    <div class="form-group">
                      <label class="form-label">既往病史</label>
                      <el-select
                        v-model="formData.patientInfo.medicalHistory"
                        multiple
                        filterable
                        allow-create
                        placeholder="选择或输入既往病史"
                        size="large"
                        class="w-full"
                      >
                        <el-option label="高血压" value="高血压" />
                        <el-option label="糖尿病" value="糖尿病" />
                        <el-option label="心脏病" value="心脏病" />
                        <el-option label="哮喘" value="哮喘" />
                      </el-select>
                    </div>
                  </div>
                </el-collapse-item>
              </el-collapse>
            </div>
          </div>
        </div>

        <!-- 步骤2: 症状评估 -->
        <div v-else-if="currentStep === 1" key="step2" class="step-content">
          <div class="step-header">
            <el-icon class="step-icon"><Warning /></el-icon>
            <div>
              <h2 class="step-title">症状评估</h2>
              <p class="step-description">详细描述患者的症状和主诉</p>
            </div>
          </div>

          <div class="step-form">
            <div class="info-card highlighted">
              <h3 class="card-title">主要症状</h3>
              <div class="space-y-6">
                <div class="form-group">
                  <label class="form-label required">患者主诉</label>
                  <el-input
                    v-model="formData.symptomInfo.chiefComplaint"
                    type="textarea"
                    :rows="3"
                    placeholder="请详细描述患者的主要症状和不适..."
                    maxlength="200"
                    show-word-limit
                    @input="validateStep2"
                  />
                </div>

                <div class="form-group">
                  <label class="form-label required">选择症状</label>
                  <div class="symptom-grid">
                    <el-checkbox-group
                      v-model="formData.symptomInfo.symptoms"
                      @change="validateStep2"
                    >
                      <el-checkbox
                        v-for="symptom in commonSymptoms"
                        :key="symptom"
                        :value="symptom"
                        class="symptom-checkbox"
                      >
                        {{ symptom }}
                      </el-checkbox>
                    </el-checkbox-group>
                  </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div class="form-group">
                    <label class="form-label">疼痛程度 (0-10分)</label>
                    <el-slider
                      v-model="formData.symptomInfo.painLevel"
                      :max="10"
                      show-tooltip
                      :format-tooltip="formatPainLevel"
                      class="pain-slider"
                    />
                  </div>
                  <div class="form-group">
                    <label class="form-label">持续时间</label>
                    <el-select
                      v-model="formData.symptomInfo.duration"
                      placeholder="选择症状持续时间"
                      size="large"
                      class="w-full"
                    >
                      <el-option label="不到5分钟" value="<5分钟" />
                      <el-option label="5-30分钟" value="5-30分钟" />
                      <el-option label="30分钟-1小时" value="30分钟-1小时" />
                      <el-option label="1-6小时" value="1-6小时" />
                      <el-option label="6-24小时" value="6-24小时" />
                      <el-option label="超过1天" value=">1天" />
                    </el-select>
                  </div>
                </div>
              </div>
            </div>

            <div class="info-card">
              <h3 class="card-title">补充信息</h3>
              <div class="space-y-4">
                <div class="form-group">
                  <label class="form-label">受伤机制</label>
                  <el-input
                    v-model="formData.symptomInfo.mechanism"
                    placeholder="如：车祸、跌倒、运动伤等"
                    size="large"
                  />
                </div>
                <div class="form-group">
                  <label class="form-label">其他症状描述</label>
                  <el-input
                    v-model="formData.symptomInfo.additionalInfo"
                    type="textarea"
                    :rows="2"
                    placeholder="补充说明其他相关症状..."
                    maxlength="300"
                    show-word-limit
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 步骤3: 生命体征 -->
        <div v-else-if="currentStep === 2" key="step3" class="step-content">
          <div class="step-header">
            <el-icon class="step-icon"><TrendCharts /></el-icon>
            <div>
              <h2 class="step-title">生命体征</h2>
              <p class="step-description">测量并记录关键的生命体征指标</p>
            </div>
          </div>

          <div class="step-form">
            <VitalSignsForm v-model="formData.vitalSigns" />
          </div>
        </div>

        <!-- 步骤4: 智能分诊 -->
        <div v-else-if="currentStep === 3" key="step4" class="step-content">
          <div class="step-header">
            <el-icon class="step-icon"><Cpu /></el-icon>
            <div>
              <h2 class="step-title">智能分诊</h2>
              <p class="step-description">AI将分析所有信息并提供专业建议</p>
            </div>
          </div>

          <div class="step-form">
            <!-- 分诊结果展示 -->
            <div v-if="triageResult" class="mb-6">
              <TriageResultCard
                :result="triageResult"
                :analysis="analysisResult"
                @call-emergency="$emit('call-emergency')"
              />
            </div>

            <!-- 分诊控制面板 -->
            <div class="info-card highlighted text-center">
              <div class="space-y-6">
                <div class="ai-icon-wrapper">
                  <div class="ai-icon">
                    <el-icon><Cpu /></el-icon>
                  </div>
                  <h3 class="ai-title">AI智能分诊系统</h3>
                  <p class="ai-description">{{ getAIDescription() }}</p>
                </div>

                <el-button
                  @click="performTriage"
                  :type="triageResult ? 'warning' : 'primary'"
                  size="large"
                  :loading="isAnalyzing"
                  :disabled="!canPerformTriage"
                  class="triage-button"
                >
                  <el-icon class="mr-3"><Cpu /></el-icon>
                  {{ getTriageButtonText() }}
                </el-button>

                <div v-if="!canPerformTriage" class="validation-message">
                  <el-icon class="mr-2"><Warning /></el-icon>
                  请确保已填写患者基本信息和症状描述
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- 步骤导航 -->
    <div class="wizard-footer">
      <div class="flex justify-between items-center">
        <el-button v-if="currentStep > 0" @click="prevStep" size="large" icon="ArrowLeft">
          上一步
        </el-button>
        <div v-else></div>

        <div class="flex items-center space-x-6">
          <span class="step-counter">{{ currentStep + 1 }} / 4</span>

          <el-button
            v-if="currentStep < 3"
            @click="nextStep"
            type="primary"
            size="large"
            :disabled="!canProceedToNext"
          >
            下一步
            <el-icon class="ml-2"><ArrowRight /></el-icon>
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Warning, TrendCharts, Cpu, ArrowLeft, ArrowRight } from '@element-plus/icons-vue'

// 组件导入
import VitalSignsForm from './VitalSignsForm.vue'
import TriageResultCard from './TriageResultCard.vue'

// 类型导入
import type { PatientInfo, VitalSigns, SymptomInfo, AITriageResponse } from '@/api/triage'
import type { TriageResult, BackendTriageRequest } from '@/types/api'
import { analyzeTriageData } from '@/api/triage'

// Props 和 Emits
const emit = defineEmits<{
  'call-emergency': []
  'analysis-started': []
  'analysis-completed': []
}>()

// 响应式数据
const currentStep = ref(0)
const activeCollapse = ref(['physical', 'medical'])
const isAnalyzing = ref(false)
const triageResult = ref<TriageResult | null>(null)
const analysisResult = ref<any>(null)

// 表单数据
const formData = reactive({
  patientInfo: {
    name: '',
    idCard: '',
    age: 0,
    gender: 'other' as 'male' | 'female' | 'other',
    weight: undefined,
    height: undefined,
    allergies: [],
    medications: [],
    medicalHistory: [],
  } as PatientInfo,

  vitalSigns: {
    heartRate: 0,
    bloodPressure: {
      systolic: 0,
      diastolic: 0,
    },
    respiratoryRate: 0,
    temperature: 0,
    oxygenSaturation: undefined,
    glucoseLevel: undefined,
  } as VitalSigns,

  symptomInfo: {
    chiefComplaint: '',
    symptoms: [],
    painLevel: undefined,
    duration: '',
    mechanism: '',
    additionalInfo: '',
  } as SymptomInfo,
})

// 常见症状列表
const commonSymptoms = [
  '胸痛',
  '呼吸困难',
  '头痛',
  '腹痛',
  '发热',
  '恶心呕吐',
  '头晕',
  '出汗',
  '心悸',
  '乏力',
  '意识障碍',
  '抽搐',
  '出血',
  '骨折',
  '烧伤',
]

// 验证函数
const step1Valid = ref(false)
const step2Valid = ref(false)

const validateStep1 = () => {
  step1Valid.value = !!(
    formData.patientInfo.name?.trim() &&
    formData.patientInfo.age &&
    formData.patientInfo.gender
  )
}

const validateStep2 = () => {
  step2Valid.value = !!(
    formData.symptomInfo.chiefComplaint?.trim() && formData.symptomInfo.symptoms.length > 0
  )
}

// 计算属性
const canProceedToNext = computed(() => {
  switch (currentStep.value) {
    case 0:
      return step1Valid.value
    case 1:
      return step2Valid.value
    case 2:
      return true // 生命体征可选
    default:
      return false
  }
})

const canPerformTriage = computed(() => {
  return step1Valid.value && step2Valid.value
})

// 步骤导航
const nextStep = () => {
  if (canProceedToNext.value && currentStep.value < 3) {
    currentStep.value++
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

// 分诊处理
const performTriage = async () => {
  if (!canPerformTriage.value) {
    ElMessage.warning('请先填写完整的患者信息')
    return
  }

  isAnalyzing.value = true
  emit('analysis-started')

  try {
    const triageInput: BackendTriageRequest = {
      patient_info: {
        name: formData.patientInfo.name,
        id_card: formData.patientInfo.idCard,
        age: formData.patientInfo.age,
        gender: formData.patientInfo.gender,
        weight: formData.patientInfo.weight,
        height: formData.patientInfo.height,
        allergies: formData.patientInfo.allergies,
        medications: formData.patientInfo.medications,
        medical_history: formData.patientInfo.medicalHistory,
      },
      vital_signs: {
        heart_rate: formData.vitalSigns.heartRate,
        blood_pressure_systolic: formData.vitalSigns.bloodPressure.systolic,
        blood_pressure_diastolic: formData.vitalSigns.bloodPressure.diastolic,
        respiratory_rate: formData.vitalSigns.respiratoryRate,
        temperature: formData.vitalSigns.temperature,
        oxygen_saturation: formData.vitalSigns.oxygenSaturation,
        blood_glucose: formData.vitalSigns.glucoseLevel,
      },
      symptom_info: {
        chief_complaint: formData.symptomInfo.chiefComplaint,
        symptoms: formData.symptomInfo.symptoms,
        pain_level: formData.symptomInfo.painLevel,
        symptom_duration: formData.symptomInfo.duration,
      },
    }

    const response = await analyzeTriageData(triageInput)
    const result = response.data

    // 后端返回的数据结构：{record_id, analysis}
    const analysis = result.analysis as any
    analysisResult.value = analysis

    // 构建前端需要的triageResult格式
    triageResult.value = {
      level:
        analysis.urgency_level === 'critical'
          ? 'red'
          : analysis.urgency_level === 'urgent'
            ? 'orange'
            : analysis.urgency_level === 'semi_urgent'
              ? 'yellow'
              : 'green',
      levelDescription: analysis.urgency_level,
      severity: analysis.urgency_level,
      recommendations: analysis.recommended_actions || [],
      immediateActions: analysis.recommended_actions || [],
      calculatedScores: [],
      referenceGuidelines: [],
      callEmergency: analysis.urgency_level === 'critical',
      estimatedWaitTime: analysis.estimated_wait_time || '待定',
    }

    ElMessage.success('AI分诊分析完成')

    if (triageResult.value.callEmergency) {
      emit('call-emergency')
    }
  } catch (error: any) {
    console.error('分诊分析失败:', error)

    // 根据错误类型提供不同的提示
    if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
      ElMessage.error('AI分析超时，请稍后重试。LLM服务可能正在处理中...')
    } else if (error.response?.status === 422) {
      ElMessage.error('数据格式错误，请检查输入信息')
    } else if (error.response?.status === 401) {
      ElMessage.error('登录已过期，请重新登录')
    } else {
      ElMessage.error(error.message || '分析过程中出现错误，请重试')
    }
  } finally {
    isAnalyzing.value = false
    emit('analysis-completed')
  }
}

// 辅助函数
const formatPainLevel = (value: number) => {
  const levels = [
    '无痛',
    '轻微',
    '轻度',
    '中度',
    '中重度',
    '重度',
    '严重',
    '很严重',
    '极严重',
    '剧烈',
    '无法忍受',
  ]
  return `${value}分 - ${levels[value] || '未知'}`
}

const getTriageButtonText = () => {
  if (isAnalyzing.value) {
    return 'AI正在深度分析中，请稍候...'
  }
  if (triageResult.value) {
    return '重新进行分诊分析'
  }
  return '开始智能分诊'
}

const getAIDescription = () => {
  if (isAnalyzing.value) {
    return 'DeepSeek AI正在分析患者信息，请耐心等待...'
  }
  if (triageResult.value) {
    return '可以基于新的信息重新进行分析评估'
  }
  return '基于国际分诊标准和DeepSeek AI的智能评估'
}

// 监听表单变化
watch(() => formData.patientInfo, validateStep1, { deep: true })
watch(() => formData.symptomInfo, validateStep2, { deep: true })
</script>

<style scoped>
.triage-wizard {
  max-width: 900px;
  margin: 0 auto;
}

.wizard-header {
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 24px;
}

.wizard-content {
  min-height: 600px;
}

.step-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.step-header {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  padding: 32px;
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e2e8f0;
}

.step-icon {
  width: 60px;
  height: 60px;
  background: var(--el-color-primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
  margin-right: 20px;
  flex-shrink: 0;
}

.step-title {
  font-size: 24px;
  font-weight: 600;
  color: var(--medical-gray-800);
  margin: 0 0 4px 0;
}

.step-description {
  color: var(--medical-gray-600);
  margin: 0;
  font-size: 16px;
}

.step-form {
  padding: 32px;
  space-y: 24px;
}

.info-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
}

.info-card.highlighted {
  background: linear-gradient(135deg, #dbeafe 0%, #e0f2fe 100%);
  border-color: #60a5fa;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: var(--medical-gray-800);
  margin: 0 0 20px 0;
  display: flex;
  align-items: center;
}

.card-title::before {
  content: '';
  width: 4px;
  height: 20px;
  background: var(--el-color-primary);
  margin-right: 12px;
  border-radius: 2px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--medical-gray-700);
  margin-bottom: 8px;
}

.form-label.required::before {
  content: '*';
  color: var(--medical-red);
  margin-right: 4px;
  font-weight: bold;
}

.symptom-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.symptom-checkbox {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 12px 16px;
  transition: all 0.2s ease;
}

.symptom-checkbox:hover {
  border-color: var(--el-color-primary);
  background: #f0f9ff;
}

.pain-slider {
  margin: 20px 0;
}

.ai-icon-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.ai-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(
    135deg,
    var(--el-color-primary) 0%,
    var(--el-color-primary-dark-2) 100%
  );
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 32px;
  margin-bottom: 16px;
  box-shadow: 0 8px 32px rgba(37, 99, 235, 0.3);
}

.ai-title {
  font-size: 20px;
  font-weight: 600;
  color: var(--medical-gray-800);
  margin: 0 0 8px 0;
}

.ai-description {
  color: var(--medical-gray-600);
  margin: 0 0 24px 0;
}

.triage-button {
  width: 100%;
  max-width: 300px;
  height: 56px;
  font-size: 16px;
  font-weight: 600;
  background: linear-gradient(
    135deg,
    var(--el-color-primary) 0%,
    var(--el-color-primary-dark-2) 100%
  );
  border: none;
  box-shadow: 0 4px 20px rgba(37, 99, 235, 0.3);
}

.triage-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 32px rgba(37, 99, 235, 0.4);
}

.validation-message {
  color: var(--medical-orange);
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.wizard-footer {
  background: white;
  padding: 24px;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  margin-top: 24px;
}

.step-counter {
  font-size: 14px;
  color: var(--medical-gray-600);
  font-weight: 500;
  background: var(--medical-gray-100);
  padding: 8px 16px;
  border-radius: 20px;
  min-width: 60px;
  text-align: center;
  margin-right: 8px;
}

/* 动画效果 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* 响应式优化 */
@media (max-width: 768px) {
  .step-header {
    padding: 24px 20px;
    flex-direction: column;
    text-align: center;
  }

  .step-icon {
    margin-right: 0;
    margin-bottom: 16px;
  }

  .step-form {
    padding: 24px 20px;
  }

  .symptom-grid {
    grid-template-columns: 1fr;
  }

  .wizard-footer {
    padding: 20px;
  }

  .wizard-footer .flex {
    flex-direction: column;
    gap: 16px;
  }

  .wizard-footer .flex:first-child {
    order: 2;
  }

  .wizard-footer .flex:last-child {
    order: 1;
    justify-content: center;
  }

  .step-counter {
    margin-right: 0;
    margin-bottom: 8px;
  }
}
</style>
