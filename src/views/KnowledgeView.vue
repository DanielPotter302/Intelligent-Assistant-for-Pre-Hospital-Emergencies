<template>
  <div class="flex flex-col min-h-screen bg-neutral-100 text-neutral-700">
    <!-- 子导航栏 Tab -->
    <nav class="bg-white border-b border-neutral-200 sticky top-16 z-40">
      <div class="container mx-auto px-4">
        <div class="flex items-center overflow-x-auto scrollbar-hide space-x-6 py-3">
          <button 
            :class="['whitespace-nowrap pb-2 transition-colors', 
              activeTab === 'doc' ? 'text-primary font-medium border-b-2 border-primary' : 'text-neutral-500 hover:text-primary']"
            @click="activeTab = 'doc'"
          >文档</button>
          <button 
            :class="['whitespace-nowrap pb-2 transition-colors', 
              activeTab === 'video' ? 'text-primary font-medium border-b-2 border-primary' : 'text-neutral-500 hover:text-primary']"
            @click="activeTab = 'video'"
          >视频</button>
          <button 
            :class="['whitespace-nowrap pb-2 transition-colors', 
              activeTab === 'favorite' ? 'text-primary font-medium border-b-2 border-primary' : 'text-neutral-500 hover:text-primary']"
            @click="activeTab = 'favorite'"
          >我的收藏</button>
        </div>
      </div>
    </nav>

    <!-- 主内容区 -->
    <main class="flex-grow">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

type TabType = 'doc' | 'video' | 'favorite'
const activeTab = ref<TabType>('doc')

const paths = {
  'doc': '/knowledge/documents',
  'video': '/knowledge/videos',
  'favorite': '/knowledge/favorites'
} as const

// 监听 activeTab 变化，切换路由
watch(activeTab, (newTab) => {
  router.push(paths[newTab])
})

// 根据当前路由设置激活的标签
onMounted(() => {
  const path = route.path
  if (path.includes('/documents')) {
    activeTab.value = 'doc'
  } else if (path.includes('/videos')) {
    activeTab.value = 'video'
  } else if (path.includes('/favorites')) {
    activeTab.value = 'favorite'
  }
})
</script>

<style scoped>
.scrollbar-hide {
  scrollbar-width: none;
  -ms-overflow-style: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style> 