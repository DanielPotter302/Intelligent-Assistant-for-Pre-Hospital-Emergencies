import request from '@/utils/request'
import type {
  ApiResponse,
  PaginatedResponse,
  TriageRequest,
  TriageResponse,
  TriageHistoryItem,
  CalculatorRequest,
  CalculatorResponse,
  CalculatorInfo,
} from '@/types/api'

// 重新导出类型以保持向后兼容
export type {
  PatientInfo,
  VitalSigns,
  SymptomInfo,
  TriageRequest as TriageInput,
  TriageResponse as AITriageResponse,
} from '@/types/api'

// AI分诊分析
export function analyzeTriageData(data: TriageRequest | any): Promise<ApiResponse<TriageResponse>> {
  return request.post('/api/triage/analyze', data)
}

// 获取分诊历史
export function getTriageHistory(params?: {
  page?: number
  pageSize?: number
  startDate?: string
  endDate?: string
}): Promise<ApiResponse<PaginatedResponse<TriageHistoryItem>>> {
  return request.get('/api/triage/history', { params })
}

// 医疗计算器
export function calculateMedicalScore(
  type: string,
  data: CalculatorRequest,
): Promise<ApiResponse<CalculatorResponse>> {
  return request.post(`/api/triage/calculator/${type}`, data)
}

// 获取计算器类型列表
export function getCalculatorTypes(): Promise<ApiResponse<CalculatorInfo[]>> {
  return request.get('/api/triage/calculators')
}

// 常见症状列表
export const getCommonSymptoms = (): string[] => {
  return [
    '胸痛',
    '呼吸困难',
    '腹痛',
    '头痛',
    '发热',
    '恶心呕吐',
    '昏迷',
    '抽搐',
    '创伤',
    '出血',
    '骨折疑似',
    '中毒',
    '过敏反应',
    '休克',
    '心悸',
    '咳嗽',
    '腰痛',
    '关节痛',
  ]
}

// 获取正常生命体征范围
export const getNormalVitalSigns = () => {
  return {
    heartRate: { min: 60, max: 100, unit: 'bpm' },
    bloodPressure: {
      systolic: { min: 90, max: 140, unit: 'mmHg' },
      diastolic: { min: 60, max: 90, unit: 'mmHg' },
    },
    respiratoryRate: { min: 12, max: 20, unit: '次/分' },
    temperature: { min: 36.0, max: 37.5, unit: '°C' },
    oxygenSaturation: { min: 95, max: 100, unit: '%' },
    glucoseLevel: { min: 3.9, max: 6.1, unit: 'mmol/L' },
  }
}

// 医疗计算器工具类
export class MedicalCalculators {
  // Glasgow昏迷评分
  static calculateGCS(
    eyeResponse: number,
    verbalResponse: number,
    motorResponse: number,
  ): {
    total: number
    interpretation: string
    riskLevel: string
  } {
    const total = eyeResponse + verbalResponse + motorResponse

    let interpretation = ''
    let riskLevel = ''

    if (total >= 13) {
      interpretation = '轻度意识障碍'
      riskLevel = 'low'
    } else if (total >= 9) {
      interpretation = '中度意识障碍'
      riskLevel = 'medium'
    } else {
      interpretation = '重度意识障碍'
      riskLevel = 'high'
    }

    return { total, interpretation, riskLevel }
  }

  // APACHE II评分（简化版）
  static calculateAPACHE(params: {
    temperature: number
    heartRate: number
    respiratoryRate: number
    bloodPressure: { systolic: number }
    oxygenation: number
    arterialPH: number
    sodium: number
    potassium: number
    creatinine: number
    hematocrit: number
    whiteBloodCells: number
    gcsScore: number
    age: number
    chronicHealth: boolean
  }): {
    total: number
    interpretation: string
    mortalityRisk: string
  } {
    // 这里是简化的APACHE II计算逻辑
    // 实际应用中需要完整的评分表
    let score = 0

    // 年龄评分
    if (params.age >= 75) score += 6
    else if (params.age >= 65) score += 5
    else if (params.age >= 55) score += 3
    else if (params.age >= 45) score += 2

    // GCS评分
    score += 15 - params.gcsScore

    // 慢性健康状况
    if (params.chronicHealth) score += 5

    let interpretation = ''
    let mortalityRisk = ''

    if (score >= 25) {
      interpretation = '极高风险'
      mortalityRisk = '>50%'
    } else if (score >= 15) {
      interpretation = '高风险'
      mortalityRisk = '25-50%'
    } else if (score >= 10) {
      interpretation = '中等风险'
      mortalityRisk = '10-25%'
    } else {
      interpretation = '低风险'
      mortalityRisk = '<10%'
    }

    return { total: score, interpretation, mortalityRisk }
  }

