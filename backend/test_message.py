#!/usr/bin/env python3
"""
测试留言功能
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_submit_message():
    """测试提交留言"""
    url = f"{BASE_URL}/api/contact"
    data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "content": "您好，我想了解一下院前急救助手系统的具体功能和使用方法。请问是否可以提供详细的使用指南？"
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"\n=== 测试提交留言 ===")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("留言提交成功!")
            return True
        else:
            print("留言提交失败!")
            return False
            
    except Exception as e:
        print(f"请求失败: {e}")
        return False

def test_admin_login():
    """测试管理员登录"""
    url = f"{BASE_URL}/api/auth/login"
    data = {
        "username": "admin",
        "password": "admin123"
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        print(f"\n=== 测试管理员登录 ===")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            token = result.get('data', {}).get('access_token')
            print("管理员登录成功!")
            return token
        else:
            print("管理员登录失败!")
            return None
            
    except Exception as e:
        print(f"请求失败: {e}")
        return None

def test_get_messages(token):
    """测试获取留言列表"""
    url = f"{BASE_URL}/api/admin/messages"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        result = response.json()
        
        print(f"\n=== 测试获取留言列表 ===")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            messages = result.get('data', {}).get('messages', [])
            print(f"获取到 {len(messages)} 条留言")
            return messages
        else:
            print("获取留言列表失败!")
            return []
            
    except Exception as e:
        print(f"请求失败: {e}")
        return []

def test_reply_message(token, message_id):
    """测试回复留言"""
    url = f"{BASE_URL}/api/admin/messages/{message_id}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "admin_reply": "感谢您的咨询！院前急救助手系统提供智能分诊、应急指导、知识库查询等功能。我们会尽快为您提供详细的使用指南。",
        "status": "replied"
    }
    
    try:
        response = requests.put(url, json=data, headers=headers)
        result = response.json()
        
        print(f"\n=== 测试回复留言 ===")
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("留言回复成功!")
            return True
        else:
            print("留言回复失败!")
            return False
            
    except Exception as e:
        print(f"请求失败: {e}")
        return False

if __name__ == "__main__":
    print("开始测试留言功能...")
    
    # 1. 测试提交留言
    print("\n" + "="*50)
    print("1. 测试提交留言")
    print("="*50)
    test_submit_message()
    
    # 再提交几条测试留言
    test_data = [
        {
            "name": "李四",
            "email": "lisi@example.com",
            "content": "系统在使用过程中遇到了一些问题，希望能得到技术支持。"
        },
        {
            "name": "王五",
            "email": "wangwu@example.com",
            "content": "请问系统是否支持移动端使用？有没有手机APP？"
        }
    ]
    
    for data in test_data:
        requests.post(f"{BASE_URL}/api/contact", json=data)
    
    # 2. 测试管理员登录
    print("\n" + "="*50)
    print("2. 测试管理员登录")
    print("="*50)
    token = test_admin_login()
    
    if not token:
        print("管理员登录失败，无法继续测试")
        exit(1)
    
    # 3. 测试获取留言列表
    print("\n" + "="*50)
    print("3. 测试获取留言列表")
    print("="*50)
    messages = test_get_messages(token)
    
    # 4. 测试回复留言
    if messages:
        print("\n" + "="*50)
        print("4. 测试回复留言")
        print("="*50)
        first_message = messages[0]
        test_reply_message(token, first_message['id'])
        
        # 再次获取留言列表，查看回复效果
        print("\n" + "="*50)
        print("5. 验证回复效果")
        print("="*50)
        test_get_messages(token)
    
    print("\n测试完成!") 