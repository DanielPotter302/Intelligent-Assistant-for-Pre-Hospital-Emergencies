<!-- 工作流程部分 -->
<template>
  <section class="py-20 bg-white">
    <div class="container mx-auto px-4">
      <div class="text-center mb-16">
        <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">工作流程</h2>
        <p class="text-gray-600 max-w-2xl mx-auto text-lg">
          智能协同，无缝衔接，确保急救过程高效准确
        </p>
        <div class="w-20 h-1 bg-red-600 mx-auto mt-6"></div>
      </div>

      <div class="relative max-w-4xl mx-auto">
        <!-- 时间线 -->
        <div class="absolute left-1/2 transform -translate-x-1/2 h-full w-0.5 bg-red-200"></div>

        <!-- 步骤1：端侧采集 -->
        <div class="relative mb-16">
          <div class="flex flex-col md:flex-row items-center">
            <div class="md:w-1/2 md:pr-12 md:text-right mb-6 md:mb-0">
              <h3 class="text-xl font-bold mb-2">端侧采集</h3>
              <p class="text-gray-600">通过多模态输入（语音、图像等）收集现场信息和伤者状况</p>
            </div>
            <div class="w-14 h-14 rounded-full bg-red-600 flex items-center justify-center text-white font-bold text-xl z-10 shadow-lg">
              1
            </div>
            <div class="md:w-1/2 md:pl-12"></div>
          </div>
        </div>

        <!-- 步骤2：离线推理 -->
        <div class="relative mb-16">
          <div class="flex flex-col md:flex-row items-center">
            <div class="md:w-1/2 md:pr-12"></div>
            <div class="w-14 h-14 rounded-full bg-red-600 flex items-center justify-center text-white font-bold text-xl z-10 shadow-lg">
              2
            </div>
            <div class="md:w-1/2 md:pl-12">
              <h3 class="text-xl font-bold mb-2">离线推理</h3>
              <p class="text-gray-600">本地小模型实时分析处理信息，提供初步急救指导和建议</p>
            </div>
          </div>
        </div>

        <!-- 步骤3：网络检测 -->
        <div class="relative mb-16">
          <div class="flex flex-col md:flex-row items-center">
            <div class="md:w-1/2 md:pr-12 md:text-right mb-6 md:mb-0">
              <h3 class="text-xl font-bold mb-2">网络检测</h3>
              <p class="text-gray-600">自动检测网络连接状态，判断是否可以进行云端协同</p>
            </div>
            <div class="w-14 h-14 rounded-full bg-red-600 flex items-center justify-center text-white font-bold text-xl z-10 shadow-lg">
              3
            </div>
            <div class="md:w-1/2 md:pl-12"></div>
          </div>
        </div>

        <!-- 步骤4：云端增强 -->
        <div class="relative mb-16">
          <div class="flex flex-col md:flex-row items-center">
            <div class="md:w-1/2 md:pr-12"></div>
            <div class="w-14 h-14 rounded-full bg-red-600 flex items-center justify-center text-white font-bold text-xl z-10 shadow-lg">
              4
            </div>
            <div class="md:w-1/2 md:pl-12">
              <h3 class="text-xl font-bold mb-2">云端增强</h3>
              <p class="text-gray-600">联网时同步数据至云端，利用大模型提供更精准的分析和建议</p>
            </div>
          </div>
        </div>

        <!-- 步骤5：结果反馈 -->
        <div class="relative">
          <div class="flex flex-col md:flex-row items-center">
            <div class="md:w-1/2 md:pr-12 md:text-right mb-6 md:mb-0">
              <h3 class="text-xl font-bold mb-2">结果反馈</h3>
              <p class="text-gray-600">整合分析结果，以直观易懂的方式呈现给用户，指导急救操作</p>
            </div>
            <div class="w-14 h-14 rounded-full bg-red-600 flex items-center justify-center text-white font-bold text-xl z-10 shadow-lg">
              5
            </div>
            <div class="md:w-1/2 md:pl-12"></div>
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

@media screen and (max-width: 768px) {
  .flex-row,
  .flex-row-reverse {
    flex-direction: column !important;
    align-items: flex-start !important;
  }

  .w-1\/2 {
    width: 100% !important;
    padding: 0 !important;
    text-align: left !important;
    margin-bottom: 1rem;
  }

  .absolute.left-1\/2 {
    left: 2rem !important;
  }

  .w-14 {
    margin-left: 0 !important;
    margin-bottom: 1rem;
  }
}
</style> 