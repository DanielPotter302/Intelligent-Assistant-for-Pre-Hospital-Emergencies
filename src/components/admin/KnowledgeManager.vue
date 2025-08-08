<template>
  <el-dialog
    v-model="visible"
    title="知识库管理"
    width="90%"
    :before-close="handleClose"
    class="knowledge-manager-dialog"
  >
    <div class="knowledge-manager">
      <!-- 标签页 -->
      <el-tabs v-model="activeTab" class="knowledge-tabs">
        <el-tab-pane label="知识内容" name="content">
          <div class="tab-content">
            <div class="toolbar">
              <el-button type="primary" @click="showAddContentDialog = true">
                <el-icon><Plus /></el-icon>
                添加知识内容
              </el-button>
              <el-input
                v-model="contentSearchKeyword"
                placeholder="搜索知识内容..."
                style="width: 300px"
                clearable
                @input="handleContentSearch"
              >
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </div>

            <el-table :data="filteredContent" style="width: 100%" v-loading="contentLoading">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="title" label="标题" min-width="200" />
              <el-table-column prop="content" label="内容" min-width="300" show-overflow-tooltip />
              <el-table-column prop="author" label="作者" width="120" />
              <el-table-column prop="view_count" label="浏览量" width="100" />
              <el-table-column prop="created_at" label="创建时间" width="180">
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button size="small" @click="handleEditContent(row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="handleDeleteContent(row)"
                    >删除</el-button
                  >
                </template>
              </el-table-column>
            </el-table>

            <!-- 分页组件 -->
            <div
              class="pagination-container"
              style="padding: 16px; text-align: center; border-top: 1px solid #e4e7ed"
            >
              <div style="margin-bottom: 10px; font-size: 14px; color: #333">
                显示第 {{ (currentPage - 1) * pageSize + 1 }} -
                {{ Math.min(currentPage * pageSize, total) }} 条，共 {{ total }} 条记录
              </div>
              <el-pagination
                v-model:current-page="currentPage"
                :page-size="pageSize"
                :total="total"
                :page-sizes="[10, 20, 50, 100]"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="
                  (size: number) => {
                    pageSize = size
                    currentPage = 1
                    loadContentItems()
                  }
                "
                @current-change="handlePageChange"
                :hide-on-single-page="false"
                background
                v-if="total > 0"
              />

              <!-- 简单分页导航（备选方案） -->
              <div
                v-if="total > pageSize"
                style="
                  margin-top: 15px;
                  text-align: center;
                  padding: 10px;
                  background: #f5f5f5;
                  border-radius: 4px;
                "
              >
                <el-button
                  :disabled="currentPage === 1"
                  @click="handlePageChange(currentPage - 1)"
                  size="small"
                >
                  上一页
                </el-button>
                <span style="margin: 0 15px; color: #666">
                  第 {{ currentPage }} 页，共 {{ Math.ceil(total / pageSize) }} 页
                </span>
                <el-button
                  :disabled="currentPage >= Math.ceil(total / pageSize)"
                  @click="handlePageChange(currentPage + 1)"
                  size="small"
                >
                  下一页
                </el-button>
              </div>

              <!-- 调试信息 -->
              <div style="margin-top: 10px; font-size: 12px; color: #666">
                总记录数: {{ total }}, 当前页: {{ currentPage }}, 每页显示: {{ pageSize }}
              </div>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="视频链接" name="videos">
          <div class="tab-content">
            <div class="toolbar">
              <el-button type="primary" @click="showAddVideoDialog = true">
                <el-icon><Plus /></el-icon>
                添加视频链接
              </el-button>
            </div>

            <el-table :data="videos" style="width: 100%" v-loading="videoLoading">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="title" label="标题" min-width="200" />
              <el-table-column
                prop="description"
                label="描述"
                min-width="200"
                show-overflow-tooltip
              />
              <el-table-column
                prop="video_url"
                label="视频链接"
                min-width="300"
                show-overflow-tooltip
              />
              <el-table-column prop="sort_order" label="排序" width="80" />
              <el-table-column prop="created_at" label="创建时间" width="180">
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button size="small" @click="handleEditVideo(row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="handleDeleteVideo(row)"
                    >删除</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <el-tab-pane label="书籍链接" name="books">
          <div class="tab-content">
            <div class="toolbar">
              <el-button type="primary" @click="showAddBookDialog = true">
                <el-icon><Plus /></el-icon>
                添加书籍链接
              </el-button>
            </div>

            <el-table :data="books" style="width: 100%" v-loading="bookLoading">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="title" label="标题" min-width="200" />
              <el-table-column prop="author" label="作者" width="120" />
              <el-table-column
                prop="description"
                label="描述"
                min-width="200"
                show-overflow-tooltip
              />
              <el-table-column
                prop="book_url"
                label="书籍链接"
                min-width="300"
                show-overflow-tooltip
              />
              <el-table-column prop="sort_order" label="排序" width="80" />
              <el-table-column prop="created_at" label="创建时间" width="180">
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button size="small" @click="handleEditBook(row)">编辑</el-button>
                  <el-button size="small" type="danger" @click="handleDeleteBook(row)"
                    >删除</el-button
                  >
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <!-- 添加/编辑知识内容对话框 -->
    <el-dialog
      v-model="showAddContentDialog"
      :title="editingContent ? '编辑知识内容' : '添加知识内容'"
      width="60%"
    >
      <el-form :model="contentForm" :rules="contentRules" ref="contentFormRef" label-width="100px">
        <el-form-item label="分类" prop="category_id">
          <el-select v-model="contentForm.category_id" placeholder="选择分类" style="width: 100%">
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="contentForm.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input
            v-model="contentForm.content"
            type="textarea"
            :rows="6"
            placeholder="请输入内容"
          />
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="contentForm.author" placeholder="请输入作者" />
        </el-form-item>
        <el-form-item label="内容类型" prop="content_type">
          <el-select
            v-model="contentForm.content_type"
            placeholder="选择内容类型"
            style="width: 100%"
          >
            <el-option label="文档" value="document" />
            <el-option label="书籍" value="book" />
            <el-option label="视频" value="video" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddContentDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSaveContent">保存</el-button>
      </template>
    </el-dialog>

    <!-- 添加/编辑视频链接对话框 -->
    <el-dialog
      v-model="showAddVideoDialog"
      :title="editingVideo ? '编辑视频链接' : '添加视频链接'"
      width="60%"
    >
      <el-form :model="videoForm" :rules="videoRules" ref="videoFormRef" label-width="100px">
        <el-form-item label="分类" prop="category_id">
          <el-select v-model="videoForm.category_id" placeholder="选择分类" style="width: 100%">
            <el-option
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="标题" prop="title">
          <el-input v-model="videoForm.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="videoForm.description" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="视频链接" prop="video_url">
          <el-input v-model="videoForm.video_url" placeholder="请输入视频链接" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="videoForm.sort_order" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddVideoDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSaveVideo">保存</el-button>
      </template>
    </el-dialog>

    <!-- 添加/编辑书籍链接对话框 -->
    <el-dialog
      v-model="showAddBookDialog"
      :title="editingBook ? '编辑书籍链接' : '添加书籍链接'"
      width="60%"
    >
      <el-form :model="bookForm" :rules="bookRules" ref="bookFormRef" label-width="100px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="bookForm.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="作者" prop="author">
          <el-input v-model="bookForm.author" placeholder="请输入作者" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="bookForm.description" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="封面图片" prop="cover_url">
          <el-input v-model="bookForm.cover_url" placeholder="请输入封面图片路径" />
        </el-form-item>
        <el-form-item label="书籍链接" prop="book_url">
          <el-input v-model="bookForm.book_url" placeholder="请输入书籍链接" />
        </el-form-item>
        <el-form-item label="排序" prop="sort_order">
          <el-input-number v-model="bookForm.sort_order" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddBookDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSaveBook">保存</el-button>
      </template>
    </el-dialog>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import {
  getKnowledgeCategories,
  getKnowledgeItems,
  getVideoLinks,
  getBookLinks,
  createKnowledgeItem,
  updateKnowledgeItem,
  deleteKnowledgeItem,
  createVideoLink,
  updateVideoLink,
  deleteVideoLink,
  createBookLink,
  updateBookLink,
  deleteBookLink,
} from '@/api/knowledge'

