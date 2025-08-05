<!-- 价值与优势部分 -->
<template>
  <section class="py-20 bg-gray-50">
    <div class="container mx-auto px-4">
      <div class="text-center mb-16">
        <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">价值与优势</h2>
        <p class="text-gray-600 max-w-2xl mx-auto text-lg">
          我们的解决方案如何改变急救现状，带来真正的价值
        </p>
        <div class="w-20 h-1 bg-red-600 mx-auto mt-6"></div>
      </div>

      <div class="grid md:grid-cols-3 gap-8">
        <!-- 时间价值 -->
        <div class="bg-white p-8 rounded-xl shadow-md relative overflow-hidden transform transition-all duration-300 hover:-translate-y-2 hover:shadow-xl">
          <div class="absolute top-0 right-0 w-32 h-32 bg-red-50 rounded-full -mr-16 -mt-16"></div>
          <div class="relative">
            <div class="w-14 h-14 bg-red-100 rounded-lg flex items-center justify-center mb-6">
              <i class="fas fa-clock text-red-600 text-2xl"></i>
            </div>
            <h3 class="text-xl font-bold mb-4">黄金4分钟</h3>
            <p class="text-gray-600 mb-6">
              心搏骤停患者的黄金抢救时间仅为4分钟，每延迟1分钟，生存率下降7%-10%。我们的智能助手能在第一时间提供专业指导，最大限度利用黄金抢救窗口。
            </p>
            <div class="bg-red-50 p-4 rounded-lg">
              <p class="font-medium text-red-600">据统计，使用智能指导可使抢救成功率提升30%以上</p>
            </div>
          </div>
        </div>

        <!-- 医学指南背书 -->
        <div class="bg-white p-8 rounded-xl shadow-md relative overflow-hidden transform transition-all duration-300 hover:-translate-y-2 hover:shadow-xl">
          <div class="absolute top-0 right-0 w-32 h-32 bg-red-50 rounded-full -mr-16 -mt-16"></div>
          <div class="relative">
            <div class="w-14 h-14 bg-red-100 rounded-lg flex items-center justify-center mb-6">
              <i class="fas fa-award text-red-600 text-2xl"></i>
            </div>
            <h3 class="text-xl font-bold mb-4">权威指南背书</h3>
            <p class="text-gray-600 mb-6">
              严格遵循美国心脏协会(AHA)和欧洲复苏委员会(ERC)2025年最新指南，确保所有急救建议的专业性和时效性，让每一步操作都有权威依据。
            </p>
            <div class="flex flex-wrap gap-3 mt-4">
              <span class="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full">AHA 2025</span>
              <span class="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full">ERC 2025</span>
              <span class="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full">国际复苏指南</span>
            </div>
          </div>
        </div>

        <!-- 数据安全 -->
        <div class="bg-white p-8 rounded-xl shadow-md relative overflow-hidden transform transition-all duration-300 hover:-translate-y-2 hover:shadow-xl">
          <div class="absolute top-0 right-0 w-32 h-32 bg-red-50 rounded-full -mr-16 -mt-16"></div>
          <div class="relative">
            <div class="w-14 h-14 bg-red-100 rounded-lg flex items-center justify-center mb-6">
              <i class="fas fa-shield-alt text-red-600 text-2xl"></i>
            </div>
            <h3 class="text-xl font-bold mb-4">数据安全与隐私</h3>
            <p class="text-gray-600 mb-6">
              所有数据优先在本地加密存储，必要时才进行匿名化处理后上传。严格遵守医疗数据安全标准和隐私保护法规，确保用户信息安全。
            </p>
            <div class="flex flex-wrap gap-3 mt-4">
              <span class="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full">本地加密</span>
              <span class="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full">隐私合规</span>
              <span class="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full">数据脱敏</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
// 移除所有 API 调用相关的代码，因为我们使用静态内容
</script>

<style scoped>
.container {
  max-width: 1280px;
}
</style> 