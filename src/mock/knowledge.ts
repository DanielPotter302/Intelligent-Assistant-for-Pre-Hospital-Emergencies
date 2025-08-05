// 知识库类别数据
export const categories = [
  {
    id: 1,
    name: '家庭院前医疗',
    description: '家庭场景下常见急救知识',
    children: [
      {
        id: 11,
        name: '心肺复苏实战指南',
        description: '标准CPR操作流程'
      },
      {
        id: 12,
        name: '家庭急救箱配置',
        description: '必备药品和器材'
      }
    ]
  },
  {
    id: 2,
    name: '户外院前医疗',
    description: '野外/户外场景的院前急救',
    children: [
      {
        id: 21,
        name: '野外创伤处理',
        description: '常见外伤处理方法'
      },
      {
        id: 22,
        name: '高原急救指南',
        description: '高原病预防与处理'
      }
    ]
  },
  {
    id: 3,
    name: '公共场所应急',
    description: '公共场所常见意外处理',
    children: []
  },
  {
    id: 4,
    name: '特殊人群',
    description: '老人、儿童等特殊人群的急救',
    children: []
  },
  {
    id: 5,
    name: '常见急症处理',
    description: '常见急症的识别与处理',
    children: []
  }
]

// 书籍数据
export const books = [
  {
    id: 1,
    categoryId: 1,
    title: '心肺复苏实战指南',
    author: '急救医学专家团队',
    coverUrl: 'https://images.unsplash.com/photo-1505751172876-fa1923c5c528?q=80&w=200',
    publishedAt: '2023-05-15',
    description: '详细介绍心肺复苏的标准流程和操作要点，包含大量实践案例和图解说明。'
  },
  {
    id: 2,
    categoryId: 1,
    title: '家庭急救箱配置指南',
    author: '院前急救专家组',
    coverUrl: 'https://images.unsplash.com/photo-1603398938378-e54eab446dde?q=80&w=200',
    publishedAt: '2023-06-20',
    description: '专业指导家庭急救物品的选择和配置，确保急救物品的完整性和有效性。'
  },
  {
    id: 3,
    categoryId: 2,
    title: '户外意外伤害处理手册',
    author: '野外救援专家组',
    coverUrl: 'https://images.unsplash.com/photo-1579684385127-1ef15d508118?q=80&w=200',
    publishedAt: '2023-07-10',
    description: '针对户外运动中常见的意外伤害，提供专业的现场处理方法和注意事项。'
  },
  {
    id: 4,
    categoryId: 3,
    title: '公共场所急救指南',
    author: '公共卫生应急专家组',
    coverUrl: 'https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b?q=80&w=200',
    publishedAt: '2023-08-01',
    description: '面向公共场所的急救知识和技能，包括突发事件的应对和人群疏散。'
  },
  {
    id: 5,
    categoryId: 4,
    title: '特殊人群急救手册',
    author: '专科医疗团队',
    coverUrl: 'https://images.unsplash.com/photo-1576091160550-2173dba999ef?q=80&w=200',
    publishedAt: '2023-08-15',
    description: '针对老人、儿童、孕妇等特殊人群的急救方法，包含特殊情况下的处理原则。'
  },
  {
    id: 6,
    categoryId: 5,
    title: '常见急症处理指南',
    author: '急诊科专家组',
    coverUrl: 'https://images.unsplash.com/photo-1631815589968-fdb09a223b1e?q=80&w=200',
    publishedAt: '2023-09-01',
    description: '详细介绍各类常见急症的识别和处理方法，帮助快速应对紧急情况。'
  }
]

