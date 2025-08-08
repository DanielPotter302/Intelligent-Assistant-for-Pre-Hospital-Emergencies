#!/usr/bin/env python3
"""
调试用户认证和会话获取
"""
import asyncio
import aiohttp
import json

async def debug_auth_and_sessions():
    """调试用户认证和会话获取"""
    print("🔧 调试用户认证和会话获取...")
    
    base_url = "http://localhost:8000"
    
    async with aiohttp.ClientSession() as session:
        try:
            # 1. 尝试danielpotter登录
            print("1️⃣ 尝试danielpotter登录...")
            login_data = {
                "username": "danielpotter",
                "password": "danielpotter123"
            }
            
            async with session.post(
                f"{base_url}/api/auth/login", 
                json=login_data,
                headers={"Content-Type": "application/json"}
            ) as resp:
                print(f"📡 登录响应状态: {resp.status}")
                if resp.status == 200:
                    login_result = await resp.json()
                    token = login_result["data"]["access_token"]
                    user_info = login_result["data"]["user"]
                    print(f"✅ danielpotter登录成功")
                    print(f"📋 用户信息: {user_info}")
                    headers = {"Authorization": f"Bearer {token}"}
                    current_user = "danielpotter"
                else:
                    error_text = await resp.text()
                    print(f"❌ danielpotter登录失败: {error_text}")
                    
                    # 尝试admin登录
                    print("\n🔄 尝试admin登录...")
                    admin_login_data = {
                        "username": "admin",
                        "password": "admin123"
                    }
                    
                    async with session.post(
                        f"{base_url}/api/auth/login", 
                        json=admin_login_data,
                        headers={"Content-Type": "application/json"}
                    ) as resp2:
                        print(f"📡 admin登录响应状态: {resp2.status}")
                        if resp2.status == 200:
                            login_result = await resp2.json()
                            token = login_result["data"]["access_token"]
                            user_info = login_result["data"]["user"]
                            print(f"✅ admin登录成功")
                            print(f"📋 用户信息: {user_info}")
                            headers = {"Authorization": f"Bearer {token}"}
                            current_user = "admin"
                        else:
                            error_text = await resp2.text()
                            print(f"❌ admin登录也失败: {error_text}")
                            return
            
            # 2. 获取当前用户信息
            print(f"\n2️⃣ 获取当前用户信息...")
            async with session.get(
                f"{base_url}/api/auth/me",
                headers=headers
            ) as resp:
                if resp.status == 200:
                    user_result = await resp.json()
                    print(f"✅ 当前用户: {user_result}")
                else:
                    error_text = await resp.text()
                    print(f"❌ 获取用户信息失败: {error_text}")
            
            # 3. 获取所有模式的会话
            modes = ["kb", "graph"]
            for mode in modes:
                print(f"\n3️⃣ 获取 {mode} 模式的会话...")
                async with session.get(
                    f"{base_url}/api/chat/sessions?mode={mode}",
                    headers=headers
                ) as resp:
                    print(f"📡 响应状态: {resp.status}")
                    if resp.status == 200:
                        sessions_result = await resp.json()
                        sessions = sessions_result["data"]
                        print(f"📋 {mode} 模式会话数量: {len(sessions)}")
                        for i, sess in enumerate(sessions):
                            print(f"  {i+1}. {sess['title']} (ID: {sess['id'][:8]}...)")
                    else:
                        error_text = await resp.text()
                        print(f"❌ 获取 {mode} 模式会话失败: {error_text}")
            
            # 4. 不指定模式获取会话（使用默认kb模式）
            print(f"\n4️⃣ 不指定模式获取会话（默认kb）...")
            async with session.get(
                f"{base_url}/api/chat/sessions",
                headers=headers
            ) as resp:
                print(f"📡 响应状态: {resp.status}")
                if resp.status == 200:
                    sessions_result = await resp.json()
                    sessions = sessions_result["data"]
                    print(f"📋 默认模式会话数量: {len(sessions)}")
                    for i, sess in enumerate(sessions):
                        print(f"  {i+1}. {sess['title']} (ID: {sess['id'][:8]}...)")
                else:
                    error_text = await resp.text()
                    print(f"❌ 获取默认模式会话失败: {error_text}")
            
        except Exception as e:
            print(f"❌ 调试失败: {e}")

if __name__ == "__main__":
    asyncio.run(debug_auth_and_sessions()) 