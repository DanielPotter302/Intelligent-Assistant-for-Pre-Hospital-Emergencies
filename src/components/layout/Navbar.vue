<!-- 导航栏组件 -->
<template>
  <header class="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-sm shadow-sm">
    <div class="container mx-auto">
      <div class="flex justify-between items-center h-16 px-4">
        <!-- Logo和项目名 - 管理员页面不显示 -->
        <div
          v-if="!isAdminPage"
          class="flex items-center space-x-3 group cursor-pointer"
          @click="goToHome"
        >
          <div
            class="w-10 h-10 rounded-lg bg-red-600 flex items-center justify-center transform group-hover:rotate-12 transition-all duration-300 shadow-lg hover:shadow-red-500/50"
          >
            <i class="fa fa-medkit text-white text-xl"></i>
          </div>
          <span class="font-bold text-xl text-gray-900 group-hover:text-red-600 transition-colors"
            >院前应急智能助手</span
          >
        </div>

        <!-- 管理员页面的简化标题 -->
        <div v-if="isAdminPage" class="flex items-center">
          <span class="font-semibold text-lg text-gray-700">系统管理与配置</span>
        </div>

        <!-- 中间导航 - 只有登录的普通用户可见，管理员不显示 -->
        <div
          v-if="userStore.isLoggedIn && userStore.userRole !== 'admin'"
          class="hidden md:flex items-center space-x-8"
        >
          <router-link
            to="/knowledge"
            class="relative py-4 px-2 text-gray-700 hover:text-primary transition-colors"
            :class="{
              'text-primary after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-primary':
                isActivePage('knowledge'),
            }"
          >
            知识库
          </router-link>
          <router-link
            to="/ai-chat"
            class="relative py-4 px-2 text-gray-700 hover:text-primary transition-colors"
            :class="{
              'text-primary after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-primary':
                isActivePage('ai-chat'),
            }"
          >
            智能问答
          </router-link>
          <router-link
            to="/emergency-guide"
            class="relative py-4 px-2 text-gray-700 hover:text-primary transition-colors"
            :class="{
              'text-primary after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-primary':
                isActivePage('emergency-guide'),
            }"
          >
            应急指导
          </router-link>
          <router-link
            to="/smart-triage"
            class="relative py-4 px-2 text-gray-700 hover:text-primary transition-colors"
            :class="{
              'text-primary after:absolute after:bottom-0 after:left-0 after:right-0 after:h-0.5 after:bg-primary':
                isActivePage('smart-triage'),
            }"
          >
            智能分诊
          </router-link>
        </div>

        <!-- 右侧按钮 -->
        <div class="flex items-center space-x-4">
          <!-- 未登录状态 -->
          <template v-if="!userStore.isLoggedIn">
            <button
              class="px-4 py-2 text-gray-700 hover:text-primary transition-colors"
              @click="goToLogin"
            >
              登录
            </button>
            <button
              class="px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transform hover:-translate-y-0.5 transition-all duration-300 shadow-lg hover:shadow-red-500/50"
              @click="goToRegister"
            >
              注册
            </button>
          </template>

          <!-- 已登录状态 -->
          <template v-else>
            <!-- 用户菜单 -->
            <el-dropdown @command="handleUserMenuCommand" trigger="click">
              <div
                class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 px-3 py-2 rounded-lg transition-colors"
              >
                <div
                  class="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center text-primary font-medium"
                >
                  <span>{{ userStore.userName.charAt(0) }}</span>
                </div>
                <span class="text-gray-700 font-medium">{{ userStore.userName }}</span>
                <el-icon class="text-gray-400"><ArrowDown /></el-icon>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon>
                    个人资料
                  </el-dropdown-item>
                  <el-dropdown-item command="settings">
                    <el-icon><Setting /></el-icon>
                    设置
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ArrowDown, User, Setting, SwitchButton } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const isKnowledgePage = computed(() => route.path.startsWith('/knowledge'))
const isAdminPage = computed(() => route.path.startsWith('/admin'))

const isActivePage = (path: string) => {
  return route.path.startsWith('/' + path)
}

const goToHome = () => {
  router.push('/')
}

const goToLogin = () => {
  router.push('/login')
}

const goToRegister = () => {
  router.push('/register')
}

const goToKnowledge = () => {
  router.push('/knowledge')
}

// 处理用户菜单命令
const handleUserMenuCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      // TODO: 跳转到个人资料页面
      console.log('Go to profile')
      break
    case 'settings':
      // TODO: 跳转到设置页面
      console.log('Go to settings')
      break
    case 'logout':
      await userStore.logoutUser()
      router.push('/')
      break
  }
}
</script>

<style scoped>
.container {
  max-width: 1280px;
}
</style>
