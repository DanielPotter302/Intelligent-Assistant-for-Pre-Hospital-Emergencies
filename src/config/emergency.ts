export interface EmergencyScenario {
  id: string
  title: string
  description: string
  icon: string
  color: string
  prompts: string[]
  quickActions: Array<{
    id: string
    title: string
    description: string
    icon: string
    color: string
  }>
}

export const emergencyScenarios: Record<string, EmergencyScenario> = {
  equipment: {
    id: 'equipment',
    title: '常用医疗设备操作',
    description: 'AED、血压计等医疗设备使用指导',
    icon: 'fas fa-medkit',
    color: 'blue',
    prompts: [
      '需要了解哪种医疗设备的使用方法？',
      '例如：AED（自动体外除颤器）、血压计、血糖仪等设备的使用方法'
    ],
    quickActions: [
      {
        id: 'aed',
        title: 'AED使用',
        description: '自动体外除颤器操作指导',
        icon: 'fas fa-heartbeat',
        color: 'red'
      },
      {
        id: 'blood-pressure',
        title: '血压测量',
        description: '血压计使用方法',
        icon: 'fas fa-tachometer-alt',
        color: 'blue'
      },
      {
        id: 'glucose',
        title: '血糖检测',
        description: '血糖仪使用指导',
        icon: 'fas fa-tint',
        color: 'green'
      }
    ]
  },
  firstAid: {
    id: 'firstAid',
    title: '紧急救护步骤',
    description: '心肺复苏、止血等急救操作指导',
    icon: 'fas fa-heartbeat',
    color: 'red',
    prompts: [
      '需要哪种急救操作的指导？',
      '例如：心肺复苏、止血、包扎、骨折固定等急救操作步骤'
    ],
    quickActions: [
      {
        id: 'cpr',
        title: '心肺复苏',
        description: 'CPR操作步骤指导',
        icon: 'fas fa-heart',
        color: 'red'
      },
      {
        id: 'bleeding',
        title: '止血处理',
        description: '伤口止血方法',
        icon: 'fas fa-band-aid',
        color: 'orange'
      },
      {
        id: 'fracture',
        title: '骨折固定',
        description: '骨折临时固定方法',
        icon: 'fas fa-bone',
        color: 'purple'
      }
    ]
  },
  location: {
    id: 'location',
    title: '医疗设备定位',
    description: '查找最近的AED、医疗设备位置',
    icon: 'fas fa-map-marker-alt',
    color: 'green',
    prompts: [
      '需要查找哪种医疗设备？',
      '例如：最近的AED位置、医疗器械柜位置等'
    ],
    quickActions: [
      {
        id: 'aed-location',
        title: 'AED位置',
        description: '查找最近的AED设备',
        icon: 'fas fa-heartbeat',
        color: 'red'
      },
      {
        id: 'first-aid-kit',
        title: '急救箱',
        description: '查找急救箱位置',
        icon: 'fas fa-medkit',
        color: 'blue'
      },
      {
        id: 'hospital',
        title: '医院位置',
        description: '查找最近的医院',
        icon: 'fas fa-hospital',
        color: 'green'
      }
    ]
  },
  emergency: {
    id: 'emergency',
    title: '现场应急处置',
    description: '快速描述现场情况，获取应急处置建议',
    icon: 'fas fa-ambulance',
    color: 'orange',
    prompts: [
      '请描述现场情况',
      '请详细描述：伤者状况、现场环境、已采取的措施等，我会提供专业的应急处置建议'
    ],
    quickActions: [
      {
        id: 'call-120',
        title: '拨打120',
        description: '立即拨打急救电话',
        icon: 'fas fa-phone',
        color: 'red'
      },
      {
        id: 'scene-assessment',
        title: '现场评估',
        description: '现场安全评估指导',
        icon: 'fas fa-shield-alt',
        color: 'yellow'
      },
      {
        id: 'patient-assessment',
        title: '伤者评估',
        description: '伤者状况评估方法',
        icon: 'fas fa-user-md',
        color: 'blue'
      }
    ]
  }
}

// 安全提示内容
export const safetyTips = [
  '在紧急情况下，请首先确保自身安全',
  '立即拨打120急救电话',
  '本指导仅供参考，不能替代专业医疗救助',
  '如有疑问，请咨询专业医护人员',
  '保持冷静，按照指导步骤操作',
  '注意观察伤者反应，及时调整措施'
]

// 常见问题模板
export const commonQuestions = {
  equipment: [
    'AED设备如何正确使用？',
    '血压计测量步骤是什么？',
    '血糖仪使用注意事项有哪些？'
  ],
  firstAid: [
    '成人CPR的正确步骤是什么？',
    '如何判断是否需要心肺复苏？',
    '止血的正确方法是什么？'
  ],
  location: [
    '最近的AED在哪里？',
    '如何快速找到医疗设备？',
    '医院的具体位置在哪里？'
  ],
  emergency: [
    '现场应该先做什么？',
    '如何判断伤者状况？',
    '等待救护车时应该注意什么？'
  ]
}

// 应急联系信息
export const emergencyContacts = {
  emergency: '120',
  police: '110',
  fire: '119',
  poison: '010-83132345', // 北京中毒急救中心
  mentalHealth: '010-82951332' // 北京心理危机干预热线
} 