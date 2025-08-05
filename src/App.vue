<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import Navbar from '@/components/layout/Navbar.vue'

const showBackToTop = ref(false)

const handleScroll = () => {
  showBackToTop.value = window.scrollY > 300
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <div class="app">
    <navbar />
    <router-view></router-view>

    <!-- 返回顶部按钮 -->
    <button
      class="back-to-top-btn"
      @click="scrollToTop"
      :class="{ show: showBackToTop }"
      aria-label="返回顶部"
    >
      <i class="fa fa-arrow-up"></i>
    </button>
  </div>
</template>

<style>
html {
  scroll-behavior: smooth;
  scroll-padding-top: 4rem;
  min-height: 100%;
}

body {
  font-family: 'Inter', 'Noto Sans SC', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  @apply text-gray-900;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  margin: 0;
}

.app {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.container {
  @apply w-full mx-auto px-4;
  max-width: 1280px;
}

.back-to-top-btn {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 3rem;
  height: 3rem;
  background-color: #dc2626;
  color: white;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  opacity: 0;
  visibility: hidden;
  transform: translateY(20px);
  z-index: 9999;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.back-to-top-btn:hover {
  background-color: #b91c1c;
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(220, 38, 38, 0.2);
}

.back-to-top-btn.show {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.back-to-top-btn i {
  font-size: 20px;
}

/* 确保 Font Awesome 图标正确显示 */
.fa {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1em;
  height: 1em;
  vertical-align: middle;
}
</style>
