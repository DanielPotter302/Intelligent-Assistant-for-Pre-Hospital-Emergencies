<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-semibold mb-4 flex items-center">
      <el-icon class="mr-2 text-purple-500"><DataAnalysis /></el-icon>
      医学计算器
    </h3>

    <el-collapse v-model="activeCalculators" accordion>
      <!-- Glasgow昏迷评分 -->
      <el-collapse-item title="Glasgow昏迷评分 (GCS)" name="gcs">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2">睁眼反应</label>
            <el-select v-model="gcsData.eyeResponse" class="w-full">
              <el-option label="4分 - 自主睁眼" :value="4" />
              <el-option label="3分 - 语言刺激睁眼" :value="3" />
              <el-option label="2分 - 疼痛刺激睁眼" :value="2" />
              <el-option label="1分 - 无反应" :value="1" />
            </el-select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">语言反应</label>
            <el-select v-model="gcsData.verbalResponse" class="w-full">
              <el-option label="5分 - 回答正确" :value="5" />
              <el-option label="4分 - 回答错乱" :value="4" />
              <el-option label="3分 - 言语错乱" :value="3" />
              <el-option label="2分 - 呻吟" :value="2" />
              <el-option label="1分 - 无反应" :value="1" />
            </el-select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">运动反应</label>
            <el-select v-model="gcsData.motorResponse" class="w-full">
              <el-option label="6分 - 遵嘱运动" :value="6" />
              <el-option label="5分 - 定位疼痛" :value="5" />
              <el-option label="4分 - 逃避疼痛" :value="4" />
              <el-option label="3分 - 异常屈曲" :value="3" />
              <el-option label="2分 - 异常伸展" :value="2" />
              <el-option label="1分 - 无反应" :value="1" />
            </el-select>
          </div>

          <div v-if="gcsResult" class="bg-blue-50 p-4 rounded-lg">
            <div class="text-lg font-semibold mb-2">GCS评分：{{ gcsResult.total }}/15</div>
            <div class="text-sm text-blue-700">
              {{ gcsResult.interpretation }}
            </div>
          </div>
        </div>
      </el-collapse-item>

      <!-- HEART评分 -->
      <el-collapse-item title="HEART评分 (胸痛)" name="heart">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2">病史 (0-2分)</label>
            <el-select v-model="heartData.history" class="w-full">
              <el-option label="0分 - 低危病史" :value="0" />
              <el-option label="1分 - 中危病史" :value="1" />
              <el-option label="2分 - 高危病史" :value="2" />
            </el-select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">心电图 (0-2分)</label>
            <el-select v-model="heartData.ecg" class="w-full">
              <el-option label="0分 - 正常" :value="0" />
              <el-option label="1分 - 非特异性改变" :value="1" />
              <el-option label="2分 - 显著异常" :value="2" />
            </el-select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">年龄 (0-2分)</label>
            <el-select v-model="heartData.age" class="w-full">
              <el-option label="0分 - <45岁" :value="0" />
              <el-option label="1分 - 45-64岁" :value="1" />
              <el-option label="2分 - ≥65岁" :value="2" />
            </el-select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">危险因素 (0-2分)</label>
            <el-select v-model="heartData.riskFactors" class="w-full">
              <el-option label="0分 - 无危险因素" :value="0" />
              <el-option label="1分 - 1-2个危险因素" :value="1" />
              <el-option label="2分 - ≥3个危险因素" :value="2" />
            </el-select>
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">肌钙蛋白 (0-2分)</label>
            <el-select v-model="heartData.troponin" class="w-full">
              <el-option label="0分 - 正常" :value="0" />
              <el-option label="1分 - 1-3倍正常上限" :value="1" />
              <el-option label="2分 - >3倍正常上限" :value="2" />
            </el-select>
          </div>

          <div v-if="heartResult" class="p-4 rounded-lg" :class="getHeartResultClass()">
            <div class="text-lg font-semibold mb-2">HEART评分：{{ heartResult.total }}/10</div>
            <div class="text-sm mb-1"><strong>风险等级：</strong>{{ heartResult.riskLevel }}</div>
            <div class="text-sm">
              {{ heartResult.interpretation }}
            </div>
          </div>
        </div>
      </el-collapse-item>

      <!-- 修正创伤评分 -->
      <el-collapse-item title="修正创伤评分 (RTS)" name="rts">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2">收缩压 (mmHg)</label>
            <el-input-number v-model="rtsData.systolicBP" :min="0" :max="300" class="w-full" />
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">呼吸频率 (次/分)</label>
            <el-input-number v-model="rtsData.respiratoryRate" :min="0" :max="60" class="w-full" />
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">GCS评分</label>
            <el-input-number v-model="rtsData.gcsScore" :min="3" :max="15" class="w-full" />
          </div>

          <div v-if="rtsResult" class="bg-orange-50 p-4 rounded-lg">
            <div class="text-lg font-semibold mb-2">RTS评分：{{ rtsResult.total }}</div>
            <div class="text-sm text-orange-700">
              {{ rtsResult.interpretation }}
            </div>
          </div>
        </div>
      </el-collapse-item>

      <!-- 儿童药物剂量计算 -->
      <el-collapse-item title="儿童药物剂量计算" name="pediatric">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2">体重 (kg)</label>
            <el-input-number
              v-model="pediatricData.weight"
              :min="1"
              :max="100"
              :precision="1"
              class="w-full"
            />
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">每公斤剂量 (mg/kg)</label>
            <el-input-number
              v-model="pediatricData.dosePerKg"
              :min="0"
              :precision="2"
              :step="0.1"
              class="w-full"
            />
          </div>

          <div v-if="pediatricResult" class="bg-green-50 p-4 rounded-lg">
            <div class="text-lg font-semibold mb-2">建议剂量：{{ pediatricResult }} mg</div>
            <div class="text-sm text-green-700">请根据具体药物说明书和临床指南确认</div>
          </div>
        </div>
      </el-collapse-item>

      <!-- 体表面积计算 -->
      <el-collapse-item title="体表面积计算 (BSA)" name="bsa">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-2">体重 (kg)</label>
            <el-input-number
              v-model="bsaData.weight"
              :min="1"
              :max="300"
              :precision="1"
              class="w-full"
            />
          </div>

          <div>
            <label class="block text-sm font-medium mb-2">身高 (cm)</label>
            <el-input-number v-model="bsaData.height" :min="50" :max="250" class="w-full" />
          </div>

          <div v-if="bsaResult" class="bg-purple-50 p-4 rounded-lg">
            <div class="text-lg font-semibold mb-2">体表面积：{{ bsaResult }} m²</div>
            <div class="text-sm text-purple-700">用于计算化疗药物剂量等</div>
          </div>
        </div>
      </el-collapse-item>
    </el-collapse>

    <!-- 快速计算按钮 -->
    <div class="mt-6">
      <el-button @click="calculateAll" type="primary" class="w-full">
        <el-icon class="mr-2"><Refresh /></el-icon>
        重新计算全部
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { DataAnalysis, Refresh } from '@element-plus/icons-vue'
import { MedicalCalculators } from '@/api/triage'

