#!/usr/bin/env python3
"""
测试会话创建后的实时同步功能
验证发送消息后会话是否能在前端实时显示
"""

import requests
import json
import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# API基础URL
BASE_URL = "http://localhost:8000"

def get_auth_token():
    """获取认证token"""
    login_data = {
        "username": "danielpotter",
        "password": "danielpotter123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json()["data"]["access_token"]
    else:
        print(f"登录失败: {response.text}")
        return None

def get_chat_sessions(token, mode="kb"):
    """获取聊天会话列表"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/chat/sessions", params={"mode": mode}, headers=headers)
    
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"❌ 获取会话列表失败: {response.text}")
        return []

def send_message_auto_session(token, content, mode="kb"):
    """发送消息（自动创建会话）并检查流式响应"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(
        f"{BASE_URL}/api/chat/messages",
        json={"content": content, "mode": mode},
        headers=headers,
        stream=True
    )
    
    if response.status_code == 200:
        session_id = None
        print("📡 开始接收流式响应...")
        
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    try:
                        data = json.loads(line_str[6:])
                        print(f"📨 收到事件: {data['type']}")
                        
                        if data['type'] == 'session_info':
                            session_id = data['data']['id']
                            print(f"✅ 检测到新会话创建: {session_id}")
                            print(f"   会话标题: {data['data']['title']}")
                            print(f"   会话模式: {data['data']['mode']}")
                            
                        elif data['type'] == 'done':
                            print("✅ 消息发送完成")
                            break
                            
                    except json.JSONDecodeError:
                        continue
        
        return session_id
    else:
        print(f"❌ 发送消息失败: {response.text}")
        return None

def main():
    print("🧪 开始测试会话创建后的实时同步功能...")
    
    # 1. 获取认证token
    print("\n1. 获取认证token...")
    token = get_auth_token()
    if not token:
        print("❌ 无法获取认证token，测试终止")
        return
    print("✅ 认证成功")
    
    # 2. 清空现有会话（为了测试）
    print("\n2. 清空现有会话...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/api/chat/sessions", params={"mode": "kb"}, headers=headers)
    if response.status_code == 200:
        print("✅ 现有会话已清空")
    
    # 3. 检查初始会话数量
    print("\n3. 检查初始会话数量...")
    initial_sessions = get_chat_sessions(token)
    print(f"📊 初始会话数量: {len(initial_sessions)}")
    
    # 4. 发送消息并自动创建会话
    print("\n4. 发送消息并自动创建会话...")
    test_message = "测试会话同步功能：如何判断患者的意识状态？"
    session_id = send_message_auto_session(token, test_message)
    
    if session_id:
        print(f"✅ 会话创建成功: {session_id}")
    else:
        print("❌ 会话创建失败")
        return
    
    # 5. 等待一下，然后检查会话列表
    print("\n5. 检查会话列表是否已更新...")
    time.sleep(1)  # 等待1秒
    updated_sessions = get_chat_sessions(token)
    print(f"📊 更新后会话数量: {len(updated_sessions)}")
    
    # 6. 验证新会话是否在列表中
    if len(updated_sessions) > len(initial_sessions):
        new_session = next((s for s in updated_sessions if s['id'] == session_id), None)
        if new_session:
            print(f"✅ 新会话已出现在列表中:")
            print(f"   ID: {new_session['id']}")
            print(f"   标题: {new_session['title']}")
            print(f"   最后消息: {new_session.get('last_message', 'N/A')}")
        else:
            print("❌ 新会话未在列表中找到")
    else:
        print("❌ 会话数量没有增加")
    
    print("\n🎉 测试完成！")
    print("\n📝 前端测试说明:")
    print("1. 打开浏览器访问前端页面")
    print("2. 登录后进入智能问答页面")
    print("3. 发送一条消息")
    print("4. 观察左侧边栏是否立即显示新创建的会话")
    print("5. 无需刷新页面，会话应该实时出现")

if __name__ == "__main__":
    main() 