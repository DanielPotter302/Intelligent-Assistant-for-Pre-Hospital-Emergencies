from typing import List, Dict, Any, Optional, AsyncGenerator
import os
import json
import asyncio
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.llm_config import LLMConfig

class AIService:
    def __init__(self):
        # 默认配置（作为后备）
        self.default_api_key = settings.dashscope_api_key
        self.default_base_url = settings.openai_base_url
        self.default_model = settings.kb_model
        
        # 缓存配置
        self._config_cache = {}
        self._cache_timestamp = 0
        self._cache_ttl = 300  # 5分钟缓存
    
    def _get_module_config(self, module_name: str) -> Dict[str, Any]:
        """获取模块的LLM配置"""
        import time
        current_time = time.time()
        
        # 检查缓存是否过期
        if current_time - self._cache_timestamp > self._cache_ttl:
            print(f"Config cache expired, refreshing...")
            self._refresh_config_cache()
        
        print(f"Getting config for module: {module_name}")
        print(f"Available modules in cache: {list(self._config_cache.keys())}")
        
        # 从缓存获取配置
        if module_name in self._config_cache:
            config = self._config_cache[module_name]
            print(f"Found config for {module_name}: API key exists = {bool(config.get('api_key'))}")
            return config
        
        # 如果没有找到配置，返回默认配置
        print(f"No config found for {module_name}, using default config")
        return {
            "api_key": self.default_api_key,
            "base_url": self.default_base_url,
            "model_name": self.default_model,
            "temperature": "0.7",
            "max_tokens": "2000",
            "is_enabled": True
        }
    
    def _refresh_config_cache(self):
        """刷新配置缓存"""
        import time
        db = SessionLocal()
        try:
            configs = db.query(LLMConfig).filter(LLMConfig.is_enabled == True).all()
            self._config_cache = {}
            print(f"Loading {len(configs)} LLM configs from database...")
            for config in configs:
                self._config_cache[config.module_name] = {
                    "api_key": config.api_key,
                    "base_url": config.base_url,
                    "model_name": config.model_name,
                    "temperature": config.temperature,
                    "max_tokens": config.max_tokens,
                    "is_enabled": config.is_enabled,
                    "enable_thinking": config.enable_thinking # 新增思考功能配置
                }
                print(f"Loaded config for module: {config.module_name}")
            self._cache_timestamp = time.time()
            print(f"Config cache refreshed with {len(self._config_cache)} modules")
        except Exception as e:
            print(f"Failed to refresh LLM config cache: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db.close()
    
    async def stream_chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        mode: str = "kb",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """流式聊天完成 - 使用OpenAI兼容模式
        
        支持的模式：
        - kb: 知识库检索（对应chat_kb模块）
        - graph: 复杂问答（对应chat_graph模块）
        - triage: 智能分诊（对应triage模块）
        - emergency: 应急指导（对应emergency_*模块）
        """
        # 根据模式映射到配置模块名称
        module_mapping = {
            "kb": "chat_kb",
            "graph": "chat_graph", 
            "triage": "triage",
            "emergency": "emergency_cpr"  # 默认使用CPR配置，可以根据具体场景调整
        }
        
        module_name = module_mapping.get(mode, "chat_kb")
        config = self._get_module_config(module_name)
        
        # 检查配置是否启用
        if not config.get("is_enabled", True):
            async for chunk in self._mock_stream_response(messages[-1]["content"], mode):
                yield chunk
            return
        
        # 检查API密钥
        api_key = config.get("api_key")
        if not api_key:
            async for chunk in self._mock_stream_response(messages[-1]["content"], mode):
                yield chunk
            return
        
        try:
            # 导入异步OpenAI SDK
            from openai import AsyncOpenAI
            
            # 创建客户端
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=config.get("base_url", "https://dashscope.aliyuncs.com/compatible-mode/v1")
            )
            
            # 处理消息格式
            processed_messages = []
            for msg in messages:
                processed_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # 获取配置参数
            model = config.get("model_name", "qwen-plus")
            if temperature is None:
                temperature = float(config.get("temperature", "0.7"))
            if max_tokens is None:
                max_tokens = int(config.get("max_tokens", "2000"))
            
            # 构建请求参数
            request_params = {
                "model": model,
                "messages": processed_messages,
                "stream": True,  # 强制启用流式输出
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            
            # 检查是否启用思考功能（从数据库配置中读取）
            enable_thinking = config.get("enable_thinking", False)
            if enable_thinking and "qwen" in model.lower():
                # 根据阿里云文档，通过extra_body配置思考功能
                request_params["extra_body"] = {
                    "enable_thinking": True,
                    "thinking_budget": 30000  # 思考过程的最大长度
                }
                print(f"启用思考模式 for model: {model}, module: {module_name}, extra_body: {request_params['extra_body']}")
            
            # 调用OpenAI兼容API
            completion = await client.chat.completions.create(**request_params)
            
            # 处理流式响应
            full_content = ""
            thinking_content = ""
            is_thinking = False
            
            async for chunk in completion:
                # 解析chunk数据
                chunk_dict = chunk.model_dump() if hasattr(chunk, 'model_dump') else chunk
                
                if 'choices' in chunk_dict and chunk_dict['choices']:
                    choice = chunk_dict['choices'][0]
                    delta = choice.get('delta', {})
                    
                    # 处理思考过程（Qwen3特有）
                    if 'reasoning_content' in delta and delta['reasoning_content']:
                        thinking_content += delta['reasoning_content']
                        is_thinking = True
                        yield {
                            "type": "thinking",
                            "content": delta['reasoning_content']
                        }
                        continue
                    
                    # 处理回复内容
                    if 'content' in delta and delta['content']:
                        content = delta['content']
                        
                        # 如果刚从思考模式切换到回答模式，或者是第一次输出内容
                        if (is_thinking and not full_content) or (not full_content and not is_thinking):
                            yield {
                                "type": "answer_start",
                                "content": ""
                            }
                            is_thinking = False
                        
                        full_content += content
                        yield {
                            "type": "answer",
                            "content": content
                        }
                    
                    # 检查是否完成
                    finish_reason = choice.get('finish_reason')
                    if finish_reason:
                        yield {
                            "type": "done",
                            "content": full_content,  # 返回完整内容而不是空字符串
                            "thinking_enabled": enable_thinking,
                            "thinking_content_length": len(thinking_content) if thinking_content else 0
                        }
                        break
            
        except Exception as e:
            print(f"AI服务调用失败: {e}")
            # 发生错误时返回模拟响应
            async for chunk in self._mock_stream_response(messages[-1]["content"], mode):
                yield chunk
    
    async def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        mode: str = "kb",
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """非流式聊天完成（用于兼容性）"""
        full_response = ""
        async for chunk in self.stream_chat_completion(messages, mode, temperature, max_tokens):
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
            "content": mock_content
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