// 激活的计算器
const activeCalculators = ref<string>('')

// GCS数据
const gcsData = ref({
  eyeResponse: 4,
  verbalResponse: 5,
  motorResponse: 6,
})

// HEART评分数据
const heartData = ref({
  history: 0,
  ecg: 0,
  age: 0,
  riskFactors: 0,
  troponin: 0,
})

// RTS数据
const rtsData = ref({
  systolicBP: 120,
  respiratoryRate: 16,
  gcsScore: 15,
})

// 儿童药物剂量数据
const pediatricData = ref({
  weight: 20,
  dosePerKg: 10,
})

// BSA数据
const bsaData = ref({
  weight: 70,
  height: 170,
})

// 计算结果
const gcsResult = computed(() => {
  if (gcsData.value.eyeResponse && gcsData.value.verbalResponse && gcsData.value.motorResponse) {
    return MedicalCalculators.calculateGCS(
      gcsData.value.eyeResponse,
      gcsData.value.verbalResponse,
      gcsData.value.motorResponse
    )
  }
  return null
})

const heartResult = computed(() => {
  return MedicalCalculators.calculateHeartScore(
    heartData.value.history,
    heartData.value.ecg,
    heartData.value.age,
    heartData.value.riskFactors,
    heartData.value.troponin
  )
})

const rtsResult = computed(() => {
  if (rtsData.value.systolicBP && rtsData.value.respiratoryRate && rtsData.value.gcsScore) {
    return MedicalCalculators.calculateRTS(
      rtsData.value.systolicBP,
      rtsData.value.respiratoryRate,
      rtsData.value.gcsScore
    )
  }
  return null
})

const pediatricResult = computed(() => {
  if (pediatricData.value.weight && pediatricData.value.dosePerKg) {
    return MedicalCalculators.calculatePediatricDose(
      pediatricData.value.weight,
      pediatricData.value.dosePerKg
    )
  }
  return null
})

const bsaResult = computed(() => {
  if (bsaData.value.weight && bsaData.value.height) {
    return MedicalCalculators.calculateBSA(bsaData.value.weight, bsaData.value.height).toFixed(2)
  }
  return null
})

// 获取HEART评分结果样式
const getHeartResultClass = () => {
  if (!heartResult.value) return 'bg-gray-50'

  if (heartResult.value.total <= 3) return 'bg-green-50'
  if (heartResult.value.total <= 6) return 'bg-yellow-50'
  return 'bg-red-50'
}

// 重新计算全部
const calculateAll = () => {
  // 强制重新计算（通过触发响应式更新）
  const temp = { ...gcsData.value }
  gcsData.value = { ...temp }
}
</script>

<style scoped>
:deep(.el-collapse-item__header) {
  font-weight: 600;
  color: #374151;
}

:deep(.el-collapse-item__content) {
  padding-bottom: 0;
}
</style>
