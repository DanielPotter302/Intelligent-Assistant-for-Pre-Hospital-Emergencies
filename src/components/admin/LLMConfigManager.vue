<template>
  <el-dialog
    v-model="visible"
    title="LLM配置管理"
    width="90%"
    :before-close="handleClose"
    class="llm-config-dialog"
  >
    <div class="llm-config-manager">
      <!-- 操作栏 -->
      <div class="action-bar">
        <el-button type="primary" @click="showAddDialog = true">
          <el-icon><Plus /></el-icon>
          添加配置
        </el-button>
        <el-button @click="initDefaultConfigs" :loading="initLoading">
          <el-icon><Setting /></el-icon>
          初始化默认配置
        </el-button>
        <el-button @click="loadConfigs" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>

      <!-- 配置列表 -->
      <el-table :data="configs" v-loading="loading" stripe style="width: 100%" class="config-table">
        <el-table-column prop="display_name" label="显示名称" width="150" />
        <el-table-column prop="module_name" label="模块名称" width="120" />
        <el-table-column prop="model_name" label="模型名称" width="120" />
        <el-table-column prop="base_url" label="API地址" min-width="200" show-overflow-tooltip />
        <el-table-column prop="temperature" label="温度" width="80" />
        <el-table-column prop="max_tokens" label="最大Token" width="100" />
        <el-table-column prop="is_enabled" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_enabled ? 'success' : 'danger'">
              {{ row.is_enabled ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="enable_thinking" label="思考功能" width="100">
          <template #default="{ row }">
            <el-tag :type="row.enable_thinking ? 'warning' : 'info'">
              {{ row.enable_thinking ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editConfig(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteConfig(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 添加/编辑配置对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="editingConfig ? '编辑配置' : '添加配置'"
      width="600px"
      :before-close="handleAddDialogClose"
    >
      <el-form ref="configFormRef" :model="configForm" :rules="configRules" label-width="120px">
        <el-form-item label="模块名称" prop="module_name">
          <el-select
            v-model="configForm.module_name"
            placeholder="请选择模块"
            :disabled="!!editingConfig"
            style="width: 100%"
          >
            <el-option label="智能问答-知识检索" value="chat_kb" />
            <el-option label="智能问答-复杂问答" value="chat_graph" />
            <el-option label="智能分诊" value="triage" />
            <el-option label="应急指导-心肺复苏" value="emergency_cpr" />
            <el-option label="应急指导-外伤处理" value="emergency_trauma" />
            <el-option label="应急指导-中毒处理" value="emergency_poisoning" />
            <el-option label="应急指导-烧伤处理" value="emergency_burn" />
          </el-select>
        </el-form-item>

        <el-form-item label="显示名称" prop="display_name">
          <el-input v-model="configForm.display_name" placeholder="请输入显示名称" />
        </el-form-item>

        <el-form-item label="API密钥" prop="api_key">
          <el-input
            v-model="configForm.api_key"
            type="password"
            placeholder="请输入API密钥"
            show-password
          />
        </el-form-item>

        <el-form-item label="API地址" prop="base_url">
          <el-input v-model="configForm.base_url" placeholder="请输入API基础URL" />
        </el-form-item>

        <el-form-item label="模型名称" prop="model_name">
          <el-input v-model="configForm.model_name" placeholder="请输入模型名称" />
        </el-form-item>

        <el-form-item label="温度参数" prop="temperature">
          <el-input v-model="configForm.temperature" placeholder="0.0-1.0" />
        </el-form-item>

        <el-form-item label="最大Token" prop="max_tokens">
          <el-input v-model="configForm.max_tokens" placeholder="请输入最大Token数" />
        </el-form-item>

        <el-form-item label="是否启用" prop="is_enabled">
          <el-switch v-model="configForm.is_enabled" />
        </el-form-item>

        <el-form-item label="思考功能" prop="enable_thinking">
          <el-switch v-model="configForm.enable_thinking" active-text="启用" inactive-text="禁用" />
          <div class="form-help-text">启用后，AI将显示思考过程（仅支持Qwen系列模型）</div>
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input
            v-model="configForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入配置描述"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="handleAddDialogClose">取消</el-button>
        <el-button type="primary" @click="saveConfig" :loading="saveLoading">
          {{ editingConfig ? '更新' : '添加' }}
        </el-button>
      </template>
    </el-dialog>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus/es'
import { Plus, Setting, Refresh } from '@element-plus/icons-vue'
import { llmConfigApi } from '@/api/llm-config'

interface LLMConfig {
  id: string
  module_name: string
  display_name: string
  api_key: string
  base_url: string
  model_name: string
  temperature: string
  max_tokens: string
  is_enabled: boolean
  enable_thinking: boolean
  description?: string
  created_at: string
  updated_at: string
}

interface ConfigForm {
  module_name: string
  display_name: string
  api_key: string
  base_url: string
  model_name: string
  temperature: string
  max_tokens: string
  is_enabled: boolean
  enable_thinking: boolean
  description: string
}

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

const configs = ref<LLMConfig[]>([])
const loading = ref(false)
const initLoading = ref(false)
const saveLoading = ref(false)
const showAddDialog = ref(false)
const editingConfig = ref<LLMConfig | null>(null)
const configFormRef = ref<FormInstance>()

const configForm = ref<ConfigForm>({
  module_name: '',
  display_name: '',
  api_key: '',
  base_url: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
  model_name: 'qwen-plus',
  temperature: '0.7',
  max_tokens: '2000',
  is_enabled: true,
  enable_thinking: false,
  description: '',
})

const configRules: FormRules = {
  module_name: [{ required: true, message: '请选择模块名称', trigger: 'change' }],
  display_name: [{ required: true, message: '请输入显示名称', trigger: 'blur' }],
  api_key: [{ required: true, message: '请输入API密钥', trigger: 'blur' }],
  base_url: [{ required: true, message: '请输入API地址', trigger: 'blur' }],
  model_name: [{ required: true, message: '请输入模型名称', trigger: 'blur' }],
  temperature: [
    { required: true, message: '请输入温度参数', trigger: 'blur' },
    { pattern: /^(0(\.\d+)?|1(\.0+)?)$/, message: '温度参数应在0-1之间', trigger: 'blur' },
  ],
  max_tokens: [
    { required: true, message: '请输入最大Token数', trigger: 'blur' },
    { pattern: /^\d+$/, message: '最大Token数应为正整数', trigger: 'blur' },
  ],
}

const loadConfigs = async () => {
  loading.value = true
  try {
    const response = await llmConfigApi.getConfigs()
    configs.value = response.data
  } catch (error) {
    console.error('Failed to load LLM configs:', error)
    ElMessage.error('加载配置失败')
  } finally {
    loading.value = false
  }
}

const initDefaultConfigs = async () => {
  initLoading.value = true
  try {
    await llmConfigApi.initDefaultConfigs()
    ElMessage.success('默认配置初始化成功')
    await loadConfigs()
  } catch (error) {
    console.error('Failed to init default configs:', error)
    ElMessage.error('初始化默认配置失败')
  } finally {
    initLoading.value = false
  }
}

const editConfig = (config: LLMConfig) => {
  editingConfig.value = config
  configForm.value = {
    module_name: config.module_name,
    display_name: config.display_name,
    api_key: config.api_key,
    base_url: config.base_url,
    model_name: config.model_name,
    temperature: config.temperature,
    max_tokens: config.max_tokens,
    is_enabled: config.is_enabled,
    enable_thinking: config.enable_thinking,
    description: config.description || '',
  }
  showAddDialog.value = true
}

const deleteConfig = async (config: LLMConfig) => {
  try {
    await ElMessageBox.confirm(`确定要删除配置"${config.display_name}"吗？`, '确认删除')

    await llmConfigApi.deleteConfig(config.id)
    ElMessage.success('删除成功')
    await loadConfigs()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('Failed to delete config:', error)
      ElMessage.error('删除失败')
    }
  }
}

const saveConfig = async () => {
  if (!configFormRef.value) return

  try {
    await configFormRef.value.validate()
    saveLoading.value = true

    if (editingConfig.value) {
      // 更新配置
      await llmConfigApi.updateConfig(editingConfig.value.id, configForm.value)
      ElMessage.success('更新成功')
    } else {
      // 创建配置
      await llmConfigApi.createConfig(configForm.value)
      ElMessage.success('添加成功')
    }

    handleAddDialogClose()
    await loadConfigs()
  } catch (error) {
    console.error('Failed to save config:', error)
    ElMessage.error(editingConfig.value ? '更新失败' : '添加失败')
  } finally {
    saveLoading.value = false
  }
}

const handleClose = () => {
  visible.value = false
}

const handleAddDialogClose = () => {
  showAddDialog.value = false
  editingConfig.value = null
  configForm.value = {
    module_name: '',
    display_name: '',
    api_key: '',
    base_url: 'https://dashscope.aliyuncs.com/compatible-mode/v1',
    model_name: 'qwen-plus',
    temperature: '0.7',
    max_tokens: '2000',
    is_enabled: true,
    enable_thinking: false,
    description: '',
  }
  configFormRef.value?.resetFields()
}

onMounted(() => {
  if (visible.value) {
    loadConfigs()
  }
})

// 监听对话框打开
watch(
  () => visible.value,
  (newVal) => {
    if (newVal) {
      loadConfigs()
    }
  },
)
</script>

<style scoped>
.llm-config-dialog :deep(.el-dialog__body) {
  padding: 20px;
}

.llm-config-manager {
  min-height: 400px;
}

.action-bar {
  margin-bottom: 20px;
  display: flex;
  gap: 12px;
}

.config-table {
  border-radius: 8px;
  overflow: hidden;
}

.config-table :deep(.el-table__header) {
  background-color: #f8fafc;
}

.config-table :deep(.el-table__row:hover) {
  background-color: #f8fafc;
}

.config-table {
  margin-top: 20px;
}

.form-help-text {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
  line-height: 1.4;
}
</style>
