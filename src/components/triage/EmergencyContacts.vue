<template>
  <div class="bg-white rounded-lg shadow-sm p-6">
    <h3 class="text-lg font-semibold mb-4 flex items-center">
      <el-icon class="mr-2 text-red-500"><Phone /></el-icon>
      紧急联系方式
    </h3>

    <div class="space-y-4">
      <!-- 紧急电话 -->
      <div class="bg-red-50 border border-red-200 rounded-lg p-4">
        <h4 class="font-semibold text-red-800 mb-3">紧急呼叫</h4>
        <div class="grid grid-cols-1 gap-3">
          <el-button
            v-for="contact in emergencyContacts"
            :key="contact.number"
            :type="contact.type as any"
            size="large"
            @click="makeCall(contact.number, contact.name)"
            class="w-full justify-start text-left"
          >
            <el-icon class="mr-2"><Phone /></el-icon>
            <span class="font-bold min-w-[48px] text-left">{{ contact.number }}</span>
            <span class="ml-2">{{ contact.name }}</span>
          </el-button>
        </div>
      </div>

      <!-- 医院联系方式 -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h4 class="font-semibold text-blue-800 mb-3">附近医院</h4>
        <div class="space-y-2">
          <div
            v-for="hospital in nearbyHospitals"
            :key="hospital.name"
            class="flex items-center justify-between p-2 bg-white rounded border"
          >
            <div>
              <div class="font-medium">{{ hospital.name }}</div>
              <div class="text-sm text-gray-600">
                距离: {{ hospital.distance }} | 科室: {{ hospital.departments.join(', ') }}
              </div>
            </div>
            <el-button size="small" type="primary" @click="makeCall(hospital.phone, hospital.name)">
              <el-icon class="mr-1"><Phone /></el-icon>
              拨打
            </el-button>
          </div>
        </div>
      </div>

      <!-- 家属联系查询 -->
      <div class="bg-green-50 border border-green-200 rounded-lg p-4">
        <h4 class="font-semibold text-green-800 mb-3">家属联系查询</h4>
        <div class="space-y-3">
          <!-- 快速查询方式 -->
          <div class="grid grid-cols-1 gap-2">
            <el-button
              @click="searchByIdCard"
              type="primary"
              plain
              size="large"
              class="w-full"
              :disabled="!patientInfo?.idCard?.trim()"
            >
              <el-icon class="mr-2"><CreditCard /></el-icon>
              {{
                patientInfo?.idCard?.trim()
                  ? '通过身份证查询家属'
                  : '通过身份证查询（需先输入身份证）'
              }}
              <span class="text-xs text-gray-500 ml-1">（推荐）</span>
            </el-button>

            <el-button @click="searchFromPhone" type="success" plain size="large" class="w-full">
              <el-icon class="mr-2"><Phone /></el-icon>
              从患者手机查找联系人
            </el-button>

            <el-button
              @click="searchByName"
              type="info"
              plain
              size="large"
              class="w-full"
              :disabled="!patientInfo?.name?.trim()"
            >
              <el-icon class="mr-2"><Search /></el-icon>
              {{
                patientInfo?.name?.trim()
                  ? `查询"${patientInfo.name}"的家属`
                  : '查询患者家属（需先输入姓名）'
              }}
            </el-button>
          </div>

          <!-- 查询结果显示 -->
          <div v-if="foundContacts.length > 0" class="mt-4">
            <h5 class="text-sm font-medium text-green-700 mb-2">找到的紧急联系人：</h5>
            <div class="space-y-2">
              <div
                v-for="contact in foundContacts"
                :key="contact.id"
                class="flex items-center justify-between p-2 bg-white rounded border"
              >
                <div>
                  <div class="font-medium">{{ contact.name }}</div>
                  <div class="text-sm text-gray-600">
                    {{ contact.relationship }} | {{ contact.phone }}
                  </div>
                </div>
                <div class="flex space-x-1">
                  <el-button
                    size="small"
                    type="primary"
                    @click="makeCall(contact.phone, contact.name)"
                  >
                    <el-icon><Phone /></el-icon>
                  </el-button>
                  <el-button size="small" type="success" @click="sendLocationSMS(contact)">
                    <el-icon><Message /></el-icon>
                  </el-button>
                </div>
              </div>
            </div>
          </div>

          <!-- 未找到时的应急录入 -->
          <div v-if="showManualInput" class="mt-4 pt-3 border-t border-green-200">
            <h5 class="text-sm font-medium text-green-700 mb-2">应急录入（查询无结果时）：</h5>
            <div class="space-y-2">
              <el-input v-model="emergencyContact.name" placeholder="紧急联系人姓名" size="large" />
              <el-input v-model="emergencyContact.phone" placeholder="联系电话" size="large">
                <template #append>
                  <el-button
                    @click="makeCall(emergencyContact.phone, emergencyContact.name)"
                    :disabled="!emergencyContact.phone"
                  >
                    <el-icon><Phone /></el-icon>
                  </el-button>
                </template>
              </el-input>
            </div>
          </div>
        </div>
      </div>

      <!-- 位置服务 -->
      <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
        <h4 class="font-semibold text-yellow-800 mb-3">位置服务</h4>
        <div class="space-y-3">
          <el-button
            @click="getCurrentLocation"
            type="warning"
            plain
            class="w-full"
            :loading="isGettingLocation"
          >
            <el-icon class="mr-2"><LocationInformation /></el-icon>
            {{ isGettingLocation ? '正在获取位置...' : '获取当前位置' }}
          </el-button>

          <div v-if="currentLocation" class="text-sm text-yellow-700 bg-yellow-100 p-2 rounded">
            <strong>当前位置：</strong>{{ currentLocation }}
          </div>

          <el-button
            @click="shareLocation"
            type="warning"
            plain
            class="w-full"
            :disabled="!currentLocation"
          >
            <el-icon class="mr-2"><Share /></el-icon>
            分享位置信息
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Phone,
  Message,
  LocationInformation,
  Share,
  CreditCard,
  Search,
} from '@element-plus/icons-vue'
import type { PatientInfo } from '@/api/triage'

