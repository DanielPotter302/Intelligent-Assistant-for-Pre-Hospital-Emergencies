#!/usr/bin/env python3
"""
调试应急指导消息API响应
检查消息数据的实际结构
"""

import requests
import json
import sys
import os

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

def debug_session_messages(token, session_id):
    """调试会话消息"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"🔍 调试会话消息: {session_id}")
    
    # 获取会话详情
    response = requests.get(f"{BASE_URL}/api/emergency/sessions/{session_id}", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API响应状态: {response.status_code}")
        print(f"📊 响应数据结构:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # 检查消息数据
        if 'data' in data:
            messages = data['data']
            print(f"\n📝 消息分析:")
            print(f"  消息类型: {type(messages)}")
            print(f"  消息数量: {len(messages) if isinstance(messages, list) else 'N/A'}")
            
            if isinstance(messages, list):
                for i, msg in enumerate(messages):
                    print(f"\n  消息 {i+1}:")
                    print(f"    ID: {msg.get('id', 'N/A')}")
                    print(f"    角色: {msg.get('role', 'N/A')}")
                    print(f"    内容长度: {len(msg.get('content', '')) if msg.get('content') else 0}")
                    print(f"    内容预览: {msg.get('content', '')[:100]}...")
                    print(f"    步骤: {msg.get('steps', 'N/A')}")
                    print(f"    设备: {msg.get('equipment', 'N/A')}")
                    print(f"    创建时间: {msg.get('created_at', 'N/A')}")
            else:
                print(f"  ⚠️  消息数据不是列表格式: {messages}")
        
        return data
    else:
        print(f"❌ API请求失败: {response.status_code}")
        print(f"错误信息: {response.text}")
        return None

def main():
    print("🧪 开始调试应急指导消息API...")
    
    # 1. 获取认证token
    print("\n1. 获取认证token...")
    token = get_auth_token()
    if not token:
        print("❌ 无法获取认证token，调试终止")
        return
    print("✅ 认证成功")
    
    # 2. 获取所有会话
    print("\n2. 获取所有会话...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/emergency/sessions", headers=headers)
    
    if response.status_code == 200:
        sessions_data = response.json()
        sessions = sessions_data.get('data', [])
        print(f"✅ 找到 {len(sessions)} 个会话")
        
        for session in sessions:
            print(f"\n会话: {session['title']} (ID: {session['id'][:8]}...)")
            
            # 调试每个会话的消息
            debug_session_messages(token, session['id'])
            
            print("\n" + "="*80)
    else:
        print(f"❌ 获取会话失败: {response.status_code}")
        print(f"错误信息: {response.text}")

if __name__ == "__main__":
    main() 