// Props
const props = defineProps<{
  modelValue: boolean
}>()

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

// 响应式数据
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value),
})

const activeTab = ref('content')
const categories = ref<any[]>([])
const contentItems = ref<any[]>([])
const videos = ref<any[]>([])
const books = ref<any[]>([])

// 加载状态
const contentLoading = ref(false)
const videoLoading = ref(false)
const bookLoading = ref(false)

// 搜索
const contentSearchKeyword = ref('')
const filteredContent = computed(() => {
  return contentItems.value
})

// 处理搜索
const handleContentSearch = async () => {
  currentPage.value = 1
  await loadContentItems()
}

// 对话框状态
const showAddContentDialog = ref(false)
const showAddVideoDialog = ref(false)
const showAddBookDialog = ref(false)

// 编辑状态
const editingContent = ref<any>(null)
const editingVideo = ref<any>(null)
const editingBook = ref<any>(null)

// 表单数据
const contentForm = ref({
  category_id: 0,
  title: '',
  content: '',
  author: '',
  content_type: 'document',
})

const videoForm = ref({
  category_id: 0,
  title: '',
  description: '',
  video_url: '',
  sort_order: 0,
})

const bookForm = ref({
  title: '',
  author: '',
  description: '',
  cover_url: '',
  book_url: '',
  sort_order: 0,
})

