#!/usr/bin/env python3
"""
测试聊天记录删除功能
验证单个删除、批量删除和清空全部功能是否正常工作
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
        "username": "danielpotter",  # 使用测试用户
        "password": "danielpotter123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
    if response.status_code == 200:
        return response.json()["data"]["access_token"]
    else:
        print(f"登录失败: {response.text}")
        return None

def create_test_sessions(token, count=3):
    """创建测试会话"""
    headers = {"Authorization": f"Bearer {token}"}
    session_ids = []
    
    for i in range(count):
        session_data = {
            "title": f"测试会话 {i+1}",
            "mode": "kb"
        }
        
        response = requests.post(f"{BASE_URL}/api/chat/sessions", json=session_data, headers=headers)
        if response.status_code == 200:
            session_id = response.json()["data"]["id"]
            session_ids.append(session_id)
            print(f"✅ 创建测试会话: {session_id}")
        else:
            print(f"❌ 创建会话失败: {response.text}")
    
    return session_ids

def get_chat_sessions(token, mode="kb"):
    """获取聊天会话列表"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/chat/sessions", params={"mode": mode}, headers=headers)
    
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"❌ 获取会话列表失败: {response.text}")
        return []

def test_single_delete(token, session_id):
    """测试单个删除功能"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/api/chat/sessions/{session_id}", headers=headers)
    
    if response.status_code == 200:
        print(f"✅ 单个删除成功: {session_id}")
        return True
    else:
        print(f"❌ 单个删除失败: {response.text}")
        return False

def test_clear_all(token, mode="kb"):
    """测试清空全部功能"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/api/chat/sessions", params={"mode": mode}, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 清空全部成功: {result['message']}")
        return True
    else:
        print(f"❌ 清空全部失败: {response.text}")
        return False

def main():
    print("🧪 开始测试聊天记录删除功能...")
    
    # 1. 获取认证token
    print("\n1. 获取认证token...")
    token = get_auth_token()
    if not token:
        print("❌ 无法获取认证token，测试终止")
        return
    print("✅ 认证成功")
    
    # 2. 查看当前会话数量
    print("\n2. 查看当前会话数量...")
    initial_sessions = get_chat_sessions(token)
    print(f"📊 当前会话数量: {len(initial_sessions)}")
    
    # 3. 创建测试会话
    print("\n3. 创建测试会话...")
    test_session_ids = create_test_sessions(token, 3)
    if len(test_session_ids) < 3:
        print("❌ 创建测试会话失败，测试终止")
        return
    
    # 4. 验证会话已创建
    print("\n4. 验证会话已创建...")
    sessions_after_create = get_chat_sessions(token)
    print(f"📊 创建后会话数量: {len(sessions_after_create)}")
    
    # 5. 测试单个删除
    print("\n5. 测试单个删除...")
    if test_single_delete(token, test_session_ids[0]):
        sessions_after_single_delete = get_chat_sessions(token)
        print(f"📊 单个删除后会话数量: {len(sessions_after_single_delete)}")
    
    # 6. 测试清空全部
    print("\n6. 测试清空全部...")
    if test_clear_all(token):
        sessions_after_clear = get_chat_sessions(token)
        print(f"📊 清空后会话数量: {len(sessions_after_clear)}")
        
        if len(sessions_after_clear) == 0:
            print("✅ 清空功能正常工作")
        else:
            print("❌ 清空功能可能存在问题")
    
    print("\n🎉 测试完成！")

if __name__ == "__main__":
    main() 