<!-- Hero部分 -->
<template>
  <section class="hero relative min-h-[800px] flex items-center bg-gray-900 overflow-hidden">
    <!-- 背景遮罩和动态效果 -->
    <div class="absolute inset-0 bg-gradient-to-r from-gray-900/90 to-gray-900/70">
      <img 
        class="w-full h-full object-cover -z-10 opacity-60 scale-105 animate-slow-zoom" 
        src="@/assets/images/hero-bg.png" 
        alt="背景图片"
      />
    </div>
    
    <!-- 动态背景形状 -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-red-500/20 to-transparent rounded-full blur-3xl animate-blob"></div>
      <div class="absolute -bottom-1/2 -right-1/2 w-full h-full bg-gradient-to-tl from-blue-500/20 to-transparent rounded-full blur-3xl animate-blob animation-delay-2000"></div>
    </div>
    
    <div class="container mx-auto px-4 relative z-10">
      <div class="max-w-4xl">
        <h1 class="text-6xl md:text-7xl font-bold text-white mb-8 leading-tight animate-title-slide-up">
          院前应急<span class="text-red-500">智能助手</span>
        </h1>
        <p class="text-2xl md:text-3xl text-white/90 mb-12 leading-relaxed animate-text-slide-up">
          让生命救援从 <span class="text-red-500 font-semibold">0</span> 分钟开始
        </p>
        <div class="flex flex-wrap gap-6 animate-buttons-slide-up">
          <button 
            class="group px-8 py-4 bg-red-600 text-white text-lg rounded-xl hover:bg-red-700 transform hover:-translate-y-1 transition-all duration-300 shadow-lg hover:shadow-red-500/50 flex items-center space-x-2"
            @click="scrollToFeatures"
          >
            <span>了解功能</span>
            <i class="fa fa-arrow-right transition-transform group-hover:translate-x-1"></i>
          </button>
          <button 
            class="group px-8 py-4 bg-white/10 backdrop-blur-sm text-white text-lg rounded-xl hover:bg-white/20 transform hover:-translate-y-1 transition-all duration-300 shadow-lg hover:shadow-white/30 flex items-center space-x-2 border border-white/30"
            @click="scrollToContact"
          >
            <span>联系我们</span>
            <i class="fa fa-envelope transition-transform group-hover:translate-x-1"></i>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const scrollToFeatures = () => {
  document.getElementById('what-we-do')?.scrollIntoView({ behavior: 'smooth' });
};

const scrollToContact = () => {
  document.getElementById('contact')?.scrollIntoView({ behavior: 'smooth' });
};
</script>

<style scoped>
.hero {
  background-color: #1a202c;
}

@keyframes slow-zoom {
  from {
    transform: scale(1);
  }
  to {
    transform: scale(1.1);
  }
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

@keyframes buttons-slide-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-slow-zoom {
  animation: slow-zoom 20s ease-in-out infinite alternate;
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animate-title-slide-up {
  animation: title-slide-up 1s ease-out;
}

.animate-text-slide-up {
  animation: text-slide-up 1s ease-out 0.3s backwards;
}

.animate-buttons-slide-up {
  animation: buttons-slide-up 1s ease-out 0.6s backwards;
}
</style> 