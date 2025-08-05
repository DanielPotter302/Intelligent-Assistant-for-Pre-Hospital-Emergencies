<template>
  <div class="medical-card">
    <div class="medical-card-header">
      <el-icon class="medical-card-icon"><User /></el-icon>
      <h3 class="medical-card-title">患者基本信息</h3>
      <div class="ml-auto">
        <span class="status-indicator status-info"></span>
        <span class="text-sm text-gray-500">基础信息采集</span>
      </div>
    </div>

    <!-- 关键信息区域 -->
    <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
      <h4 class="text-sm font-semibold text-blue-800 mb-4 flex items-center">
        <el-icon class="mr-2 text-blue-600"><InfoFilled /></el-icon>
        患者身份信息
      </h4>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 患者姓名 -->
        <div>
          <label class="medical-label medical-label-required">
            患者姓名
            <span class="medical-label-hint">用于查询家属联系方式</span>
          </label>
          <el-input
            v-model="localPatientInfo.name"
            placeholder="请输入患者姓名"
            size="large"
            maxlength="20"
            show-word-limit
            class="w-full"
          />
        </div>

        <!-- 身份证号 -->
        <div>
          <label class="medical-label">
            身份证号
            <span class="medical-label-hint">可用于精确查询患者档案</span>
          </label>
          <el-input
            v-model="localPatientInfo.idCard"
            placeholder="请输入身份证号"
            size="large"
            maxlength="18"
            class="w-full"
          />
        </div>
      </div>
    </div>

    <!-- 基本体征信息 -->
    <div class="mb-6">
      <h4 class="text-sm font-semibold text-gray-700 mb-4 flex items-center">
        <el-icon class="mr-2 text-gray-600"><DataAnalysis /></el-icon>
        基本体征信息
      </h4>

      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <!-- 年龄 -->
        <div>
          <label class="medical-label">年龄</label>
          <el-input-number
            v-model="localPatientInfo.age"
            :min="0"
            :max="150"
            placeholder="岁"
            size="large"
            class="w-full"
            controls-position="right"
          />
        </div>

        <!-- 性别 -->
        <div>
          <label class="medical-label">性别</label>
          <el-select
            v-model="localPatientInfo.gender"
            placeholder="请选择"
            size="large"
            class="w-full"
          >
            <el-option label="男" value="male" />
            <el-option label="女" value="female" />
            <el-option label="其他" value="other" />
          </el-select>
        </div>

        <!-- 体重 -->
        <div>
          <label class="medical-label">体重 (kg)</label>
          <el-input-number
            v-model="localPatientInfo.weight"
            :min="1"
            :max="300"
            :precision="1"
            placeholder="体重"
            size="large"
            class="w-full"
            controls-position="right"
          />
        </div>

        <!-- 身高 -->
        <div>
          <label class="medical-label">身高 (cm)</label>
          <el-input-number
            v-model="localPatientInfo.height"
            :min="50"
            :max="250"
            placeholder="身高"
            size="large"
            class="w-full"
            controls-position="right"
          />
        </div>
      </div>
    </div>

    <!-- 医疗历史信息 -->
    <div class="space-y-4">
      <h4 class="text-sm font-semibold text-gray-700 mb-4 flex items-center">
        <el-icon class="mr-2 text-gray-600"><DocumentCopy /></el-icon>
        医疗历史信息
      </h4>

      <!-- 过敏史 -->
      <div>
        <label class="medical-label">
          过敏史
          <span class="medical-label-hint">重要！影响用药安全</span>
        </label>
        <el-select
          v-model="localPatientInfo.allergies"
          multiple
          filterable
          allow-create
          placeholder="选择或输入过敏物质"
          size="large"
          class="w-full"
        >
          <el-option-group label="常见药物过敏">
            <el-option label="青霉素" value="青霉素" />
            <el-option label="磺胺类" value="磺胺类" />
            <el-option label="阿司匹林" value="阿司匹林" />
          </el-option-group>
          <el-option-group label="食物过敏">
            <el-option label="海鲜" value="海鲜" />
            <el-option label="花生" value="花生" />
            <el-option label="牛奶" value="牛奶" />
            <el-option label="鸡蛋" value="鸡蛋" />
          </el-option-group>
        </el-select>
      </div>

      <!-- 当前用药 -->
      <div>
        <label class="medical-label">
          当前用药
          <span class="medical-label-hint">避免药物相互作用</span>
        </label>
        <el-select
          v-model="localPatientInfo.medications"
          multiple
          filterable
          allow-create
          placeholder="选择或输入当前用药"
          size="large"
          class="w-full"
        >
          <el-option-group label="心血管药物">
            <el-option label="降压药" value="降压药" />
            <el-option label="阿司匹林" value="阿司匹林" />
            <el-option label="华法林" value="华法林" />
          </el-option-group>
          <el-option-group label="内分泌药物">
            <el-option label="降糖药" value="降糖药" />
            <el-option label="胰岛素" value="胰岛素" />
          </el-option-group>
        </el-select>
      </div>

      <!-- 既往病史 -->
      <div>
        <label class="medical-label">
          既往病史
          <span class="medical-label-hint">影响诊断和治疗方案</span>
        </label>
        <el-select
          v-model="localPatientInfo.medicalHistory"
          multiple
          filterable
          allow-create
          placeholder="选择或输入既往病史"
          size="large"
          class="w-full"
        >
          <el-option-group label="心血管疾病">
            <el-option label="高血压" value="高血压" />
            <el-option label="冠心病" value="冠心病" />
            <el-option label="脑梗死" value="脑梗死" />
          </el-option-group>
          <el-option-group label="内分泌疾病">
            <el-option label="糖尿病" value="糖尿病" />
          </el-option-group>
          <el-option-group label="神经系统">
            <el-option label="癫痫" value="癫痫" />
          </el-option-group>
          <el-option-group label="呼吸系统">
            <el-option label="哮喘" value="哮喘" />
          </el-option-group>
          <el-option-group label="其他">
            <el-option label="肿瘤" value="肿瘤" />
            <el-option label="手术史" value="手术史" />
          </el-option-group>
        </el-select>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import { User, InfoFilled, DataAnalysis, DocumentCopy } from '@element-plus/icons-vue'
import type { PatientInfo } from '@/api/triage'

// Props 和 Emits
const props = defineProps<{
  modelValue: PatientInfo
}>()

const emit = defineEmits<{
  'update:modelValue': [value: PatientInfo]
}>()

// 本地状态
const localPatientInfo = reactive<PatientInfo>({
  ...{
    name: '',
    idCard: '',
    age: undefined,
    gender: undefined,
    weight: undefined,
    height: undefined,
    allergies: [],
    medications: [],
    medicalHistory: [],
  },
  ...props.modelValue,
})

// 监听本地变化并向上传递
watch(
  () => localPatientInfo,
  (newValue) => {
    emit('update:modelValue', { ...newValue })
  },
  { deep: true }
)

// 监听外部变化
watch(
  () => props.modelValue,
  (newValue) => {
    Object.assign(localPatientInfo, newValue)
  },
  { deep: true }
)
</script>

<style scoped>
/* 数字输入框优化 */
:deep(.el-input-number .el-input__inner) {
  text-align: center !important;
}

/* 选择器组样式 */
:deep(.el-select-group__title) {
  font-weight: 600;
  color: var(--medical-gray-600);
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* 标签样式优化 */
:deep(.el-tag) {
  margin-right: 6px;
  margin-bottom: 6px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .grid-cols-4 {
    grid-template-columns: repeat(2, 1fr);
  }

  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
}
</style>
