#!/usr/bin/env python3
"""
API测试脚本
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查"""
    print("测试健康检查...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 健康检查通过")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_register():
    """测试用户注册"""
    print("测试用户注册...")
    try:
        data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
            "real_name": "测试用户"
        }
        response = requests.post(f"{BASE_URL}/api/auth/register", json=data)
        if response.status_code in [200, 201]:
            print("✅ 用户注册成功")
            return True
        elif response.status_code == 400:
            print("⚠️ 用户可能已存在")
            return True
        else:
            print(f"❌ 用户注册失败: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ 用户注册异常: {e}")
        return False

def test_login():
    """测试用户登录"""
    print("测试用户登录...")
    try:
        data = {
            "username": "test",
            "password": "test123"
        }
        response = requests.post(f"{BASE_URL}/api/auth/login", json=data)
        if response.status_code == 200:
            result = response.json()
            token = result.get("data", {}).get("access_token")
            if token:
                print("✅ 用户登录成功")
                return token
            else:
                print("❌ 登录响应中没有token")
                return None
        else:
            print(f"❌ 用户登录失败: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ 用户登录异常: {e}")
        return None

def test_features(token):
    """测试获取功能列表"""
    print("测试获取功能列表...")
    try:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        response = requests.get(f"{BASE_URL}/api/features", headers=headers)
        if response.status_code == 200:
            print("✅ 获取功能列表成功")
            return True
        else:
            print(f"❌ 获取功能列表失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取功能列表异常: {e}")
        return False

def test_chat_session(token):
    """测试聊天会话"""
    if not token:
        print("⚠️ 跳过聊天测试（无token）")
        return False
        
    print("测试创建聊天会话...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {
            "title": "测试聊天",
            "mode": "kb"
        }
        response = requests.post(f"{BASE_URL}/api/chat/sessions", json=data, headers=headers)
        if response.status_code in [200, 201]:
            print("✅ 创建聊天会话成功")
            return True
        else:
            print(f"❌ 创建聊天会话失败: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"❌ 创建聊天会话异常: {e}")
        return False

def main():
    """主测试函数"""
    print("=== 院前急救助手系统API测试 ===\n")
    
    # 测试健康检查
    if not test_health():
        print("❌ 服务未启动或不可用")
        sys.exit(1)
    
    print()
    
    # 测试注册
    test_register()
    print()
    
    # 测试登录
    token = test_login()
    print()
    
    # 测试功能列表
    test_features(token)
    print()
    
    # 测试聊天会话
    test_chat_session(token)
    print()
    
    print("=== 测试完成 ===")
    print("如需查看完整API文档，请访问: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 