from typing import Dict, List
from app.schemas.triage import TriageRequest, TriageResponse
from app.services.ai_service import ai_service

class TriageService:
    def __init__(self):
        self.urgency_keywords = {
            "critical": ["心脏骤停", "呼吸停止", "大出血", "昏迷", "休克", "严重外伤"],
            "urgent": ["胸痛", "呼吸困难", "高热", "剧烈疼痛", "意识模糊", "骨折"],
            "semi_urgent": ["发热", "腹痛", "头痛", "恶心", "呕吐", "轻微外伤"],
            "non_urgent": ["轻微感冒", "皮疹", "轻微疼痛", "咨询"]
        }
    
    async def analyze_triage(self, triage_data: TriageRequest) -> TriageResponse:
        """AI分诊分析"""
        # 构建分诊提示
        prompt = self._build_triage_prompt(triage_data)
        
        # 获取AI分析
        ai_messages = [
            {
                "role": "user", 
                "content": prompt
            }
        ]
        
        try:
            # 使用分诊模式进行AI分析
            ai_response = await ai_service.chat_completion(ai_messages, mode="triage", temperature=0.3)
            return self._parse_ai_response(ai_response, triage_data)
        except Exception as e:
            # 如果AI分析失败，使用规则引擎
            return self._rule_based_triage(triage_data)
    
    async def analyze_triage_stream(self, triage_data: TriageRequest):
        """AI分诊分析（流式输出）"""
        # 构建分诊提示
        prompt = self._build_triage_prompt(triage_data)
        
        # 获取AI分析
        ai_messages = [
            {
                "role": "user", 
                "content": prompt
            }
        ]
        
        try:
            # 使用分诊模式进行流式AI分析
            async for chunk in ai_service.chat_completion_stream(ai_messages, mode="triage", temperature=0.3):
                yield chunk
        except Exception as e:
            # 如果AI分析失败，返回错误信息
            yield {
                "type": "error",
                "message": f"AI分析失败: {str(e)}"
            }
    
    def _build_triage_prompt(self, triage_data: TriageRequest) -> str:
        """构建分诊提示"""
        patient = triage_data.patient_info
        vitals = triage_data.vital_signs
        symptoms = triage_data.symptom_info
        
        prompt = f"""
患者信息：
- 姓名：{patient.name}
- 年龄：{patient.age}岁
- 性别：{patient.gender}
- 体重：{patient.weight or '未知'}kg
- 身高：{patient.height or '未知'}cm
- 过敏史：{', '.join(patient.allergies) if patient.allergies else '无'}
- 用药史：{', '.join(patient.medications) if patient.medications else '无'}
- 病史：{', '.join(patient.medical_history) if patient.medical_history else '无'}

生命体征：
- 心率：{vitals.heart_rate or '未测'}次/分
- 血压：{vitals.blood_pressure_systolic or '未测'}/{vitals.blood_pressure_diastolic or '未测'} mmHg
- 呼吸频率：{vitals.respiratory_rate or '未测'}次/分
- 体温：{vitals.temperature or '未测'}°C
- 血氧饱和度：{vitals.oxygen_saturation or '未测'}%
- 血糖：{vitals.blood_glucose or '未测'}mmol/L

症状信息：
- 主诉：{symptoms.chief_complaint}
- 症状：{', '.join(symptoms.symptoms) if symptoms.symptoms else '无'}
- 疼痛等级：{symptoms.pain_level or '未评估'}/10
- 症状持续时间：{symptoms.symptom_duration or '未知'}

请根据以上信息进行分诊分析，评估紧急程度（critical/urgent/semi_urgent/non_urgent）
并提供具体的处理建议。
"""
        return prompt
    
    def _parse_ai_response(self, ai_response: str, triage_data: TriageRequest) -> TriageResponse:
        """解析AI响应"""
        # 简单的关键词匹配来确定紧急程度
        urgency_level = "semi_urgent"  # 默认值
        
        if any(keyword in ai_response for keyword in ["危急", "紧急", "立即", "critical"]):
            urgency_level = "critical"
        elif any(keyword in ai_response for keyword in ["急诊", "尽快", "urgent"]):
            urgency_level = "urgent"
        elif any(keyword in ai_response for keyword in ["非紧急", "可等待", "non_urgent"]):
            urgency_level = "non_urgent"
        
        # 根据紧急程度设置优先级分数
        priority_scores = {
            "critical": 5,
            "urgent": 4,
            "semi_urgent": 3,
            "non_urgent": 2
        }
        
        # 提取建议行动
        recommended_actions = self._extract_recommendations(ai_response)
        
        return TriageResponse(
            urgency_level=urgency_level,
            priority_score=priority_scores[urgency_level],
            recommended_actions=recommended_actions,
            estimated_wait_time=self._get_estimated_wait_time(urgency_level),
            department_recommendation=self._get_department_recommendation(triage_data),
            additional_notes=ai_response
        )
    
    def _rule_based_triage(self, triage_data: TriageRequest) -> TriageResponse:
        """基于规则的分诊（备用方案）"""
        urgency_level = "semi_urgent"
        priority_score = 3
        
        # 检查生命体征异常
        vitals = triage_data.vital_signs
        if vitals.heart_rate and (vitals.heart_rate > 120 or vitals.heart_rate < 50):
            urgency_level = "urgent"
            priority_score = 4
        
        if vitals.blood_pressure_systolic and vitals.blood_pressure_systolic > 180:
            urgency_level = "urgent"
            priority_score = 4
        
        if vitals.temperature and vitals.temperature > 39.0:
            urgency_level = "urgent"
            priority_score = 4
        
        if vitals.oxygen_saturation and vitals.oxygen_saturation < 90:
            urgency_level = "critical"
            priority_score = 5
        
        # 检查症状关键词
        chief_complaint = triage_data.symptom_info.chief_complaint.lower()
        for level, keywords in self.urgency_keywords.items():
            if any(keyword in chief_complaint for keyword in keywords):
                urgency_level = level
                priority_score = {"critical": 5, "urgent": 4, "semi_urgent": 3, "non_urgent": 2}[level]
                break
        
        recommended_actions = self._get_default_recommendations(urgency_level)
        
        return TriageResponse(
            urgency_level=urgency_level,
            priority_score=priority_score,
            recommended_actions=recommended_actions,
            estimated_wait_time=self._get_estimated_wait_time(urgency_level),
            department_recommendation=self._get_department_recommendation(triage_data)
        )
    
    def _extract_recommendations(self, ai_response: str) -> List[str]:
        """从AI响应中提取建议"""
        # 简单的建议提取
        recommendations = []
        lines = ai_response.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '•')):
                recommendations.append(line)
        
        if not recommendations:
            recommendations = ["请根据分诊结果安排相应的医疗处理"]
        
        return recommendations[:5]  # 最多返回5条建议
    
    def _get_default_recommendations(self, urgency_level: str) -> List[str]:
        """获取默认建议"""
        recommendations = {
            "critical": [
                "立即启动急救程序",
                "监测生命体征",
                "准备急救设备",
                "联系专科医生",
                "考虑转院治疗"
            ],
            "urgent": [
                "尽快安排医生诊治",
                "密切监测患者状态",
                "准备必要的检查",
                "评估是否需要住院"
            ],
            "semi_urgent": [
                "安排医生诊治",
                "进行基础检查",
                "观察症状变化",
                "提供对症治疗"
            ],
            "non_urgent": [
                "安排普通门诊",
                "提供健康指导",
                "必要时复诊"
            ]
        }
        return recommendations.get(urgency_level, ["请咨询医生"])
    
    def _get_estimated_wait_time(self, urgency_level: str) -> str:
        """获取预估等待时间"""
        wait_times = {
            "critical": "立即处理",
            "urgent": "15-30分钟",
            "semi_urgent": "1-2小时",
            "non_urgent": "2-4小时"
        }
        return wait_times.get(urgency_level, "待定")
    
    def _get_department_recommendation(self, triage_data: TriageRequest) -> str:
        """获取科室建议"""
        chief_complaint = triage_data.symptom_info.chief_complaint.lower()
        
        if any(keyword in chief_complaint for keyword in ["胸痛", "心脏", "心悸"]):
            return "心内科"
        elif any(keyword in chief_complaint for keyword in ["呼吸", "咳嗽", "气喘"]):
            return "呼吸科"
        elif any(keyword in chief_complaint for keyword in ["腹痛", "胃痛", "消化"]):
            return "消化科"
        elif any(keyword in chief_complaint for keyword in ["头痛", "神经", "意识"]):
            return "神经科"
        elif any(keyword in chief_complaint for keyword in ["外伤", "骨折", "创伤"]):
            return "外科"
        else:
            return "急诊科"

# 创建全局分诊服务实例
triage_service = TriageService() 