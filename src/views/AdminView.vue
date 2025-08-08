<template>
  <div class="admin-container">
    <div class="admin-content">
      <div class="admin-grid">
        <!-- 留言查询 -->
        <div class="admin-card">
          <div class="card-icon">
            <el-icon size="32"><Message /></el-icon>
          </div>
          <h3>留言查询</h3>
          <p>查看和管理用户提交的联系留言</p>
          <el-button type="primary" @click="showMessageManager = true">查看留言</el-button>
        </div>

        <!-- 知识库管理 -->
        <div class="admin-card">
          <div class="card-icon">
            <el-icon size="32"><Document /></el-icon>
          </div>
          <h3>知识库管理</h3>
          <p>管理知识库内容、视频链接和书籍链接</p>
          <el-button type="primary" @click="showKnowledgeManager = true">管理知识库</el-button>
        </div>

        <!-- 用户管理 -->
        <div class="admin-card">
          <div class="card-icon">
            <el-icon size="32"><User /></el-icon>
          </div>
          <h3>用户管理</h3>
          <p>管理系统用户，查看用户信息</p>
          <el-button type="primary" disabled>即将开放</el-button>
        </div>

        <!-- LLM配置管理 -->
        <div class="admin-card">
          <div class="card-icon">
            <el-icon size="32"><Setting /></el-icon>
          </div>
          <h3>LLM配置管理</h3>
          <p>管理大语言模型的API KEY和配置参数</p>
          <el-button type="primary" @click="showLLMConfigManager = true">配置管理</el-button>
        </div>

        <!-- 系统设置 -->
        <div class="admin-card">
          <div class="card-icon">
            <el-icon size="32"><Tools /></el-icon>
          </div>
          <h3>系统设置</h3>
          <p>配置系统参数和功能选项</p>
          <el-button type="primary" disabled>即将开放</el-button>
        </div>

        <!-- 数据统计 -->
        <div class="admin-card">
          <div class="card-icon">
            <el-icon size="32"><DataAnalysis /></el-icon>
          </div>
          <h3>数据统计</h3>
          <p>查看系统使用情况和统计数据</p>
          <el-button type="primary" disabled>即将开放</el-button>
        </div>
      </div>
    </div>

    <!-- 留言管理对话框 -->
    <MessageManager v-model="showMessageManager" />

    <!-- 知识库管理对话框 -->
    <KnowledgeManager v-model="showKnowledgeManager" />

    <!-- LLM配置管理对话框 -->
    <LLMConfigManager v-model="showLLMConfigManager" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { User, Setting, DataAnalysis, Message, Document, Tools } from '@element-plus/icons-vue'
import MessageManager from '@/components/admin/MessageManager.vue'
import KnowledgeManager from '@/components/admin/KnowledgeManager.vue'
import LLMConfigManager from '@/components/admin/LLMConfigManager.vue'

const showMessageManager = ref(false)
const showKnowledgeManager = ref(false)
const showLLMConfigManager = ref(false)
</script>

<style scoped>
.admin-container {
  min-height: calc(100vh - 64px);
  background: #f5f7fa;
  padding: 40px 24px 24px 24px;
  margin-top: 64px;
}

.admin-content {
  max-width: 1200px;
  margin: 0 auto;
}

.admin-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.admin-card {
  background: white;
  border-radius: 12px;
  padding: 32px 24px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.admin-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.card-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 64px;
  height: 64px;
  background: #f0f9ff;
  border-radius: 16px;
  margin: 0 auto 16px;
  color: #3b82f6;
}

.admin-card h3 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #1f2937;
}

.admin-card p {
  color: #6b7280;
  margin: 0 0 24px 0;
  line-height: 1.5;
}

.admin-card .el-button {
  width: 100%;
}
</style>
