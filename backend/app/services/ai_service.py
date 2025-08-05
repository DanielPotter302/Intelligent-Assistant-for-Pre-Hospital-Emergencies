from typing import List, Dict, Any, Optional, AsyncGenerator
import os
import json
import asyncio
from app.core.config import settings

class AIService:
    def __init__(self):
        # 使用配置中的API密钥
        self.api_key = settings.dashscope_api_key
        self.base_url = settings.openai_base_url
        self.has_api = bool(self.api_key)
        
        # 模型配置
        self.kb_model = settings.kb_model  # 知识库检索模型
        self.complex_model = settings.complex_model  # 复杂问答模型
    
    async def chat_completion_stream(
        self, 
        messages: List[Dict[str, str]], 
        mode: str = "kb",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """流式聊天完成 - 使用OpenAI兼容模式
        
        支持的模式：
        - kb: 知识库检索（不开启思考）
        - graph: 复杂问答（开启思考）
        - triage: 智能分诊（不开启思考）
        - emergency: 应急指导（不开启思考）
        """
        if not self.has_api:
            # 如果没有配置API密钥，返回模拟流式响应
            async for chunk in self._mock_stream_response(messages[-1]["content"], mode):
                yield chunk
            return
        
        try:
            # 导入OpenAI SDK
            from openai import OpenAI
            
            # 创建OpenAI客户端
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
            )
            
            # 选择模型和配置
            # 只有复杂问答模式开启思考功能
            model = self.complex_model if mode == "graph" else self.kb_model
            enable_thinking = mode == "graph"  # 只有复杂问答模式开启思考
            
            # 根据模式调整消息内容
            processed_messages = self._process_messages_for_mode(messages, mode)
            
            # 构建请求参数
            request_params = {
                "model": model,
                "messages": processed_messages,
                "stream": True,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            
            # 如果是复杂问答模式，开启思考
            if enable_thinking:
                request_params["extra_body"] = {"enable_thinking": True}
            
            # 调用OpenAI兼容API
            completion = client.chat.completions.create(**request_params)
            
            # 处理流式响应
            full_content = ""
            thinking_content = ""
            
            for chunk in completion:
                # 解析chunk数据
                chunk_dict = chunk.model_dump() if hasattr(chunk, 'model_dump') else chunk
                
                if 'choices' in chunk_dict and chunk_dict['choices']:
                    choice = chunk_dict['choices'][0]
                    delta = choice.get('delta', {})
                    
                    # 处理思考内容（reasoning_content）
                    if 'reasoning_content' in delta and delta['reasoning_content'] and enable_thinking:
                        reasoning_text = delta['reasoning_content']
                        thinking_content += reasoning_text
                        yield {
                            "type": "thinking",
                            "content": reasoning_text
                        }
                    
                    # 处理回复内容
                    if 'content' in delta and delta['content']:
                        content = delta['content']
                        
                        # 如果是第一次输出内容，发送开始信号
                        if not full_content:
                            yield {
                                "type": "answer_start",
                                "content": ""
                            }
                        
                        full_content += content
                        yield {
                            "type": "answer",
                            "content": content
                        }
                    
                    # 检查是否完成
                    finish_reason = choice.get('finish_reason')
                    if finish_reason == "stop":
                        yield {
                            "type": "done",
                            "content": full_content,
                            "reasoning": thinking_content if enable_thinking else None
                        }
                        break
                
                # 处理使用情况信息
                if 'usage' in chunk_dict and chunk_dict['usage']:
                    yield {
                        "type": "usage",
                        "data": chunk_dict['usage']
                    }
            
        except ImportError:
            print("OpenAI SDK未安装，使用模拟响应")
            async for chunk in self._mock_stream_response(messages[-1]["content"], mode):
                yield chunk
        except Exception as e:
            print(f"OpenAI API调用错误: {e}")
            # 如果API调用失败，返回错误信息
            yield {
                "type": "error",
                "message": f"API调用失败: {str(e)}"
            }
            # 然后返回模拟流式响应
            async for chunk in self._mock_stream_response(messages[-1]["content"], mode):
                yield chunk
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        mode: str = "kb",
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """非流式聊天完成（用于兼容性）"""
        full_response = ""
        async for chunk in self.chat_completion_stream(messages, mode, temperature, max_tokens):
            if chunk["type"] == "answer":
                full_response += chunk["content"]
            elif chunk["type"] == "done":
                return chunk["content"]
        return full_response
    
    async def _mock_stream_response(self, user_message: str, mode: str = "kb") -> AsyncGenerator[Dict[str, Any], None]:
        """模拟流式响应（当没有API密钥时使用）"""
        import asyncio
        
        # 生成模拟响应内容
        mock_content = self._generate_mock_content(user_message)
        
        # 模拟思考过程（仅在复杂问答模式下）
        if mode == "graph":
            thinking_text = "正在分析您的问题，考虑相关的医疗知识和急救流程..."
            for char in thinking_text:
                yield {
                    "type": "thinking",
                    "content": char
                }
                await asyncio.sleep(0.02)
        
        # 发送回答开始信号
        yield {
            "type": "answer_start",
            "content": ""
        }
        
        # 逐字符发送回答内容
        for char in mock_content:
            yield {
                "type": "answer",
                "content": char
            }
            await asyncio.sleep(0.03)
        
        # 发送完成信号
        yield {
            "type": "done",
            "content": mock_content,
            "reasoning": thinking_text if mode == "graph" else None
        }
    
    def _process_messages_for_mode(self, messages: List[Dict[str, str]], mode: str) -> List[Dict[str, str]]:
        """根据不同模式处理消息，添加合适的系统提示词"""
        processed_messages = messages.copy()
        
        # 如果第一条消息不是系统消息，或者需要替换系统消息
        if not processed_messages or processed_messages[0]["role"] != "system":
            # 插入系统消息
            system_prompt = self._get_system_prompt_for_mode(mode)
            processed_messages.insert(0, {"role": "system", "content": system_prompt})
        else:
            # 更新现有的系统消息
            system_prompt = self._get_system_prompt_for_mode(mode)
            processed_messages[0]["content"] = system_prompt
            
        return processed_messages
    
    def _get_system_prompt_for_mode(self, mode: str) -> str:
        """获取不同模式的系统提示词"""
        prompts = {
            "kb": """你是一个专业的院前急救知识助手。你的任务是：
1. 基于医疗急救知识库，为用户提供准确、专业的医疗指导
2. 回答关于急救操作、医疗设备使用、症状识别等问题
3. 提供清晰、易懂的步骤说明和注意事项
4. 在紧急情况下，优先给出关键的救命措施
5. 始终提醒用户在严重情况下立即寻求专业医疗帮助

请用专业但易懂的语言回答，确保信息准确可靠。""",

            "graph": """你是一个具有深度思考能力的院前急救专家。你需要：
1. 深入分析复杂的医疗急救问题
2. 考虑多种可能的情况和风险因素
3. 提供详细的分析过程和推理逻辑
4. 给出全面的处理方案和预防措施
5. 考虑不同环境和条件下的应对策略

请充分利用你的思考能力，为用户提供深入、全面的专业建议。""",

            "triage": """你是一个专业的医疗分诊AI助手。你的职责是：
1. 根据患者症状和生命体征进行紧急程度评估
2. 按照标准医疗分诊流程进行分类（Critical/Urgent/Semi-urgent/Non-urgent）
3. 提供明确的处理建议和时间要求
4. 识别潜在的危及生命的症状
5. 给出科学、客观的分诊结果

请严格按照医疗分诊标准，给出准确的评估结果。""",

            "emergency": """你是一个院前急救指导专家。你需要：
1. 针对紧急情况提供即时、有效的急救指导
2. 按照标准急救流程给出清晰的操作步骤
3. 强调安全第一，避免二次伤害
4. 提供关键的生命支持措施
5. 指导现场人员正确使用急救设备

请提供简洁明了、易于执行的急救指导，确保在紧急情况下能够快速理解和执行。"""
        }
        
        return prompts.get(mode, prompts["kb"])
    
    def _generate_mock_content(self, user_message: str) -> str:
        """生成模拟响应内容"""
        if "分诊" in user_message or "症状" in user_message or "患者信息" in user_message:
            if "胸痛" in user_message:
                return """### 分诊分析：

#### 1. 紧急程度评估：
- **初步分类**：**Urgent（紧急）**
- 胸痛可能是多种潜在严重疾病的症状（如心源性、肺栓塞、主动脉夹层等），需进一步评估以排除危及生命的病因。

#### 2. 处理建议：
**立即行动**：
1. **完善关键信息**：询问胸痛的具体特征、持续时间、伴随症状
2. **初步排查**：测量血氧饱和度和心电图
3. **紧急处理**：如怀疑心源性胸痛，保持患者静卧，吸氧，立即转运

**总结**：分诊级别为**Urgent**（需1小时内评估）"""
            else:
                return """### 分诊分析：

#### 1. 紧急程度评估：
- **初步分类**：**Semi-urgent（次紧急）**
- 根据症状描述，建议进一步评估以确定具体处理方案。

#### 2. 处理建议：
1. **详细评估**：完善症状描述和持续时间
2. **监测观察**：密切观察症状变化
3. **医疗处理**：安排医生诊治，进行必要检查

**总结**：分诊级别为**Semi-urgent**（建议2小时内处理）"""

        elif "急救" in user_message or "紧急" in user_message:
            return """紧急情况处理指导：

1. **确保现场安全**：首先确认环境安全，避免二次伤害
2. **评估患者状态**：快速检查意识、呼吸、脉搏
3. **基础生命支持**：
   - 如无呼吸：立即开始心肺复苏
   - 如有出血：采取止血措施
   - 保持气道通畅
4. **联系专业医疗**：立即拨打急救电话
5. **持续监护**：密切观察患者状态变化

记住：在专业医疗人员到达前，保持冷静并按照标准急救流程操作。"""

        else:
            return f"""感谢您的咨询。针对您的问题，我建议：

1. **详细评估**：请提供更多具体信息，如症状持续时间、严重程度等
2. **专业建议**：建议咨询专业医疗人员获得准确诊断
3. **预防措施**：注意观察症状变化，记录相关信息
4. **紧急情况**：如出现严重症状，请立即就医

如需更详细的指导，请提供更多具体信息。"""

# 创建全局AI服务实例
ai_service = AIService() 