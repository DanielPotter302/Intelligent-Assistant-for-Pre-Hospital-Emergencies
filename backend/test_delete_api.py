#!/usr/bin/env python3
"""
测试删除API的实际效果
"""
import asyncio
import aiohttp
import json

async def test_delete_api():
    """测试删除API"""
    print("🔧 测试删除API的实际效果...")
    
    base_url = "http://localhost:8000"
    
    # 登录获取token
    login_data = {
        "username": "danielpotter",
        "password": "danielpotter123"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            # 1. 登录
            print("1️⃣ 登录...")
            async with session.post(
                f"{base_url}/api/auth/login", 
                json=login_data,
                headers={"Content-Type": "application/json"}
            ) as resp:
                if resp.status != 200:
                    print(f"❌ 登录失败: {resp.status}")
                    # 尝试admin用户
                    login_data["username"] = "admin"
                    login_data["password"] = "admin123"
                    async with session.post(
                        f"{base_url}/api/auth/login", 
                        json=login_data,
                        headers={"Content-Type": "application/json"}
                    ) as resp2:
                        if resp2.status != 200:
                            print(f"❌ admin登录也失败: {resp2.status}")
                            return
                        login_result = await resp2.json()
                else:
                    login_result = await resp.json()
                
                token = login_result["data"]["access_token"]
                headers = {"Authorization": f"Bearer {token}"}
                print("✅ 登录成功")
            
            # 2. 获取当前所有会话
            print("\n2️⃣ 获取当前所有会话...")
            async with session.get(
                f"{base_url}/api/chat/sessions",  # 移除mode参数
                headers=headers
            ) as resp:
                if resp.status != 200:
                    print(f"❌ 获取会话失败: {resp.status}")
                    return
                
                sessions_result = await resp.json()
                sessions = sessions_result["data"]
                print(f"📋 当前有 {len(sessions)} 个会话:")
                
                for i, sess in enumerate(sessions):
                    print(f"  {i+1}. {sess['title']} (ID: {sess['id'][:8]}...)")
                
                if not sessions:
                    print("❌ 没有会话可以删除")
                    return
                
                # 选择第一个会话进行删除测试
                target_session = sessions[0]
                session_id = target_session['id']
                session_title = target_session['title']
                
                print(f"\n🎯 选择删除会话: {session_title} (ID: {session_id[:8]}...)")
            
            # 3. 删除选中的会话
            print("\n3️⃣ 执行删除操作...")
            async with session.delete(
                f"{base_url}/api/chat/sessions/{session_id}",
                headers=headers
            ) as resp:
                print(f"📡 删除请求状态: {resp.status}")
                if resp.status == 200:
                    result = await resp.json()
                    print(f"✅ 删除成功: {result['message']}")
                elif resp.status == 404:
                    print("⚠️ 会话不存在或已被删除")
                elif resp.status == 403:
                    print("❌ 权限不足，无法删除此会话")
                else:
                    error_text = await resp.text()
                    print(f"❌ 删除失败: {error_text}")
                    return
            
            # 4. 验证删除效果 - 重新获取会话列表
            print("\n4️⃣ 验证删除效果...")
            await asyncio.sleep(1)  # 等待数据库更新
            
            async with session.get(
                f"{base_url}/api/chat/sessions",
                headers=headers
            ) as resp:
                if resp.status != 200:
                    print(f"❌ 重新获取会话失败: {resp.status}")
                    return
                
                new_sessions_result = await resp.json()
                new_sessions = new_sessions_result["data"]
                
                print(f"📋 删除后剩余 {len(new_sessions)} 个会话:")
                for i, sess in enumerate(new_sessions):
                    print(f"  {i+1}. {sess['title']} (ID: {sess['id'][:8]}...)")
                
                # 检查被删除的会话是否还存在
                deleted_session_exists = any(s['id'] == session_id for s in new_sessions)
                if deleted_session_exists:
                    print(f"❌ 删除失败！会话 {session_title} 仍然存在")
                else:
                    print(f"✅ 删除成功！会话 {session_title} 已被移除")
            
            # 5. 尝试直接访问被删除的会话
            print("\n5️⃣ 尝试直接访问被删除的会话...")
            async with session.get(
                f"{base_url}/api/chat/sessions/{session_id}",
                headers=headers
            ) as resp:
                if resp.status == 404:
                    print("✅ 会话已被彻底删除（404错误符合预期）")
                elif resp.status == 200:
                    print("❌ 会话仍然可以访问，删除失败")
                else:
                    print(f"⚠️ 意外的响应状态: {resp.status}")
            
            print("\n🎉 删除API测试完成！")
            
        except Exception as e:
            print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_delete_api()) 