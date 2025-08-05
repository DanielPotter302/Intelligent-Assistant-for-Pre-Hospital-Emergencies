import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { tokenManager } from '@/api/auth'
import HomeView from '@/views/HomeView.vue'
import KnowledgeView from '@/views/KnowledgeView.vue'
import DocumentView from '@/components/knowledge/DocumentView.vue'
import VideoView from '@/components/knowledge/VideoView.vue'
import FavoriteView from '@/components/knowledge/FavoriteView.vue'
import AIChat from '@/views/AIChat.vue'
import EmergencyGuide from '@/views/EmergencyGuide.vue'
import SmartTriage from '@/views/SmartTriage.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import AdminView from '@/views/AdminView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: {
        title: '登录',
        requiresGuest: true, // 只有未登录用户可以访问
      },
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: {
        title: '注册',
        requiresGuest: true, // 只有未登录用户可以访问
      },
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        requiresAuth: false, // 首页不需要登录
      },
    },
    {
      path: '/knowledge',
      component: KnowledgeView,
      meta: {
        requiresAuth: true, // 知识库需要登录
      },
      children: [
        {
          path: 'documents',
          name: 'knowledge-documents',
          component: DocumentView,
        },
        {
          path: 'videos',
          name: 'knowledge-videos',
          component: VideoView,
        },
        {
          path: 'favorites',
          name: 'knowledge-favorites',
          component: FavoriteView,
        },
        {
          path: '',
          redirect: '/knowledge/documents',
        },
      ],
    },
    {
      path: '/ai-chat',
      name: 'ai-chat',
      component: AIChat,
      meta: {
        title: '智能问答',
        requiresAuth: true, // 需要登录
      },
    },
    {
      path: '/emergency-guide',
      name: 'emergency-guide',
      component: EmergencyGuide,
      meta: {
        title: '应急指导',
        requiresAuth: true, // 需要登录
      },
    },
    {
      path: '/smart-triage',
      name: 'smart-triage',
      component: SmartTriage,
      meta: {
        title: '智能分诊',
        requiresAuth: true, // 需要登录
      },
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminView,
      meta: {
        title: '管理员后台',
        requiresAuth: true,
        requiresRole: 'admin', // 需要管理员权限
      },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      redirect: '/',
    },
  ],
  scrollBehavior() {
    // 始终滚动到顶部
    return { top: 0 }
  },
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 设置页面标题
  document.title = to.meta?.title ? `${to.meta.title} - 院前应急智能助手` : '院前应急智能助手'

  const userStore = useUserStore()
  const hasToken = tokenManager.hasToken()

  // 如果有token但没有用户信息，尝试获取用户信息
  if (hasToken && !userStore.user) {
    try {
      await userStore.fetchUserInfo()
    } catch (error) {
      console.error('Failed to fetch user info:', error)
      // 获取用户信息失败，清除token
      tokenManager.clearTokens()
    }
  }

  const isLoggedIn = userStore.isLoggedIn

  // 检查需要登录的路由
  if (to.meta?.requiresAuth && !isLoggedIn) {
    // 需要登录但未登录，跳转到登录页
    next({
      path: '/login',
      query: { redirect: to.fullPath }, // 保存原始路径，登录后跳转回来
    })
    return
  }

  // 检查只有未登录用户可以访问的路由
  if (to.meta?.requiresGuest && isLoggedIn) {
    // 已登录用户访问登录/注册页，跳转到首页
    next('/')
    return
  }

  // 检查权限
  if (to.meta?.requiresRole && !userStore.hasPermission(to.meta.requiresRole as string)) {
    // 权限不足，跳转到首页
    next('/')
    return
  }

  next()
})

export default router
