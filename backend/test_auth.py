#!/usr/bin/env python3
"""
测试登录验证功能
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_login(username, password):
    """测试登录功能"""
    url = f"{BASE_URL}/api/auth/login"
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"\n=== 测试登录: {username} ===")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            user_data = result.get('data', {}).get('user', {})
            print(f"登录成功! 用户角色: {user_data.get('role')}")
            return True
        else:
            print("登录失败!")
            return False
            
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def test_register(username, password):
    """测试注册功能"""
    url = f"{BASE_URL}/api/auth/register"
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"\n=== 测试注册: {username} ===")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200 or response.status_code == 201:
            print("注册成功!")
            return True
        else:
            print("注册失败!")
            return False
            
    except Exception as e:
        print(f"请求失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试登录验证功能...")
    
    # 测试现有用户登录
    print("\n" + "="*50)
    print("测试现有用户登录")
    print("="*50)
    
    test_login("admin", "admin123")
    test_login("danielpotter", "danielpotter123")
    test_login("wronguser", "wrongpass")
    
    # 测试新用户注册
    print("\n" + "="*50)
    print("测试新用户注册")
    print("="*50)
    
    test_register("testuser", "testpass123")
    test_register("admin", "admin123")  # 应该失败，用户名已存在
    
    # 测试新注册用户登录
    print("\n" + "="*50)
    print("测试新注册用户登录")
    print("="*50)
    
    test_login("testuser", "testpass123")
    
    print("\n测试完成!") 