#!/usr/bin/env python3
"""
测试应急指导会话加载功能
验证聊天记录点击功能是否正常工作
"""

import requests
import json
import sys
import os

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

def get_emergency_sessions(token):
    """获取应急指导会话列表"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/emergency/sessions", headers=headers)
    
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"❌ 获取会话列表失败: {response.text}")
        return []

def get_session_messages(token, session_id):
    """获取会话消息"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/emergency/sessions/{session_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"❌ 获取会话消息失败: {response.text}")
        return []

def create_test_session(token):
    """创建测试会话"""
    headers = {"Authorization": f"Bearer {token}"}
    session_data = {
        "scenario_type": "equipment",
        "title": "测试应急指导会话"
    }
    
    response = requests.post(f"{BASE_URL}/api/emergency/sessions", json=session_data, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"❌ 创建会话失败: {response.text}")
        return None

def send_test_message(token, session_id):
    """发送测试消息"""
    headers = {"Authorization": f"Bearer {token}"}
    message_data = {
        "content": "测试消息：如何使用AED设备？",
        "scenario": "equipment"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/emergency/sessions/{session_id}/messages",
        json=message_data,
        headers=headers,
        stream=True
    )
    
    if response.status_code == 200:
        print("✅ 消息发送成功")
        # 简单处理流式响应
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    try:
                        data = json.loads(line_str[6:])
                        if data['type'] == 'done':
                            break
                    except json.JSONDecodeError:
                        continue
        return True
    else:
        print(f"❌ 发送消息失败: {response.text}")
        return False

def main():
    print("🧪 开始测试应急指导会话加载功能...")
    
    # 1. 获取认证token
    print("\n1. 获取认证token...")
    token = get_auth_token()
    if not token:
        print("❌ 无法获取认证token，测试终止")
        return
    print("✅ 认证成功")
    
    # 2. 获取现有会话列表
    print("\n2. 获取现有会话列表...")
    sessions = get_emergency_sessions(token)
    print(f"📊 当前应急指导会话数量: {len(sessions)}")
    
    # 3. 如果没有会话，创建一个测试会话
    if len(sessions) == 0:
        print("\n3. 创建测试会话...")
        session = create_test_session(token)
        if not session:
            print("❌ 创建测试会话失败，测试终止")
            return
        
        session_id = session["id"]
        print(f"✅ 创建测试会话成功: {session_id}")
        
        # 发送测试消息
        print("\n4. 发送测试消息...")
        if not send_test_message(token, session_id):
            print("❌ 发送测试消息失败")
            return
        
        # 重新获取会话列表
        sessions = get_emergency_sessions(token)
    else:
        session_id = sessions[0]["id"]
        print(f"📋 使用现有会话: {session_id}")
    
    # 5. 测试获取会话消息
    print(f"\n5. 测试获取会话消息...")
    messages = get_session_messages(token, session_id)
    
    if isinstance(messages, list):
        print(f"✅ 成功获取会话消息: {len(messages)} 条")
        for i, msg in enumerate(messages):
            print(f"   消息 {i+1}: {msg.get('role', 'unknown')} - {msg.get('content', '')[:50]}...")
    else:
        print(f"❌ 获取会话消息失败，返回数据格式错误: {type(messages)}")
        print(f"   返回数据: {messages}")
        return
    
    # 6. 验证数据格式
    print("\n6. 验证数据格式...")
    if messages and len(messages) > 0:
        first_msg = messages[0]
        required_fields = ['id', 'role', 'content', 'created_at']
        missing_fields = [field for field in required_fields if field not in first_msg]
        
        if missing_fields:
            print(f"❌ 消息数据缺少必要字段: {missing_fields}")
            print(f"   实际字段: {list(first_msg.keys())}")
        else:
            print("✅ 消息数据格式正确")
    
    print("\n🎉 测试完成！")
    print("\n📝 前端测试说明:")
    print("1. 打开浏览器访问前端页面")
    print("2. 登录后进入应急指导页面")
    print("3. 点击左侧场景中的历史记录")
    print("4. 观察是否能正常加载聊天记录")

if __name__ == "__main__":
    main() 