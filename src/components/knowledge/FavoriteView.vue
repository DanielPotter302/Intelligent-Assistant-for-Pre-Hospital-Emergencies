<template>
  <div class="container mx-auto px-4 py-6">
    <!-- 面包屑导航 -->
    <div class="bg-white border-b border-neutral-200 py-2 mb-6">
      <div class="text-sm text-neutral-500">
        <a href="#" class="hover:text-primary" @click.prevent="goToHome">首页</a>
        <span class="mx-2"><i class="fa fa-angle-right text-xs"></i></span>
        <span class="text-neutral-700">我的收藏</span>
      </div>
    </div>

    <!-- 收藏内容 -->
    <div class="bg-white rounded-lg shadow-sm p-6">
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-neutral-700 mb-2">我的收藏</h1>
        <p class="text-neutral-500">您收藏的知识内容和视频教程</p>
      </div>

      <!-- 筛选标签 -->
      <div class="mb-6">
        <div class="flex items-center gap-4">
          <span class="text-neutral-700 font-medium">筛选:</span>
          <div class="flex flex-wrap gap-2">
            <button
              class="px-3 py-1.5 rounded-md border transition-colors"
              :class="[
                selectedType === 'all'
                  ? 'bg-primary text-white border-primary'
                  : 'border-neutral-300 hover:border-primary text-neutral-600 hover:text-primary',
              ]"
              @click="selectedType = 'all'"
            >
              全部
            </button>
            <button
              class="px-3 py-1.5 rounded-md border transition-colors"
              :class="[
                selectedType === 'item'
                  ? 'bg-primary text-white border-primary'
                  : 'border-neutral-300 hover:border-primary text-neutral-600 hover:text-primary',
              ]"
              @click="selectedType = 'item'"
            >
              知识内容
            </button>
            <button
              class="px-3 py-1.5 rounded-md border transition-colors"
              :class="[
                selectedType === 'video'
                  ? 'bg-primary text-white border-primary'
                  : 'border-neutral-300 hover:border-primary text-neutral-600 hover:text-primary',
              ]"
              @click="selectedType = 'video'"
            >
              视频教程
            </button>
          </div>
        </div>
      </div>

      <!-- 收藏列表 -->
      <div v-if="filteredFavorites.length > 0" class="space-y-4">
        <div
          v-for="favorite in filteredFavorites"
          :key="favorite.id"
          class="favorite-item border border-neutral-200 rounded-lg p-4 hover:border-primary/30 transition-colors"
        >
          <!-- 知识内容 -->
          <div v-if="favorite.favorite_type === 'item'" class="flex items-start gap-4">
            <div
              class="flex-shrink-0 w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center"
            >
              <i class="fa fa-book text-primary text-lg"></i>
            </div>
            <div class="flex-1">
              <div class="flex items-start justify-between">
                <div>
                  <h3 class="font-medium text-neutral-800 mb-1">{{ favorite.item?.title }}</h3>
                  <p class="text-sm text-neutral-600 line-clamp-2 mb-2">
                    {{ favorite.item?.content }}
                  </p>
                  <div class="flex items-center text-xs text-neutral-500 gap-4">
                    <span>作者: {{ favorite.item?.author }}</span>
                    <span>浏览量: {{ favorite.item?.view_count }}</span>
                    <span>收藏时间: {{ formatDate(favorite.created_at) }}</span>
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <button
                    class="px-3 py-1.5 rounded-md border border-neutral-300 hover:bg-neutral-50 text-neutral-600 transition-colors"
                    @click="handleViewItem(favorite.item)"
                  >
                    查看详情
                  </button>
                  <button
                    class="px-3 py-1.5 rounded-md border border-red-300 hover:bg-red-50 text-red-600 transition-colors"
                    @click="handleRemoveFavorite(favorite)"
                  >
                    取消收藏
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 视频 -->
          <div v-else-if="favorite.favorite_type === 'video'" class="flex items-start gap-4">
            <div
              class="flex-shrink-0 w-12 h-12 bg-blue-500/10 rounded-lg flex items-center justify-center"
            >
              <i class="fa fa-video-camera text-blue-500 text-lg"></i>
            </div>
            <div class="flex-1">
              <div class="flex items-start justify-between">
                <div>
                  <h3 class="font-medium text-neutral-800 mb-1">{{ favorite.video?.title }}</h3>
                  <p class="text-sm text-neutral-600 line-clamp-2 mb-2">
                    {{ favorite.video?.description }}
                  </p>
                  <div class="flex items-center text-xs text-neutral-500 gap-4">
                    <span>分类: {{ favorite.video?.category?.name }}</span>
                    <span>收藏时间: {{ formatDate(favorite.created_at) }}</span>
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <button
                    class="px-3 py-1.5 rounded-md border border-neutral-300 hover:bg-neutral-50 text-neutral-600 transition-colors"
                    @click="handleViewVideo(favorite.video)"
                  >
                    观看视频
                  </button>
                  <button
                    class="px-3 py-1.5 rounded-md border border-red-300 hover:bg-red-50 text-red-600 transition-colors"
                    @click="handleRemoveFavorite(favorite)"
                  >
                    取消收藏
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-else class="text-center py-12">
        <i class="fa fa-bookmark text-4xl text-neutral-300 mb-4"></i>
        <h3 class="text-lg font-medium text-neutral-700 mb-2">暂无收藏</h3>
        <p class="text-neutral-500 mb-4">您还没有收藏任何内容</p>
        <div class="flex justify-center gap-4">
          <button
            class="px-4 py-2 rounded-md bg-primary text-white hover:bg-primary/90 transition-colors"
            @click="goToDocuments"
          >
            浏览知识库
          </button>
          <button
            class="px-4 py-2 rounded-md border border-neutral-300 hover:bg-neutral-50 text-neutral-600 transition-colors"
            @click="goToVideos"
          >
            观看视频
          </button>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="totalPages > 1" class="mt-6 flex justify-center">
        <nav class="flex items-center space-x-2">
          <button
            class="px-3 py-2 rounded-md border border-neutral-300 hover:bg-neutral-50 disabled:opacity-50"
            :disabled="currentPage === 1"
            @click="handlePageChange(currentPage - 1)"
          >
            上一页
          </button>
          <span class="px-3 py-2 text-neutral-600"> {{ currentPage }} / {{ totalPages }} </span>
          <button
            class="px-3 py-2 rounded-md border border-neutral-300 hover:bg-neutral-50 disabled:opacity-50"
            :disabled="currentPage === totalPages"
            @click="handlePageChange(currentPage + 1)"
          >
            下一页
          </button>
        </nav>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getFavorites, removeFavorite } from '@/api/knowledge'