// Props
const props = defineProps<{
  patientInfo?: PatientInfo
}>()

// 紧急联系方式
const emergencyContacts = [
  { number: '120', name: '急救中心', type: 'danger' },
  { number: '110', name: '报警电话', type: 'danger' },
  { number: '119', name: '消防电话', type: 'danger' },
  { number: '122', name: '交通事故', type: 'warning' },
]

// 附近医院（示例数据）
const nearbyHospitals = [
  {
    name: '市人民医院',
    phone: '0571-87236114',
    distance: '1.2km',
    departments: ['急诊科', '外科', '内科'],
  },
  {
    name: '市中心医院',
    phone: '0571-87236115',
    distance: '2.5km',
    departments: ['急诊科', '心内科', '神经科'],
  },
  {
    name: '市第一医院',
    phone: '0571-87236116',
    distance: '3.1km',
    departments: ['急诊科', '创伤科', '重症科'],
  },
]

// 家属紧急联系
const emergencyContact = reactive({
  name: '',
  phone: '',
})

// 位置相关
const currentLocation = ref('')
const isGettingLocation = ref(false)

// 家属联系查询相关
const foundContacts = ref<Array<{ id: string; name: string; relationship: string; phone: string }>>(
  []
)
const showManualInput = ref(false)

// 拨打电话
const makeCall = (number: string, name: string) => {
  if (!number) {
    ElMessage.warning('电话号码不能为空')
    return
  }

  // 确认对话框
  ElMessageBox.confirm(`确认拨打 ${name} 的电话：${number}？`, '确认拨打')
    .then(() => {
      // 在移动设备上直接拨打
      if (navigator.userAgent.match(/iPhone|iPad|iPod|Android/i)) {
        window.location.href = `tel:${number}`
      } else {
        // 桌面设备显示提示
        ElMessage.info(`请使用手机拨打：${number}`)
      }
    })
    .catch(() => {
      // 用户取消
    })
}

// 发送短信
const sendSMS = () => {
  if (!emergencyContact.phone) {
    ElMessage.warning('请先输入联系电话')
    return
  }

  const message = `紧急情况！患者${emergencyContact.name || '姓名未知'}需要医疗救助。位置：${
    currentLocation.value || '位置未知'
  }。请立即联系或前往现场。`

  if (navigator.userAgent.match(/iPhone|iPad|iPod|Android/i)) {
    window.location.href = `sms:${emergencyContact.phone}?body=${encodeURIComponent(message)}`
  } else {
    // 复制到剪贴板
    navigator.clipboard.writeText(`${emergencyContact.phone}: ${message}`).then(() => {
      ElMessage.success('短信内容已复制到剪贴板')
    })
  }
}

// 获取当前位置
const getCurrentLocation = () => {
  if (!navigator.geolocation) {
    ElMessage.error('浏览器不支持地理位置服务')
    return
  }

  isGettingLocation.value = true

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords
      // 这里可以调用地理编码API获取地址
      currentLocation.value = `纬度: ${latitude.toFixed(6)}, 经度: ${longitude.toFixed(6)}`
      isGettingLocation.value = false
      ElMessage.success('位置获取成功')
    },
    (error) => {
      isGettingLocation.value = false
      ElMessage.error('位置获取失败：' + error.message)
    },
    {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 300000,
    }
  )
}

