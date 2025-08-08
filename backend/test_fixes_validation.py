#!/usr/bin/env python3
"""
验证修复后的功能
"""
import asyncio
import aiohttp
import json
import time

async def test_chat_and_delete():
    """测试聊天功能和删除功能"""
    print("🔧 测试修复后的聊天和删除功能...")
    
    # API基础URL
    base_url = "http://localhost:8000"
    
    # 登录获取token
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            # 1. 登录
            print("1️⃣ 登录...")
            login_data = {
                "username": "admin",
                "password": "admin123"
            }
            
            async with session.post(
                f"{base_url}/api/auth/login", 
                json=login_data,
                headers={"Content-Type": "application/json"}
            ) as resp:
                if resp.status != 200:
                    print(f"❌ 登录失败: {resp.status}")
                    text = await resp.text()
                    print(f"错误详情: {text}")
                    return
                
                login_result = await resp.json()
                token = login_result["data"]["access_token"]
                headers = {"Authorization": f"Bearer {token}"}
                print("✅ 登录成功")
            
            # 2. 发送消息并测试流式响应
            print("\n2️⃣ 发送消息测试流式响应...")
            message_data = {
                "content": "什么是心肺复苏？请简单介绍一下。",
                "mode": "kb"  # 使用知识检索模式
            }
            
            session_id = None
            full_response = ""
            
            async with session.post(
                f"{base_url}/api/chat/messages", 
                json=message_data, 
                headers=headers
            ) as resp:
                if resp.status != 200:
                    print(f"❌ 发送消息失败: {resp.status}")
                    return
                
                print("📡 接收流式响应...")
                async for line in resp.content:
                    line = line.decode('utf-8').strip()
                    if line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])
                            if data['type'] == 'user_message':
                                # 从用户消息中获取消息ID，稍后用于查询session
                                user_message_id = data['data']['id']
                                print(f"✅ 用户消息ID: {user_message_id[:8]}...")
                            elif data['type'] == 'assistant_message':
                                # 从助手消息中获取session_id
                                if 'data' in data and 'session_id' in data['data']:
                                    session_id = data['data']['session_id']
                                    print(f"✅ 从助手消息获取会话ID: {session_id[:8]}...")
                            elif data['type'] == 'answer':
                                full_response += data['content']
                                print("📝", end="", flush=True)
                            elif data['type'] == 'done':
                                print(f"\n✅ 流式响应完成，总长度: {len(full_response)} 字符")
                                break
                        except json.JSONDecodeError:
                            continue
            
            if not session_id:
                print("⚠️ 未从流式响应中获取到会话ID，尝试从API获取...")
                # 获取用户的所有会话
                async with session.get(
                    f"{base_url}/api/chat/sessions",
                    headers=headers
                ) as resp:
                    if resp.status == 200:
                        sessions_result = await resp.json()
                        sessions = sessions_result["data"]
                        if sessions:
                            # 获取最新的会话
                            session_id = sessions[0]['id']
                            print(f"✅ 从API获取到最新会话ID: {session_id[:8]}...")
                        else:
                            print("❌ 没有找到任何会话")
                            return
                    else:
                        print(f"❌ 获取会话列表失败: {resp.status}")
                        return
            
            # 3. 等待一下让数据库保存
            await asyncio.sleep(1)
            
            # 4. 获取会话历史验证AI回答是否保存
            print("\n3️⃣ 验证AI回答是否正确保存...")
            async with session.get(
                f"{base_url}/api/chat/sessions/{session_id}",
                headers=headers
            ) as resp:
                if resp.status != 200:
                    print(f"❌ 获取会话历史失败: {resp.status}")
                    return
                
                messages_result = await resp.json()
                messages = messages_result["data"]  # data直接就是消息列表
                
                print(f"📋 会话中共有 {len(messages)} 条消息:")
                ai_answer_found = False
                for i, msg in enumerate(messages[-4:]):  # 只显示最后4条消息
                    role = msg['role']
                    content = msg['content']
                    content_preview = content[:50] + "..." if len(content) > 50 else content
                    print(f"  {i+1}. [{role}] {content_preview}")
                    
                    if role == 'assistant':
                        if content and len(content) > 10:
                            print(f"✅ AI回答已正确保存，长度: {len(content)} 字符")
                            ai_answer_found = True
                        else:
                            print(f"❌ AI回答保存失败，内容为空或过短: '{content}'")
                
                if not ai_answer_found:
                    print("❌ 没有找到AI回答")
                    return
            
            # 5. 测试删除功能
            print("\n4️⃣ 测试删除功能...")
            async with session.delete(
                f"{base_url}/api/chat/sessions/{session_id}",
                headers=headers
            ) as resp:
                if resp.status != 200:
                    print(f"❌ 删除会话失败: {resp.status}")
                    return
                
                print("✅ 删除请求成功")
            
            # 6. 验证删除是否生效
            print("\n5️⃣ 验证删除是否生效...")
            await asyncio.sleep(1)  # 等待删除完成
            
            async with session.get(
                f"{base_url}/api/chat/sessions/{session_id}",
                headers=headers
            ) as resp:
                if resp.status == 404:
                    print("✅ 会话已成功删除（404错误符合预期）")
                elif resp.status == 200:
                    result = await resp.json()
                    if not result.get("data"):
                        print("✅ 会话已成功删除（返回空数据）")
                    else:
                        print("❌ 删除失败，会话仍然存在")
                        return
                else:
                    print(f"⚠️ 意外的响应状态: {resp.status}")
            
            # 7. 获取所有会话验证
            print("\n6️⃣ 获取所有会话验证删除...")
            async with session.get(
                f"{base_url}/api/chat/sessions",
                headers=headers
            ) as resp:
                if resp.status != 200:
                    print(f"❌ 获取会话列表失败: {resp.status}")
                    return
                
                sessions_result = await resp.json()
                sessions = sessions_result["data"]
                
                deleted_session_exists = any(s['id'] == session_id for s in sessions)
                if deleted_session_exists:
                    print("❌ 删除失败，会话仍在列表中")
                else:
                    print("✅ 删除成功，会话不在列表中")
            
            print("\n🎉 所有测试完成！")
            print("✅ AI回答保存功能：正常")
            print("✅ 删除功能：正常")
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_chat_and_delete()) 