  // NEWS评分（国家早期预警评分）
  static calculateNEWS(params: {
    respiratoryRate: number
    oxygenSaturation: number
    temperature: number
    systolicBP: number
    heartRate: number
    consciousness: 'alert' | 'voice' | 'pain' | 'unresponsive'
    supplementalOxygen: boolean
  }): {
    total: number
    interpretation: string
    riskLevel: string
  } {
    let score = 0

    // 呼吸频率评分
    if (params.respiratoryRate <= 8) score += 3
    else if (params.respiratoryRate <= 11) score += 1
    else if (params.respiratoryRate <= 20) score += 0
    else if (params.respiratoryRate <= 24) score += 2
    else score += 3

    // 血氧饱和度评分
    if (params.oxygenSaturation <= 91) score += 3
    else if (params.oxygenSaturation <= 93) score += 2
    else if (params.oxygenSaturation <= 95) score += 1
    else score += 0

    // 体温评分
    if (params.temperature <= 35.0) score += 3
    else if (params.temperature <= 36.0) score += 1
    else if (params.temperature <= 38.0) score += 0
    else if (params.temperature <= 39.0) score += 1
    else score += 2

    // 收缩压评分
    if (params.systolicBP <= 90) score += 3
    else if (params.systolicBP <= 100) score += 2
    else if (params.systolicBP <= 110) score += 1
    else if (params.systolicBP <= 219) score += 0
    else score += 3

    // 心率评分
    if (params.heartRate <= 40) score += 3
    else if (params.heartRate <= 50) score += 1
    else if (params.heartRate <= 90) score += 0
    else if (params.heartRate <= 110) score += 1
    else if (params.heartRate <= 130) score += 2
    else score += 3

    // 意识状态评分
    if (params.consciousness !== 'alert') score += 3

    // 吸氧评分
    if (params.supplementalOxygen) score += 2

    let interpretation = ''
    let riskLevel = ''

    if (score >= 7) {
      interpretation = '高风险，需要紧急医疗干预'
      riskLevel = 'high'
    } else if (score >= 5) {
      interpretation = '中等风险，需要密切监护'
      riskLevel = 'medium'
    } else {
      interpretation = '低风险，常规监护'
      riskLevel = 'low'
    }

    return { total: score, interpretation, riskLevel }
  }

  // HEART评分（胸痛评估）
  static calculateHeartScore(
    history: number,
    ecg: number,
    age: number,
    riskFactors: number,
    troponin: number,
  ): {
    total: number
    interpretation: string
    riskLevel: string
  } {
    const total = history + ecg + age + riskFactors + troponin

    let interpretation = ''
    let riskLevel = ''

    if (total <= 3) {
      interpretation = '低风险，30天内主要心脏不良事件风险<2%'
      riskLevel = 'low'
    } else if (total <= 6) {
      interpretation = '中等风险，30天内主要心脏不良事件风险2-20%'
      riskLevel = 'medium'
    } else {
      interpretation = '高风险，30天内主要心脏不良事件风险>20%'
      riskLevel = 'high'
    }

    return { total, interpretation, riskLevel }
  }

  // RTS评分（修正创伤评分）
  static calculateRTS(
    systolicBP: number,
    respiratoryRate: number,
    gcsScore: number,
  ): {
    total: number
    interpretation: string
    riskLevel: string
  } {
    let bpScore = 0
    let rrScore = 0
    let gcsCodedValue = 0

    // 收缩压评分
    if (systolicBP >= 90) bpScore = 4
    else if (systolicBP >= 76) bpScore = 3
    else if (systolicBP >= 50) bpScore = 2
    else if (systolicBP >= 1) bpScore = 1
    else bpScore = 0

    // 呼吸频率评分
    if (respiratoryRate >= 10 && respiratoryRate <= 29) rrScore = 4
    else if (respiratoryRate >= 30) rrScore = 3
    else if (respiratoryRate >= 6) rrScore = 2
    else if (respiratoryRate >= 1) rrScore = 1
    else rrScore = 0

    // GCS评分转换
    if (gcsScore >= 13) gcsCodedValue = 4
    else if (gcsScore >= 9) gcsCodedValue = 3
    else if (gcsScore >= 6) gcsCodedValue = 2
    else if (gcsScore >= 4) gcsCodedValue = 1
    else gcsCodedValue = 0

    // RTS计算（加权）
    const total = 0.9368 * bpScore + 0.7326 * rrScore + 0.2908 * gcsCodedValue

    let interpretation = ''
    let riskLevel = ''

    if (total >= 7.8) {
      interpretation = '轻微创伤，存活率>95%'
      riskLevel = 'low'
    } else if (total >= 6.9) {
      interpretation = '中度创伤，存活率85-95%'
      riskLevel = 'medium'
    } else if (total >= 4.0) {
      interpretation = '重度创伤，存活率50-85%'
      riskLevel = 'high'
    } else {
      interpretation = '极重度创伤，存活率<50%'
      riskLevel = 'critical'
    }

    return { total: parseFloat(total.toFixed(2)), interpretation, riskLevel }
  }

  // 儿童药物剂量计算
  static calculatePediatricDose(
    weight: number,
    dosePerKg: number,
  ): {
    totalDose: number
    interpretation: string
  } {
    const totalDose = weight * dosePerKg

    return {
      totalDose: parseFloat(totalDose.toFixed(2)),
      interpretation: `体重${weight}kg，按${dosePerKg}mg/kg计算，总剂量为${totalDose.toFixed(2)}mg`,
    }
  }

  // 体表面积计算（BSA）
  static calculateBSA(weight: number, height: number): number {
    // 使用Mosteller公式：BSA = √((height × weight) / 3600)
    return Math.sqrt((height * weight) / 3600)
  }
}