// 分享位置
const shareLocation = () => {
  if (!currentLocation.value) {
    ElMessage.warning('请先获取当前位置')
    return
  }

  const shareText = `紧急医疗位置信息：${currentLocation.value}`

  if (navigator.share) {
    navigator.share({
      title: '紧急医疗位置',
      text: shareText,
    })
  } else {
    navigator.clipboard.writeText(shareText).then(() => {
      ElMessage.success('位置信息已复制到剪贴板')
    })
  }
}

// 通过身份证查询家属
const searchByIdCard = () => {
  const idCard = props.patientInfo?.idCard?.trim()

  if (!idCard) {
    ElMessage.warning('请先在患者基本信息中输入身份证号')
    return
  }

  ElMessage.info(`正在通过身份证查询患者档案...`)
  // 模拟查询结果
  setTimeout(() => {
    foundContacts.value = [
      { id: '1', name: '张丽华', relationship: '配偶', phone: '138****1234' },
      { id: '2', name: '李小明', relationship: '子女', phone: '139****5678' },
      { id: '3', name: '张大爷', relationship: '父亲', phone: '137****9999' },
    ]
    showManualInput.value = foundContacts.value.length === 0

    if (foundContacts.value.length > 0) {
      ElMessage.success(`通过身份证找到${foundContacts.value.length}位紧急联系人`)
    } else {
      ElMessage.warning('未找到该身份证对应的患者档案')
    }
  }, 1000)
}

// 从患者手机查找联系人
const searchFromPhone = () => {
  ElMessage.info('手机通讯录读取功能开发中，需要设备权限')
  // 模拟手机通讯录搜索
  setTimeout(() => {
    foundContacts.value = [{ id: '3', name: '王五', relationship: '家人', phone: '137****9012' }]
    showManualInput.value = foundContacts.value.length === 0
  }, 800)
}

// 按姓名查询患者信息
const searchByName = () => {
  const patientName = props.patientInfo?.name?.trim()

  if (!patientName) {
    ElMessage.warning('请先在患者基本信息中输入患者姓名')
    return
  }

  ElMessage.info(`正在查询患者"${patientName}"的家属信息...`)
  // 模拟查询过程
  setTimeout(() => {
    // 模拟基于患者姓名的查询结果
    foundContacts.value = [
      { id: '4', name: '王芳', relationship: '配偶', phone: '136****3456' },
      { id: '5', name: '李明', relationship: '子女', phone: '137****7890' },
    ]
    showManualInput.value = foundContacts.value.length === 0

    if (foundContacts.value.length > 0) {
      ElMessage.success(`找到患者"${patientName}"的${foundContacts.value.length}位紧急联系人`)
    } else {
      ElMessage.warning(`未找到患者"${patientName}"的家属信息，请使用应急录入`)
    }
  }, 1200)
}

// 发送位置短信给家属
const sendLocationSMS = (contact: any) => {
  const message = `紧急情况！患者需要医疗救助。位置：${
    currentLocation.value || '位置未知'
  }。请立即联系或前往现场。`

  if (navigator.userAgent.match(/iPhone|iPad|iPod|Android/i)) {
    window.location.href = `sms:${contact.phone}?body=${encodeURIComponent(message)}`
  } else {
    navigator.clipboard.writeText(`${contact.phone}: ${message}`).then(() => {
      ElMessage.success('短信内容已复制到剪贴板')
    })
  }
}
</script>

<style scoped>
/* 紧急联系按钮动画 */
.el-button--danger {
  animation: emergencyPulse 2s infinite;
}

@keyframes emergencyPulse {
  0% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0.7);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(245, 108, 108, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0);
  }
}

/* 按钮对齐优化 */
:deep(.el-button) {
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  text-align: left !important;
  min-height: 44px !important;
}

:deep(.el-button--large) {
  padding: 12px 16px !important;
  font-size: 14px !important;
}

/* 紧急按钮内容对齐 */
.justify-start {
  justify-content: flex-start !important;
}

/* 号码对齐 */
.min-w-[48px] {
  min-width: 48px;
  display: inline-block;
  text-align: left;
}

/* 查询按钮优化 */
:deep(.el-button.is-disabled) {
  opacity: 0.6 !important;
  cursor: not-allowed !important;
}

:deep(.el-button.is-disabled .text-xs) {
  color: #9ca3af !important;
}
</style>
