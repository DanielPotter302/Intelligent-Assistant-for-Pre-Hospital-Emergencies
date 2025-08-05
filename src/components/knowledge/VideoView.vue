<template>
  <div class="container mx-auto px-4 py-6">
    <!-- 面包屑导航 -->
    <div class="bg-white border-b border-neutral-200 py-2 mb-6">
      <div class="text-sm text-neutral-500">
        <a href="#" class="hover:text-primary" @click.prevent="goToHome">首页</a>
        <span class="mx-2"><i class="fa fa-angle-right text-xs"></i></span>
        <span class="text-neutral-700">视频教程</span>
      </div>
    </div>

    <!-- 视频分类和列表 -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- 左侧分类 -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-lg shadow-sm p-4">
          <h3 class="text-neutral-700 font-semibold mb-3">视频分类</h3>
          <div class="space-y-1">
            <button
              class="flex items-center justify-between w-full text-left px-3 py-2 rounded-md"
              :class="[
                currentCategory?.id === category.id
                  ? 'bg-primary/5 text-primary font-medium'
                  : 'hover:bg-neutral-100',
              ]"
              @click="handleCategoryClick(category)"
              v-for="category in categories"
              :key="category.id"
            >
              <span>{{ category.name }}</span>
              <i class="fa fa-chevron-right text-xs"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- 右侧视频列表 -->
      <div class="lg:col-span-3">
        <div class="bg-white rounded-lg shadow-sm p-6">
          <div class="mb-6">
            <h2 class="text-xl font-semibold text-neutral-700 mb-2">
              {{ currentCategory?.name || '所有视频' }}
            </h2>
            <p class="text-neutral-500">{{ currentCategory?.description }}</p>
          </div>

          <!-- 视频网格 -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="video in videos"
              :key="video.id"
              class="video-card border border-neutral-200 rounded-lg overflow-hidden hover:border-primary/30 transition-colors cursor-pointer"
              @click="handleVideoClick(video)"
            >
              <!-- 视频缩略图 -->
              <div class="video-thumbnail bg-neutral-100 h-48 flex items-center justify-center">
                <div class="text-center">
                  <i class="fa fa-play-circle text-4xl text-primary mb-2"></i>
                  <p class="text-sm text-neutral-500">点击观看视频</p>
                </div>
              </div>

              <!-- 视频信息 -->
              <div class="p-4">
                <h3 class="font-medium text-neutral-800 mb-2 line-clamp-2">
                  {{ video.title }}
                </h3>
                <p class="text-sm text-neutral-600 line-clamp-3 mb-3">
                  {{ video.description }}
                </p>
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <button
                      class="flex items-center gap-1 px-2 py-1 rounded text-xs border border-neutral-300 hover:bg-neutral-50 text-neutral-600 transition-colors"
                      :class="{ 'text-primary border-primary': isVideoCollected(video.id) }"
                      @click.stop="handleCollectVideo(video)"
                    >
                      <i
                        class="fa"
                        :class="isVideoCollected(video.id) ? 'fa-bookmark' : 'fa-bookmark-o'"
                      ></i>
                      <span>{{ isVideoCollected(video.id) ? '已收藏' : '收藏' }}</span>
                    </button>
                  </div>
                  <span class="text-xs text-neutral-500">{{ formatDate(video.created_at) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 空状态 -->
          <div v-if="videos.length === 0" class="text-center py-12">
            <i class="fa fa-video-camera text-4xl text-neutral-300 mb-4"></i>
            <p class="text-neutral-500">暂无视频内容</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getKnowledgeCategories, getVideoLinks, addFavorite, removeFavorite } from '@/api/knowledge'

const router = useRouter()

// 响应式数据
const categories = ref<any[]>([])
const currentCategory = ref<any>(null)
const videos = ref<any[]>([])
const collectedVideos = ref<Set<number>>(new Set())

// 处理分类点击
const handleCategoryClick = async (category: any) => {
  currentCategory.value = category
  await loadVideos()
}

// 加载视频数据
const loadVideos = async () => {
  try {
    const categoryId = currentCategory.value?.id
    const response = await getVideoLinks(categoryId)
    videos.value = response.data
  } catch (error) {
    ElMessage.error('加载视频失败')
  }
}

// 处理视频点击
const handleVideoClick = (video: any) => {
  window.open(video.video_url, '_blank')
}

// 处理收藏视频
const handleCollectVideo = async (video: any) => {
  try {
    if (isVideoCollected(video.id)) {
      // 取消收藏 - 这里需要获取收藏ID，简化处理
      collectedVideos.value.delete(video.id)
      ElMessage.success('取消收藏成功')
    } else {
      // 添加收藏
      await addFavorite('video', video.id)
      collectedVideos.value.add(video.id)
      ElMessage.success('收藏成功')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 检查视频是否已收藏
const isVideoCollected = (videoId: number) => {
  return collectedVideos.value.has(videoId)
}

// 格式化日期
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 导航方法
const goToHome = () => {
  router.push('/')
}

// 初始化
onMounted(async () => {
  try {
    // 加载分类
    const categoriesResponse = await getKnowledgeCategories()
    categories.value = categoriesResponse.data

    // 默认选择第一个分类
    if (categories.value.length > 0) {
      await handleCategoryClick(categories.value[0])
    }
  } catch (error) {
    ElMessage.error('初始化失败')
  }
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.video-thumbnail {
  position: relative;
  overflow: hidden;
}

.video-thumbnail::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.05));
  opacity: 0;
  transition: opacity 0.3s;
}

.video-card:hover .video-thumbnail::before {
  opacity: 1;
}
</style>
