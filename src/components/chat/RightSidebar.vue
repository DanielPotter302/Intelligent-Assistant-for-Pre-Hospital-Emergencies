<!-- 右侧参考栏组件 -->
<template>
  <aside id="rightSidebar" class="w-72 bg-light border-l border-gray-200 flex-shrink-0 hidden xl:block overflow-y-auto transition-all duration-300 ease-in-out">
    <!-- 引用文档 -->
    <div class="p-4 border-b border-gray-200">
      <h2 class="text-sm font-medium text-gray-500 mb-3">参考资料</h2>
      
      <div class="space-y-4">
        <div 
          v-for="ref in references" 
          :key="ref.id"
          :id="`ref-${ref.id}`"
          :class="[
            'p-3 rounded-lg border transition-colors',
            activeRefId === ref.id ? 'border-primary bg-primary/5' : 'border-gray-200 bg-gray-50'
          ]"
        >
          <h3 class="text-sm font-medium text-dark">{{ ref.title }}</h3>
          <p class="text-xs text-gray-600 mt-2 whitespace-pre-line">{{ ref.content }}</p>
        </div>
      </div>
    </div>
    
    <!-- 快捷指令 -->
    <div class="p-4">
      <h2 class="text-sm font-medium text-gray-500 mb-3">常用问题</h2>
      
      <div class="space-y-2">
        <button 
          v-for="question in quickQuestions" 
          :key="question"
          class="w-full text-left p-3 rounded-lg bg-gray-50 hover:bg-gray-100 text-sm text-gray-700 transition-colors text-balance ripple"
          @click="selectQuestion(question)"
        >
          {{ question }}
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits(['select-question'])

// 状态
const activeRefId = ref<string | null>(null)

interface Reference {
  id: string
  title: string
  content: string
}

// 引用数据
const references = ref<Reference[]>([
  {
    id: '1',
    title: '《家庭应急救护指南》第3章',
    content: '婴儿心肺复苏操作规范：\n1. 按压位置：两乳头连线中点正下方的胸骨处\n2. 按压深度：约4厘米（胸部厚度的1/3）\n3. 按压频率：每分钟100-120次\n4. 按压与通气比例：30:2（单人）或15:2（双人）'
  },
  {
    id: '2',
    title: '《院前急救手册》第5节',
    content: '儿科心肺复苏要点：\n婴儿胸外按压应使用两根手指（食指和中指），按压深度为4厘米左右，避免过度用力造成胸骨或内脏损伤。'
  }
])

// 快捷问题
const quickQuestions = [
  '如何判断气道阻塞？',
  '成人CPR的正确步骤是什么？',
  '止血的方法有哪些？',
  '骨折固定的基本原则',
  '烧烫伤的应急处理步骤'
]

// 方法
const selectQuestion = (question: string) => {
  emit('select-question', question)
}

// 暴露方法给父组件
defineExpose({
  setActiveReference: (refId: string) => {
    activeRefId.value = refId
    // 滚动到对应引用
    const refElement = document.getElementById(`ref-${refId}`)
    if (refElement) {
      refElement.scrollIntoView({ behavior: 'smooth', block: 'center' })
    }
  },
  updateReferences: (newRefs: Reference[]) => {
    references.value = newRefs
  }
})
</script>

<style scoped>
@media (max-width: 1280px) {
  #rightSidebar.fixed {
    top: 4rem !important; /* 确保在移动端时正确定位 */
  }
}

.ripple {
  position: relative;
  overflow: hidden;
}
.ripple:after {
  content: "";
  display: block;
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  background-image: radial-gradient(circle, #000 10%, transparent 10.01%);
  background-repeat: no-repeat;
  background-position: 50%;
  transform: scale(10, 10);
  opacity: 0;
  transition: transform .5s, opacity 1s;
}
.ripple:active:after {
  transform: scale(0, 0);
  opacity: .3;
  transition: 0s;
}
</style> 