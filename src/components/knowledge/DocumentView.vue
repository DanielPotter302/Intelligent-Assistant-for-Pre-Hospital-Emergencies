<template>
  <!-- 面包屑导航 -->
  <div class="bg-white border-b border-neutral-200 py-2">
    <div class="container mx-auto px-4 text-sm text-neutral-500">
      <a href="#" class="hover:text-primary" @click.prevent="goToHome">首页</a>
      <span class="mx-2"><i class="fa fa-angle-right text-xs"></i></span>
      <a href="#" class="hover:text-primary" @click.prevent="goToCategory">{{
        currentCategory?.name || '知识库'
      }}</a>
      <span class="mx-2"><i class="fa fa-angle-right text-xs"></i></span>
      <span class="text-neutral-700">{{ currentItem?.title || '知识内容' }}</span>
    </div>
  </div>

  <main class="flex-grow container mx-auto px-4 py-6 flex flex-col md:flex-row gap-6">
    <!-- 左侧栏：分类树和推荐书籍 -->
    <aside class="md:w-1/4 lg:w-1/5 shrink-0">
      <!-- 知识库类别 -->
      <div class="bg-white rounded-lg shadow-sm p-4 mb-4">
        <h3 class="text-neutral-700 font-semibold mb-3">知识库类别</h3>
        <div class="space-y-1">
          <!-- 分类列表 -->
          <div v-for="category in categories" :key="category.id">
            <button
              class="flex items-center justify-between w-full text-left px-3 py-2 rounded-md"
              :class="[
                currentCategory?.id === category.id
                  ? 'bg-primary/5 text-primary font-medium'
                  : 'hover:bg-neutral-100',
              ]"
              @click="handleCategoryClick(category)"
            >
              <span>{{ category.name }}</span>
              <i class="fa fa-chevron-right text-xs"></i>
            </button>
          </div>
        </div>
      </div>

      <!-- 推荐书籍 -->
      <div class="bg-white rounded-lg shadow-sm p-4">
        <h3 class="text-neutral-700 font-semibold mb-3 flex items-center">
          <i class="fa fa-book mr-2 text-primary"></i>推荐书籍
        </h3>
        <div class="space-y-4">
          <div v-for="book in books" :key="book.id" class="book-item">
            <div
              class="flex items-start space-x-3 mb-2 cursor-pointer"
              @click="handleBookClick(book)"
            >
              <img
                :src="getBookCoverUrl(book.cover_url)"
                alt="封面"
                class="w-16 h-20 object-cover rounded shadow-sm"
                @error="handleImageError"
              />
              <div class="flex-1">
                <h4
                  class="font-medium text-neutral-800 hover:text-primary transition-colors line-clamp-2"
                >
                  {{ book.title }}
                </h4>
                <p class="text-sm text-neutral-500 mt-1">{{ book.author }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <!-- 右侧内容区 -->
    <div class="md:w-3/4 lg:w-4/5">
      <!-- 内容头部 -->
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="mb-6">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
            <div>
              <h1 class="text-[clamp(1.5rem,3vw,2rem)] font-bold text-neutral-700 mb-2">
                {{ currentItem?.title || '知识内容' }}
              </h1>
              <div class="flex items-center text-neutral-500 text-sm">
                <span>作者: {{ currentItem?.author || '急救医学专家团队' }}</span>
                <span class="mx-2">•</span>
                <span>浏览量: {{ currentItem?.view_count || 0 }}</span>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <button
                class="flex items-center gap-1 px-3 py-1.5 rounded-md border border-neutral-300 hover:bg-neutral-50 text-neutral-600 transition-colors"
                :class="{ 'text-primary border-primary': isCollected }"
                @click="handleCollect"
              >
                <i class="fa" :class="isCollected ? 'fa-bookmark' : 'fa-bookmark-o'"></i>
                <span>{{ isCollected ? '已收藏' : '收藏' }}</span>
              </button>
              <button
                class="flex items-center gap-1 px-3 py-1.5 rounded-md border border-neutral-300 hover:bg-neutral-50 text-neutral-600 transition-colors"
                @click="handleShare"
              >
                <i class="fa fa-share-alt"></i>
                <span>分享</span>
              </button>
            </div>
          </div>

          <!-- 搜索框 -->
          <div class="relative">
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索知识内容..."
              class="w-full pl-10 pr-4 py-2 rounded-lg border border-neutral-300 focus:border-primary focus:ring-1 focus:ring-primary focus:outline-none transition-all"
              @keydown.enter="handleSearch"
            />
            <i class="fa fa-search absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400"></i>
          </div>
        </div>
      </div>

      <!-- 知识内容列表 -->
      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="mb-4">
          <h2 class="text-xl font-semibold text-neutral-700 mb-2">
            {{ currentCategory?.name || '知识内容' }}
          </h2>
          <p class="text-neutral-500">{{ currentCategory?.description }}</p>
        </div>

        <!-- 知识条目列表 -->
        <div class="space-y-4">
          <div
            v-for="item in knowledgeItems"
            :key="item.id"
            class="border border-neutral-200 rounded-lg p-4 hover:border-primary/30 transition-colors cursor-pointer"
            :class="{ 'border-primary bg-primary/5': currentItem?.id === item.id }"
            @click="handleItemClick(item)"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h3 class="font-medium text-neutral-800 mb-2">{{ item.title }}</h3>
                <p class="text-sm text-neutral-600 line-clamp-3">{{ item.content }}</p>
                <div class="flex items-center mt-2 text-xs text-neutral-500">
                  <span>作者: {{ item.author }}</span>
                  <span class="mx-2">•</span>
                  <span>浏览量: {{ item.view_count }}</span>
                </div>
              </div>
            </div>
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

      <!-- 当前选中内容详情 -->
      <div v-if="currentItem" class="bg-white rounded-lg shadow-sm p-6 mt-6">
        <div class="prose max-w-none">
          <h2 class="text-xl font-semibold text-neutral-700 mb-4">{{ currentItem.title }}</h2>
          <div class="text-neutral-700 leading-relaxed whitespace-pre-wrap">
            {{ currentItem.content }}
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  getKnowledgeCategories,
  getKnowledgeItems,
  getKnowledgeItem,
  getBookLinks,
  addFavorite,
  removeFavorite,
  searchKnowledge,
} from '@/api/knowledge'

