<!-- 联系我们部分 -->
<template>
  <section id="contact" class="py-20 bg-white">
    <div class="container mx-auto px-4">
      <div class="text-center mb-16">
        <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">联系我们</h2>
        <p class="text-gray-600 max-w-2xl mx-auto text-lg">
          如有任何问题或合作意向，请随时与我们联系
        </p>
        <div class="w-20 h-1 bg-red-600 mx-auto mt-6"></div>
      </div>

      <div
        class="bg-gray-50 p-8 md:p-12 rounded-2xl shadow-md max-w-4xl mx-auto transform transition-all duration-300 hover:shadow-lg"
      >
        <div class="grid md:grid-cols-2 gap-12">
          <!-- 联系方式 -->
          <div>
            <h3 class="text-xl font-bold mb-6">联系方式</h3>
            <div class="space-y-6">
              <div class="flex items-start">
                <div
                  class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center mr-4 mt-1 flex-shrink-0"
                >
                  <i class="fas fa-envelope text-red-600"></i>
                </div>
                <div>
                  <h4 class="font-semibold mb-1">邮箱</h4>
                  <p class="text-gray-600">{{ contactInfo.email }}</p>
                </div>
              </div>

              <div class="flex items-start">
                <div
                  class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center mr-4 mt-1 flex-shrink-0"
                >
                  <i class="fab fa-weixin text-red-600"></i>
                </div>
                <div>
                  <h4 class="font-semibold mb-1">微信</h4>
                  <p class="text-gray-600">{{ contactInfo.wechat }}</p>
                </div>
              </div>

              <div class="flex items-start">
                <div
                  class="w-10 h-10 rounded-full bg-red-100 flex items-center justify-center mr-4 mt-1 flex-shrink-0"
                >
                  <i class="fab fa-github text-red-600"></i>
                </div>
                <div>
                  <h4 class="font-semibold mb-1">GitHub</h4>
                  <p class="text-gray-600">{{ contactInfo.github }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 留言表单 -->
          <div>
            <h3 class="text-xl font-bold mb-6">留言咨询</h3>
            <el-form ref="messageFormRef" :model="form" :rules="rules" label-position="top">
              <el-form-item label="姓名" prop="name" class="mb-4">
                <el-input
                  v-model="form.name"
                  placeholder="请输入您的姓名"
                  :maxlength="20"
                  show-word-limit
                  class="custom-input"
                />
              </el-form-item>

              <el-form-item label="邮箱" prop="email" class="mb-4">
                <el-input v-model="form.email" placeholder="请输入您的邮箱" class="custom-input" />
              </el-form-item>

              <el-form-item label="留言内容" prop="content" class="mb-6">
                <el-input
                  v-model="form.content"
                  type="textarea"
                  :rows="4"
                  placeholder="请输入您的留言内容..."
                  :maxlength="500"
                  show-word-limit
                  class="custom-input"
                />
              </el-form-item>

              <el-form-item>
                <el-button
                  type="danger"
                  class="w-full h-12 text-lg"
                  :loading="submitting"
                  @click="submitForm"
                >
                  发送留言
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { FormInstance, FormRules } from 'element-plus/es'
import { ElMessage } from 'element-plus/es'

interface ContactInfo {
  email: string
  wechat: string
  github: string
}

const contactInfo = ref<ContactInfo>({
  email: 'contact@prehospital.ai',
  wechat: 'PreHospital-AI',
  github: 'github.com/prehospital-ai',
})

const messageFormRef = ref<FormInstance>()
const submitting = ref(false)

const form = reactive({
  name: '',
  email: '',
  content: '',
})

const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' },
  ],
  content: [
    { required: true, message: '请输入留言内容', trigger: 'blur' },
    { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' },
  ],
})

const submitForm = async () => {
  if (!messageFormRef.value) return

  await messageFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      submitting.value = true
      try {
        const { submitContactMessage } = await import('@/api/message')
        const response = await submitContactMessage({
          name: form.name,
          email: form.email,
          content: form.content,
        })

        if (response.code === 200 || response.code === 201) {
          ElMessage.success('留言提交成功，我们会尽快回复您！')
          messageFormRef.value?.resetFields()
        } else {
          ElMessage.error(response.message || '留言提交失败，请稍后重试')
        }
      } catch (error: any) {
        console.error('提交留言出错:', error)
        ElMessage.error(error.message || '留言提交失败，请稍后重试')
      } finally {
        submitting.value = false
      }
    }
  })
}
</script>

<style scoped>
.container {
  max-width: 1280px;
}

.custom-input :deep(.el-input__wrapper) {
  box-shadow: none;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
}

.custom-input :deep(.el-input__wrapper:hover) {
  border-color: #dc2626;
}

.custom-input :deep(.el-input__wrapper.is-focus) {
  border-color: #dc2626;
  box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.1);
}

.custom-input :deep(.el-textarea__inner) {
  box-shadow: none;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
}

.custom-input :deep(.el-textarea__inner:hover) {
  border-color: #dc2626;
}

.custom-input :deep(.el-textarea__inner:focus) {
  border-color: #dc2626;
  box-shadow: 0 0 0 2px rgba(220, 38, 38, 0.1);
}

:deep(.el-form-item__label) {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}
</style>
