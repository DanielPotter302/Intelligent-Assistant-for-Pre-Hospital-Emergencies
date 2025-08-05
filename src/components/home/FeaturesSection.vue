<!-- 功能总览部分 -->
<template>
  <section id="what-we-do" class="py-32 bg-white relative overflow-hidden">
    <!-- 背景装饰 -->
    <div class="absolute inset-0 bg-gradient-to-b from-gray-50 to-white"></div>
    <div class="absolute inset-0">
      <div class="absolute top-0 left-1/4 w-72 h-72 bg-red-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob"></div>
      <div class="absolute top-0 right-1/4 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-2000"></div>
      <div class="absolute -bottom-8 left-1/3 w-72 h-72 bg-green-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-blob animation-delay-4000"></div>
    </div>

    <div class="container mx-auto px-4 relative">
      <!-- 标题部分 -->
      <div class="text-center mb-20">
        <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6 animate-title-slide-up">
          我们能做什么？
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed animate-text-slide-up">
          集成前沿AI技术，为院前急救提供全方位智能支持，让救援更及时、更专业、更有效
        </p>
        <div class="w-24 h-1.5 bg-gradient-to-r from-red-500 to-red-600 mx-auto mt-8 rounded-full animate-scale-in"></div>
      </div>

      <!-- 功能卡片网格 -->
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- 功能卡片1：权威知识库问答 -->
        <div class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-500 transform hover:-translate-y-2 hover:bg-gradient-to-br hover:from-white hover:to-red-50 animate-card-slide-up animation-delay-[0ms]">
          <div class="w-16 h-16 bg-gradient-to-br from-red-500 to-red-600 rounded-xl flex items-center justify-center mb-6 transform group-hover:rotate-6 group-hover:scale-110 transition-all duration-500 shadow-lg">
            <i class="fa fa-book text-white text-2xl"></i>
          </div>
          <h3 class="text-xl font-bold mb-4 text-gray-900 group-hover:text-red-600 transition-colors">权威知识库问答</h3>
          <p class="text-gray-600 leading-relaxed">
            基于最新版AHA/ERC指南的专业知识库，实时解答急救相关问题，确保信息准确性。
          </p>
        </div>

        <!-- 功能卡片2：实时步骤指导 -->
        <div class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-500 transform hover:-translate-y-2 hover:bg-gradient-to-br hover:from-white hover:to-red-50 animate-card-slide-up animation-delay-[200ms]">
          <div class="w-16 h-16 bg-gradient-to-br from-red-500 to-red-600 rounded-xl flex items-center justify-center mb-6 transform group-hover:rotate-6 group-hover:scale-110 transition-all duration-500 shadow-lg">
            <i class="fa fa-list-ol text-white text-2xl"></i>
          </div>
          <h3 class="text-xl font-bold mb-4 text-gray-900 group-hover:text-red-600 transition-colors">实时步骤指导</h3>
          <p class="text-gray-600 leading-relaxed">
            通过语音和图文并茂的方式，清晰指导CPR、止血、包扎等急救操作，确保步骤正确。
          </p>
        </div>

        <!-- 功能卡片3：AI分诊与危急值评估 -->
        <div class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-500 transform hover:-translate-y-2 hover:bg-gradient-to-br hover:from-white hover:to-red-50 animate-card-slide-up animation-delay-[400ms]">
          <div class="w-16 h-16 bg-gradient-to-br from-red-500 to-red-600 rounded-xl flex items-center justify-center mb-6 transform group-hover:rotate-6 group-hover:scale-110 transition-all duration-500 shadow-lg">
            <i class="fa fa-heartbeat text-white text-2xl"></i>
          </div>
          <h3 class="text-xl font-bold mb-4 text-gray-900 group-hover:text-red-600 transition-colors">AI分诊与危急值评估</h3>
          <p class="text-gray-600 leading-relaxed">
            快速识别伤者危急情况并优先建议处理措施，帮助救援人员做出更明智的决策。
          </p>
        </div>

        <!-- 功能卡片4：多模态输入 -->
        <div class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-500 transform hover:-translate-y-2 hover:bg-gradient-to-br hover:from-white hover:to-red-50 animate-card-slide-up animation-delay-[600ms]">
          <div class="w-16 h-16 bg-gradient-to-br from-red-500 to-red-600 rounded-xl flex items-center justify-center mb-6 transform group-hover:rotate-6 group-hover:scale-110 transition-all duration-500 shadow-lg">
            <i class="fa fa-microphone text-white text-2xl"></i>
          </div>
          <h3 class="text-xl font-bold mb-4 text-gray-900 group-hover:text-red-600 transition-colors">多模态输入</h3>
          <p class="text-gray-600 leading-relaxed">
            支持语音、图像等多种输入方式，适应紧急情况下的操作需求，提高使用便捷性。
          </p>
        </div>

        <!-- 功能卡片5：离线小模型 + 云端大模型 -->
        <div class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-500 transform hover:-translate-y-2 hover:bg-gradient-to-br hover:from-white hover:to-red-50 animate-card-slide-up animation-delay-[800ms]">
          <div class="w-16 h-16 bg-gradient-to-br from-red-500 to-red-600 rounded-xl flex items-center justify-center mb-6 transform group-hover:rotate-6 group-hover:scale-110 transition-all duration-500 shadow-lg">
            <i class="fa fa-cloud-download text-white text-2xl"></i>
          </div>
          <h3 class="text-xl font-bold mb-4 text-gray-900 group-hover:text-red-600 transition-colors">离线小模型 + 云端大模型</h3>
          <p class="text-gray-600 leading-relaxed">
            端侧小模型保障离线运行，联网后自动同步云端大模型，获取更强大的分析能力。
          </p>
        </div>

        <!-- 功能卡片6：学习与演练模块 -->
        <div class="group bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-500 transform hover:-translate-y-2 hover:bg-gradient-to-br hover:from-white hover:to-red-50 animate-card-slide-up animation-delay-[1000ms]">
          <div class="w-16 h-16 bg-gradient-to-br from-red-500 to-red-600 rounded-xl flex items-center justify-center mb-6 transform group-hover:rotate-6 group-hover:scale-110 transition-all duration-500 shadow-lg">
            <i class="fa fa-graduation-cap text-white text-2xl"></i>
          </div>
          <h3 class="text-xl font-bold mb-4 text-gray-900 group-hover:text-red-600 transition-colors">学习与演练模块</h3>
          <p class="text-gray-600 leading-relaxed">
            提供场景化模拟训练，记录学习进度，帮助用户提升急救技能和应对紧急情况的能力。
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Feature {
  id: number;
  title: string;
  icon: string;
  description: string;
}

