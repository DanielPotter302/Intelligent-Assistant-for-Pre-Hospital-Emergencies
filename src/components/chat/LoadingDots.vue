<!-- 加载动画组件 -->
<template>
  <div class="flex space-x-1">
    <div 
      v-for="i in 3" 
      :key="i"
      class="w-2 h-2 bg-gray-400 rounded-full"
      :style="{
        animation: `bounce 0.6s infinite`,
        animationDelay: `${(i - 1) * 0.15}s`
      }"
    ></div>
  </div>
</template>

<style scoped>
@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}
</style> 