// 表单验证规则
const contentRules = {
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }],
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }],
  author: [{ required: true, message: '请输入作者', trigger: 'blur' }],
  content_type: [{ required: true, message: '请选择内容类型', trigger: 'change' }],
}

const videoRules = {
  category_id: [{ required: true, message: '请选择分类', trigger: 'change' }],
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  video_url: [{ required: true, message: '请输入视频链接', trigger: 'blur' }],
}

const bookRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  book_url: [{ required: true, message: '请输入书籍链接', trigger: 'blur' }],
}

// 表单引用
const contentFormRef = ref()
const videoFormRef = ref()
const bookFormRef = ref()

// 方法
const handleClose = () => {
  visible.value = false
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 知识内容管理
const handleEditContent = (row: any) => {
  editingContent.value = row
  contentForm.value = { ...row }
  showAddContentDialog.value = true
}

const handleDeleteContent = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除这条知识内容吗？')

    await deleteKnowledgeItem(row.id)
    ElMessage.success('删除成功')
    await loadContentItems()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSaveContent = async () => {
  try {
    await contentFormRef.value.validate()

    if (editingContent.value) {
      await updateKnowledgeItem(editingContent.value.id, contentForm.value)
      ElMessage.success('更新成功')
    } else {
      await createKnowledgeItem(contentForm.value)
      ElMessage.success('添加成功')
    }

    showAddContentDialog.value = false
    editingContent.value = null
    contentForm.value = {
      category_id: 0,
      title: '',
      content: '',
      author: '',
      content_type: 'document',
    }
    await loadContentItems()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 视频管理
const handleEditVideo = (row: any) => {
  editingVideo.value = row
  videoForm.value = { ...row }
  showAddVideoDialog.value = true
}

const handleDeleteVideo = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除这个视频链接吗？')

    await deleteVideoLink(row.id)
    ElMessage.success('删除成功')
    await loadVideos()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSaveVideo = async () => {
  try {
    await videoFormRef.value.validate()

    if (editingVideo.value) {
      await updateVideoLink(editingVideo.value.id, videoForm.value)
      ElMessage.success('更新成功')
    } else {
      await createVideoLink(videoForm.value)
      ElMessage.success('添加成功')
    }

    showAddVideoDialog.value = false
    editingVideo.value = null
    videoForm.value = {
      category_id: 0,
      title: '',
      description: '',
      video_url: '',
      sort_order: 0,
    }
    await loadVideos()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 书籍管理
const handleEditBook = (row: any) => {
  editingBook.value = row
  bookForm.value = { ...row }
  showAddBookDialog.value = true
}

const handleDeleteBook = async (row: any) => {
  try {
    await ElMessageBox.confirm('确定要删除这个书籍链接吗？')

    await deleteBookLink(row.id)
    ElMessage.success('删除成功')
    await loadBooks()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSaveBook = async () => {
  try {
    await bookFormRef.value.validate()

    if (editingBook.value) {
      await updateBookLink(editingBook.value.id, bookForm.value)
      ElMessage.success('更新成功')
    } else {
      await createBookLink(bookForm.value)
      ElMessage.success('添加成功')
    }

    showAddBookDialog.value = false
    editingBook.value = null
    bookForm.value = {
      title: '',
      author: '',
      description: '',
      cover_url: '',
      book_url: '',
      sort_order: 0,
    }
    await loadBooks()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 加载数据
const loadCategories = async () => {
  try {
    const response = await getKnowledgeCategories()
    categories.value = response.data
  } catch (error) {
    ElMessage.error('加载分类失败')
  }
}

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const loadContentItems = async () => {
  contentLoading.value = true
  try {
    const params: any = {
      page: currentPage.value,
      page_size: pageSize.value,
    }

    // 如果有搜索关键词，添加到参数中
    if (contentSearchKeyword.value.trim()) {
      params.search = contentSearchKeyword.value
    }

    const response = await getKnowledgeItems(params)
    contentItems.value = response.data.records
    total.value = response.data.total
    console.log('Loaded content items:', {
      records: response.data.records.length,
      total: response.data.total,
      currentPage: currentPage.value,
      pageSize: pageSize.value,
    })
    console.log('Total records:', response.data.total)
    console.log('Current page:', currentPage.value)
    console.log('Page size:', pageSize.value)
  } catch (error) {
    ElMessage.error('加载知识内容失败')
  } finally {
    contentLoading.value = false
  }
}

const handlePageChange = async (page: number) => {
  currentPage.value = page
  await loadContentItems()
}

const loadVideos = async () => {
  videoLoading.value = true
  try {
    const response = await getVideoLinks()
    videos.value = response.data
  } catch (error) {
    ElMessage.error('加载视频失败')
  } finally {
    videoLoading.value = false
  }
}

const loadBooks = async () => {
  bookLoading.value = true
  try {
    const response = await getBookLinks()
    books.value = response.data
  } catch (error) {
    ElMessage.error('加载书籍失败')
  } finally {
    bookLoading.value = false
  }
}

// 监听对话框打开
watch(visible, (newVal) => {
  if (newVal) {
    loadCategories()
    loadContentItems()
    loadVideos()
    loadBooks()
  }
})
</script>

<style scoped>
.knowledge-manager-dialog :deep(.el-dialog__body) {
  padding: 0;
}

.knowledge-manager {
  height: 70vh;
  overflow: hidden;
}

.knowledge-tabs {
  height: 100%;
}

.knowledge-tabs :deep(.el-tabs__content) {
  height: calc(100% - 55px);
  overflow: auto;
}

.tab-content {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: auto;
}

.toolbar {
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e4e7ed;
}

.toolbar .el-table {
  flex: 1;
  overflow: auto;
}

.pagination-container {
  border-top: 1px solid #e4e7ed;
  background: #fafafa;
  position: relative;
  z-index: 10;
}
</style>
