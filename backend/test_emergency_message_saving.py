#!/usr/bin/env python3
"""
测试应急指导AI消息保存功能
验证AI回复是否正确保存到数据库
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

def create_test_session(token):
    """创建测试会话"""
    headers = {"Authorization": f"Bearer {token}"}
    session_data = {
        "scenario_type": "equipment",
        "title": "测试AI消息保存"
    }
    
    response = requests.post(f"{BASE_URL}/api/emergency/sessions", json=session_data, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"❌ 创建会话失败: {response.text}")
        return None

def send_message_and_track(token, session_id, content):
    """发送消息并跟踪AI回复"""
    headers = {"Authorization": f"Bearer {token}"}
    message_data = {
        "content": content,
        "scenario": "equipment"
    }
    
    print(f"📤 发送消息: {content}")
    
    response = requests.post(
        f"{BASE_URL}/api/emergency/sessions/{session_id}/messages",
        json=message_data,
        headers=headers,
        stream=True
    )
    
    if response.status_code == 200:
        ai_message_id = None
        ai_content = ""
        
        print("📡 接收流式响应...")
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    try:
                        data = json.loads(line_str[6:])
                        print(f"   事件: {data['type']}")
                        
                        if data['type'] == 'answer_start':
                            ai_message_id = data.get('message_id')
                            print(f"   AI消息ID: {ai_message_id}")
                            
                        elif data['type'] == 'answer':
                            ai_content += data.get('content', '')
                            
                        elif data['type'] == 'assistant_message':
                            print(f"   AI消息保存: {data['data']['id']}")
                            
                        elif data['type'] == 'done':
                            print("✅ 消息发送完成")
                            break
                            
                    except json.JSONDecodeError:
                        continue
        
        return ai_message_id, ai_content
    else:
        print(f"❌ 发送消息失败: {response.text}")
        return None, None

def get_session_messages(token, session_id):
    """获取会话消息"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/emergency/sessions/{session_id}", headers=headers)
    
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"❌ 获取会话消息失败: {response.text}")
        return []

def main():
    print("🧪 开始测试应急指导AI消息保存功能...")
    
    # 1. 获取认证token
    print("\n1. 获取认证token...")
    token = get_auth_token()
    if not token:
        print("❌ 无法获取认证token，测试终止")
        return
    print("✅ 认证成功")
    
    # 2. 创建测试会话
    print("\n2. 创建测试会话...")
    session = create_test_session(token)
    if not session:
        print("❌ 创建测试会话失败，测试终止")
        return
    
    session_id = session["id"]
    print(f"✅ 创建测试会话成功: {session_id}")
    
    # 3. 检查初始会话消息（应该为空）
    print("\n3. 检查初始会话消息...")
    initial_messages = get_session_messages(token, session_id)
    print(f"📊 初始消息数量: {len(initial_messages)}")
    
    if len(initial_messages) > 0:
        print("⚠️  发现初始消息（可能是系统自动添加的）:")
        for msg in initial_messages:
            print(f"   {msg['role']}: {msg['content'][:50]}...")
    
    # 4. 发送测试消息
    print("\n4. 发送测试消息...")
    test_message = "如何正确使用AED设备进行心肺复苏？"
    ai_message_id, ai_content = send_message_and_track(token, session_id, test_message)
    
    if not ai_message_id:
        print("❌ 未获取到AI消息ID")
        return
    
    print(f"📝 AI回复内容预览: {ai_content[:100]}...")
    
    # 5. 等待一下，然后检查数据库中的消息
    print("\n5. 检查数据库中的消息...")
    time.sleep(2)  # 等待2秒确保数据库写入完成
    
    final_messages = get_session_messages(token, session_id)
    print(f"📊 最终消息数量: {len(final_messages)}")
    
    # 6. 分析消息内容
    print("\n6. 分析消息内容...")
    user_messages = [msg for msg in final_messages if msg['role'] == 'user']
    assistant_messages = [msg for msg in final_messages if msg['role'] == 'assistant']
    
    print(f"   用户消息: {len(user_messages)} 条")
    print(f"   AI消息: {len(assistant_messages)} 条")
    
    if len(user_messages) == 0:
        print("❌ 用户消息未保存")
    else:
        print(f"✅ 用户消息已保存: {user_messages[0]['content'][:50]}...")
    
    if len(assistant_messages) == 0:
        print("❌ AI消息未保存 - 这是问题所在！")
    else:
        print(f"✅ AI消息已保存: {assistant_messages[-1]['content'][:50]}...")
        
        # 检查AI消息的完整性
        last_ai_msg = assistant_messages[-1]
        if last_ai_msg['id'] == ai_message_id:
            print("✅ AI消息ID匹配")
        else:
            print(f"⚠️  AI消息ID不匹配: 期望 {ai_message_id}, 实际 {last_ai_msg['id']}")
    
    # 7. 详细显示所有消息
    print("\n7. 详细消息列表:")
    for i, msg in enumerate(final_messages):
        print(f"   消息 {i+1}: [{msg['role']}] {msg['content'][:80]}...")
        if msg.get('steps'):
            print(f"      步骤: {msg['steps']}")
        if msg.get('equipment'):
            print(f"      设备: {msg['equipment']}")
    
    print("\n🎉 测试完成！")
    
    # 总结
    if len(assistant_messages) == 0:
        print("\n❌ 问题确认: AI消息没有被保存到数据库")
        print("   可能的原因:")
        print("   1. 流式响应中的保存逻辑有问题")
        print("   2. 数据库事务没有正确提交")
        print("   3. AI服务返回的数据格式有问题")
    else:
        print("\n✅ AI消息保存正常")

if __name__ == "__main__":
    main() 