const router = useRouter()

// 响应式数据
const categories = ref<any[]>([])
const currentCategory = ref<any>(null)
const knowledgeItems = ref<any[]>([])
const currentItem = ref<any>(null)
const books = ref<any[]>([])
const searchKeyword = ref('')
const isCollected = ref(false)

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const totalPages = computed(() => Math.ceil(total.value / pageSize.value))

// 处理分类点击
const handleCategoryClick = async (category: any) => {
  currentCategory.value = category
  currentPage.value = 1
  await loadKnowledgeItems()
}

// 加载知识库内容
const loadKnowledgeItems = async () => {
  if (!currentCategory.value) return

  try {
    const response = await getKnowledgeItems({
      category_id: currentCategory.value.id,
      page: currentPage.value,
      page_size: pageSize.value,
    })

    knowledgeItems.value = response.data.records
    total.value = response.data.total

    if (response.data.records.length > 0) {
      await handleItemClick(response.data.records[0])
    }
  } catch (error) {
    ElMessage.error('加载知识内容失败')
  }
}

// 处理知识条目点击
const handleItemClick = async (item: any) => {
  currentItem.value = item
  try {
    const response = await getKnowledgeItem(item.id)
    currentItem.value = response.data
  } catch (error) {
    ElMessage.error('加载内容详情失败')
  }
}

// 处理书籍点击
const handleBookClick = (book: any) => {
  window.open(book.book_url, '_blank')
}

// 获取书籍封面URL
const getBookCoverUrl = (coverUrl: string) => {
  if (!coverUrl) {
    return '/src/assets/images/default-book-cover.jpg'
  }
  // 如果coverUrl已经是完整URL，直接返回
  if (coverUrl.startsWith('http')) {
    return coverUrl
  }
  // 否则拼接后端API地址
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  return `${baseUrl}${coverUrl}`
}

// 处理图片加载错误
const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = '/src/assets/images/default-book-cover.jpg'
}

// 处理搜索
const handleSearch = async () => {
  if (!searchKeyword.value.trim()) return

  try {
    const response = await searchKnowledge({
      keyword: searchKeyword.value,
      page: 1,
      page_size: 10,
    })

    knowledgeItems.value = response.data.records
    total.value = response.data.total
    currentPage.value = 1

    ElMessage.success(`找到 ${response.data.total} 条相关内容`)
  } catch (error) {
    ElMessage.error('搜索失败')
  }
}

// 处理收藏
const handleCollect = async () => {
  if (!currentItem.value) return

  try {
    if (isCollected.value) {
      await removeFavorite(currentItem.value.id)
    } else {
      await addFavorite('item', currentItem.value.id)
    }
    isCollected.value = !isCollected.value
    ElMessage.success(isCollected.value ? '收藏成功' : '取消收藏成功')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 处理分享
const handleShare = async () => {
  if (!currentItem.value) return

  try {
    const url = `${window.location.origin}/knowledge/item/${currentItem.value.id}`
    await navigator.clipboard.writeText(url)
    ElMessage.success('链接已复制到剪贴板')
  } catch (error) {
    ElMessage.error('分享失败')
  }
}

// 处理分页
const handlePageChange = async (page: number) => {
  currentPage.value = page
  await loadKnowledgeItems()
}

// 加载书籍数据
const loadBooks = async () => {
  try {
    const response = await getBookLinks()
    books.value = response.data
  } catch (error) {
    ElMessage.error('加载书籍失败')
  }
}

// 导航方法
const goToHome = () => {
  router.push('/')
}

const goToCategory = () => {
  if (currentCategory.value) {
    console.log('Navigate to category:', currentCategory.value.name)
  }
}

// 监听分类变化
watch(currentCategory, () => {
  if (currentCategory.value) {
    loadKnowledgeItems()
  }
})

// 初始化
onMounted(async () => {
  try {
    // 加载分类
    const categoriesResponse = await getKnowledgeCategories()
    categories.value = categoriesResponse.data

    // 加载书籍
    await loadBooks()

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

:deep(.prose) {
  max-width: none;
}
</style>
