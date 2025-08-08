<template>
  <div class="markdown-content" v-html="renderedContent"></div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { marked } from 'marked'

const props = defineProps<{
  content: string
}>()

// 配置marked
marked.setOptions({
  breaks: true, // 支持换行
  gfm: true, // 支持GitHub风格的Markdown
})

const renderedContent = computed(() => {
  if (!props.content) return ''

  try {
    // 使用同步版本的 marked.parse
    let htmlContent = marked.parse(props.content) as string

    // 调试信息（开发环境）
    if (import.meta.env.DEV) {
      console.log('Original content:', props.content)
      console.log('Parsed HTML:', htmlContent)
    }

    // 后处理：添加医疗相关的特殊格式支持
    // 处理警告标记 ⚠️
    htmlContent = htmlContent.replace(
      /⚠️\s*(.*?)(?=<\/p>|<br>|$)/g,
      '<div class="medical-warning">⚠️ $1</div>',
    )

    // 处理提示标记 💡
    htmlContent = htmlContent.replace(
      /💡\s*(.*?)(?=<\/p>|<br>|$)/g,
      '<div class="medical-tip">💡 $1</div>',
    )

    return htmlContent
  } catch (error) {
    console.error('Markdown parsing error:', error)
    return props.content // 如果解析失败，返回原文本
  }
})
</script>

<style scoped>
.markdown-content {
  @apply text-gray-700 leading-relaxed;
}

/* 标题样式 */
.markdown-content :deep(h1) {
  @apply text-2xl font-bold mb-4 mt-6 text-gray-800 border-b border-gray-200 pb-2;
}

.markdown-content :deep(h2) {
  @apply text-xl font-bold mb-3 mt-5 text-gray-800;
}

.markdown-content :deep(h3) {
  @apply text-lg font-semibold mb-2 mt-4 text-gray-800;
}

.markdown-content :deep(h4) {
  @apply text-base font-semibold mb-2 mt-3 text-gray-800;
}

/* 段落样式 */
.markdown-content :deep(p) {
  @apply mb-3 leading-relaxed;
}

/* 列表样式 */
.markdown-content :deep(ul) {
  @apply mb-3 pl-6 space-y-1;
}

.markdown-content :deep(ol) {
  @apply mb-3 pl-6 space-y-1;
}

.markdown-content :deep(li) {
  @apply leading-relaxed;
}

.markdown-content :deep(ul li) {
  @apply list-disc;
}

.markdown-content :deep(ol li) {
  @apply list-decimal;
}

/* 强调样式 */
.markdown-content :deep(strong) {
  @apply font-semibold text-gray-800;
}

.markdown-content :deep(em) {
  @apply italic;
}

/* 代码样式 */
.markdown-content :deep(code) {
  @apply bg-gray-100 text-gray-800 px-1 py-0.5 rounded text-sm font-mono;
}

.markdown-content :deep(pre) {
  @apply bg-gray-50 border border-gray-200 rounded-lg p-4 mb-3 overflow-x-auto;
}

.markdown-content :deep(pre code) {
  @apply bg-transparent p-0 text-sm;
}

/* 引用样式 */
.markdown-content :deep(blockquote) {
  @apply border-l-4 border-primary pl-4 py-2 mb-3 bg-gray-50 italic text-gray-600;
}

/* 表格样式 */
.markdown-content :deep(table) {
  @apply w-full border-collapse border border-gray-200 mb-3;
}

.markdown-content :deep(th) {
  @apply border border-gray-200 bg-gray-50 px-3 py-2 text-left font-semibold;
}

.markdown-content :deep(td) {
  @apply border border-gray-200 px-3 py-2;
}

/* 分割线样式 */
.markdown-content :deep(hr) {
  @apply border-0 border-t border-gray-200 my-6;
}

/* 链接样式 */
.markdown-content :deep(a) {
  @apply text-primary hover:text-blue-700 underline;
}

/* 医疗相关的特殊样式 */
.markdown-content :deep(.medical-warning) {
  @apply bg-red-50 border border-red-200 rounded-lg p-3 mb-3;
}

.markdown-content :deep(.medical-tip) {
  @apply bg-blue-50 border border-blue-200 rounded-lg p-3 mb-3;
}

.markdown-content :deep(.emergency-step) {
  @apply bg-yellow-50 border border-yellow-200 rounded-lg p-3 mb-2;
}

/* 数字列表的特殊样式 - 用于急救步骤 */
.markdown-content :deep(ol.emergency-steps) {
  @apply space-y-3 mb-4;
}

.markdown-content :deep(ol.emergency-steps li) {
  @apply bg-gray-50 border border-gray-200 rounded-lg p-3 font-medium;
}

/* 重要信息高亮 */
.markdown-content :deep(.highlight) {
  @apply bg-yellow-200 px-1 rounded;
}

/* 警告文本 */
.markdown-content :deep(.warning) {
  @apply text-red-600 font-semibold;
}

/* 成功/安全提示 */
.markdown-content :deep(.success) {
  @apply text-green-600 font-semibold;
}
</style>
