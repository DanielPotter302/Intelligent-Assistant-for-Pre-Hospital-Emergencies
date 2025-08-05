<!-- 错误提示组件 -->
<template>
  <transition
    enter-active-class="transform transition duration-300 ease-out"
    enter-from-class="translate-y-2 opacity-0"
    enter-to-class="translate-y-0 opacity-100"
    leave-active-class="transform transition duration-200 ease-in"
    leave-from-class="translate-y-0 opacity-100"
    leave-to-class="translate-y-2 opacity-0"
  >
    <div 
      v-if="show"
      class="fixed bottom-20 left-1/2 transform -translate-x-1/2 bg-danger/90 text-white px-4 py-2 rounded-lg shadow-lg flex items-center space-x-2 z-50"
    >
      <i class="fa fa-exclamation-circle"></i>
      <span>{{ message }}</span>
    </div>
  </transition>
</template>

<script setup lang="ts">
defineProps<{
  show: boolean
  message: string
}>()
</script> 