const router = useRouter()

// 响应式数据
const favorites = ref<any[]>([])
const selectedType = ref<'all' | 'item' | 'video'>('all')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 计算属性
const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

const filteredFavorites = computed(() => {
  if (selectedType.value === 'all') {
    return favorites.value
  }
  return favorites.value.filter((fav) => fav.favorite_type === selectedType.value)
})

// 方法
const loadFavorites = async () => {
  try {
    const response = await getFavorites(currentPage.value, pageSize.value)
    favorites.value = response.data.records
    total.value = response.data.total
  } catch (error) {
    ElMessage.error('加载收藏失败')
  }
}

const handlePageChange = async (page: number) => {
  currentPage.value = page
  await loadFavorites()
}

const handleViewItem = (item: any) => {
  // 跳转到知识内容详情页
  router.push(`/knowledge/documents?item=${item.id}`)
}

const handleViewVideo = (video: any) => {
  window.open(video.video_url, '_blank')
}

const handleRemoveFavorite = async (favorite: any) => {
  try {
    await ElMessageBox.confirm('确定要取消收藏吗？')

    await removeFavorite(favorite.id)
    ElMessage.success('取消收藏成功')
    await loadFavorites()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('取消收藏失败')
    }
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const goToHome = () => {
  router.push('/')
}

const goToDocuments = () => {
  router.push('/knowledge/documents')
}

const goToVideos = () => {
  router.push('/knowledge/videos')
}

// 初始化
onMounted(() => {
  loadFavorites()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.favorite-item:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
