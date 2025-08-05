<!-- 页脚部分 -->
<template>
  <footer class="bg-gray-900 text-white py-12">
    <div class="container mx-auto px-4">
      <!-- 主要内容 -->
      <div class="flex flex-col md:flex-row justify-between items-center mb-8">
        <div class="mb-6 md:mb-0">
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center">
              <i class="fas fa-kit-medical text-red-600 text-xl"></i>
            </div>
            <span class="font-bold text-xl">院前应急智能助手</span>
          </div>
          <p class="text-gray-400 max-w-md">
            我们致力于通过人工智能技术，为院前急救提供专业、及时的智能指导，让生命救援从0分钟开始，挽救更多生命。
          </p>
        </div>

        <div class="flex space-x-6">
          <a 
            v-for="platform in socialLinks"
            :key="platform.icon"
            :href="platform.url"
            target="_blank"
            class="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center text-white hover:bg-red-600 hover:scale-110 transform transition-all duration-300 hover:shadow-lg hover:shadow-red-500/20"
          >
            <i :class="['fab', platform.icon]"></i>
          </a>
        </div>
      </div>

      <!-- 分隔线 -->
      <div class="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center">
        <p class="text-gray-500 text-sm mb-4 md:mb-0">© {{ currentYear }} 院前应急智能助手团队 版权所有</p>
        <div class="flex space-x-6">
          <a 
            v-for="link in footerLinks" 
            :key="link.text"
            :href="link.url"
            class="text-gray-500 hover:text-white transition-colors text-sm"
          >
            {{ link.text }}
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

const currentYear = computed(() => new Date().getFullYear());

const socialLinks = ref([
  { icon: 'fa-weixin', url: '#', title: '微信' },
  { icon: 'fa-qq', url: '#', title: 'QQ' },
  { icon: 'fa-github', url: '#', title: 'GitHub' },
  { icon: 'fa-envelope', url: '#', title: '邮箱' }
]);

const footerLinks = ref([
  { text: '隐私政策', url: '#' },
  { text: '使用条款', url: '#' },
  { text: '版本 v1.0.0', url: '#' }
]);
</script>

<style scoped>
.container {
  max-width: 1280px;
}
</style> 