// 章节数据
export const chapters = [
  {
    id: 1,
    bookId: 1,
    title: '1. 基础概念',
    content: `
      <h1 class="text-2xl font-bold mb-4">第1章 心肺复苏基础概念</h1>
      
      <p class="text-lg leading-relaxed mb-4">
        心肺复苏（Cardiopulmonary Resuscitation, CPR）是一种紧急救生程序，用于在心脏骤停时维持受害者的血液循环和氧气供应。本章将介绍心肺复苏的基本概念、适应症和操作原则。
      </p>

      <h2 class="text-xl font-bold mt-6 mb-3">1.1 心肺复苏的定义</h2>
      <p class="leading-relaxed mb-4">
        心肺复苏是一系列挽救心跳骤停患者生命的紧急医疗措施，包括胸外按压、开放气道和人工呼吸。这些措施旨在维持大脑和其他重要器官的血液灌注和氧气供应，直到专业医疗人员到达并提供更高级的生命支持。
      </p>

      <div class="bg-primary/5 border-l-4 border-primary p-4 my-6 rounded-r-md">
        <h4 class="font-semibold text-primary mb-2">重要提示</h4>
        <p class="text-sm">
          即使是未经专业训练的人员，也可以通过单纯的胸外按压（无需人工呼吸）来实施心肺复苏，这被称为"Hands-Only CPR"。研究表明，这种简化版的CPR在心脏骤停的最初几分钟内同样有效。
        </p>
      </div>
    `,
    depthLevel: 1,
    sortOrder: 1
  },
  {
    id: 2,
    bookId: 1,
    title: '2. 操作流程',
    content: `
      <h1 class="text-2xl font-bold mb-4">第2章 心肺复苏操作流程</h1>
      
      <p class="text-lg leading-relaxed mb-4">
        高质量的心肺复苏操作是提高患者生存率的关键。本章将详细介绍心肺复苏的标准操作流程和关键步骤。
      </p>

      <h2 class="text-xl font-bold mt-6 mb-3">2.1 实施步骤</h2>
      <ol class="list-decimal pl-6 space-y-4">
        <li>确认现场安全，避免施救者也受到伤害</li>
        <li>快速评估患者意识和呼吸状态</li>
        <li>立即呼叫急救电话（120）</li>
        <li>开始胸外按压：
          <ul class="list-disc pl-6 mt-2">
            <li>按压位置：胸骨下半部</li>
            <li>按压频率：100-120次/分钟</li>
            <li>按压深度：5-6厘米</li>
          </ul>
        </li>
      </ol>
    `,
    depthLevel: 1,
    sortOrder: 2
  },
  {
    id: 3,
    bookId: 1,
    title: '3. 注意事项',
    content: '实施CPR时的注意事项...',
    depthLevel: 1,
    sortOrder: 3
  },
  {
    id: 4,
    bookId: 1,
    title: '4. 常见错误',
    content: '常见的CPR操作错误...',
    depthLevel: 1,
    sortOrder: 4
  },
  {
    id: 5,
    bookId: 2,
    title: '1. 基础药品配置',
    content: '家庭急救箱基础药品的配置说明...',
    depthLevel: 1,
    sortOrder: 1
  },
  {
    id: 6,
    bookId: 2,
    title: '2. 常用器材配置',
    content: '家庭急救箱常用器材的配置说明...',
    depthLevel: 1,
    sortOrder: 2
  }
]

// 视频数据
export const videos = [
  {
    id: 1,
    categoryId: 1,
    title: '心肺复苏实操演示',
    thumbnailUrl: 'https://picsum.photos/400/200',
    videoUrl: 'https://example.com/video1.mp4',
    description: '专业医护人员详细演示心肺复苏各关键步骤...',
    durationSec: 600,
    uploadedAt: '2023-07-01'
  },
  {
    id: 2,
    categoryId: 1,
    title: 'AED设备使用方法教学',
    thumbnailUrl: 'https://picsum.photos/400/200',
    videoUrl: 'https://example.com/video2.mp4',
    description: '介绍AED自动体外除颤仪的正确操作要点...',
    durationSec: 480,
    uploadedAt: '2023-07-15'
  }
]

// 收藏数据
export const favorites = [
  {
    id: 1,
    resourceType: 'CHAPTER',
    resourceId: 1,
    title: '第1章 心肺复苏基础概念',
    collectedAt: '2024-01-15'
  },
  {
    id: 2,
    resourceType: 'VIDEO',
    resourceId: 1,
    title: '心肺复苏实操演示',
    collectedAt: '2024-01-16'
  }
] 