const features = ref<Feature[]>([
  {
    id: 1,
    title: '权威知识库问答',
    icon: 'fa-book',
    description: '基于最新版AHA/ERC指南的专业知识库，实时解答急救相关问题，确保信息准确性。'
  },
  {
    id: 2,
    title: '实时步骤指导',
    icon: 'fa-list-ol',
    description: '通过语音和图文并茂的方式，清晰指导CPR、止血、包扎等急救操作，确保步骤正确。'
  },
  {
    id: 3,
    title: 'AI分诊与危急值评估',
    icon: 'fa-heartbeat',
    description: '快速识别伤者危急情况并优先建议处理措施，帮助救援人员做出更明智的决策。'
  },
  {
    id: 4,
    title: '多模态输入',
    icon: 'fa-microphone',
    description: '支持语音、图像等多种输入方式，适应紧急情况下的操作需求，提高使用便捷性。'
  },
  {
    id: 5,
    title: '离线小模型 + 云端大模型',
    icon: 'fa-cloud-download',
    description: '端侧小模型保障离线运行，联网后自动同步云端大模型，获取更强大的分析能力。'
  },
  {
    id: 6,
    title: '学习与演练模块',
    icon: 'fa-graduation-cap',
    description: '提供场景化模拟训练，记录学习进度，帮助用户提升急救技能和应对紧急情况的能力。'
  }
]);
</script>

<style scoped>
.container {
  max-width: 1280px;
}

@keyframes blob {
  0% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30%, -20%) scale(1.1);
  }
  66% {
    transform: translate(-20%, 20%) scale(0.9);
  }
  100% {
    transform: translate(0, 0) scale(1);
  }
}

@keyframes title-slide-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes text-slide-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scale-in {
  from {
    transform: scaleX(0);
  }
  to {
    transform: scaleX(1);
  }
}

@keyframes card-slide-up {
  from {
    opacity: 0;
    transform: translateY(60px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

.animate-title-slide-up {
  animation: title-slide-up 1s ease-out;
}

.animate-text-slide-up {
  animation: text-slide-up 1s ease-out 0.3s backwards;
}

.animate-scale-in {
  animation: scale-in 1s ease-out 0.6s backwards;
}

.animate-card-slide-up {
  animation: card-slide-up 1s ease-out backwards;
}

.animation-delay-\[200ms\] {
  animation-delay: 200ms;
}

.animation-delay-\[400ms\] {
  animation-delay: 400ms;
}

.animation-delay-\[600ms\] {
  animation-delay: 600ms;
}

.animation-delay-\[800ms\] {
  animation-delay: 800ms;
}

.animation-delay-\[1000ms\] {
  animation-delay: 1000ms;
}
</style> 