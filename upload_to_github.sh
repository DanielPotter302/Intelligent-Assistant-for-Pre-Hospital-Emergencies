#!/bin/bash

# 院前急救助手系统 - GitHub上传脚本
echo "🚑 院前急救助手系统 - GitHub上传脚本"
echo "=================================="

# 检查Git是否可用
if ! command -v git &> /dev/null; then
    echo "❌ Git未安装或开发者工具未完成安装"
    echo "请等待Xcode命令行工具安装完成后再运行此脚本"
    exit 1
fi

echo "✅ Git已可用"

# 检查是否已经初始化Git仓库
if [ ! -d ".git" ]; then
    echo "📁 初始化Git仓库..."
    git init
    echo "✅ Git仓库初始化完成"
else
    echo "✅ Git仓库已存在"
fi

# 配置Git用户信息（如果需要）
if [ -z "$(git config user.name)" ]; then
    echo "👤 配置Git用户信息..."
    read -p "请输入您的GitHub用户名: " github_username
    read -p "请输入您的邮箱地址: " github_email
    
    git config user.name "$github_username"
    git config user.email "$github_email"
    echo "✅ Git用户信息配置完成"
fi

# 添加所有文件
echo "📦 添加文件到Git..."
git add .

# 检查是否有更改需要提交
if git diff --cached --quiet; then
    echo "ℹ️  没有新的更改需要提交"
else
    echo "💾 提交更改..."
    git commit -m "Initial commit: 院前急救助手系统

- 添加Vue.js前端应用
- 添加FastAPI后端服务
- 添加智能聊天功能
- 添加分诊系统
- 添加知识库管理
- 添加紧急指南
- 添加用户认证系统"
    echo "✅ 更改已提交"
fi

# 检查远程仓库配置
if ! git remote get-url origin &> /dev/null; then
    echo "🔗 配置远程仓库..."
    echo "请选择远程仓库URL类型："
    echo "1) HTTPS (推荐新手使用)"
    echo "2) SSH (需要配置SSH密钥)"
    read -p "请选择 (1/2): " url_type
    
    if [ "$url_type" = "2" ]; then
        read -p "请输入GitHub用户名: " username
        read -p "请输入仓库名称: " repo_name
        git remote add origin "git@github.com:$username/$repo_name.git"
    else
        read -p "请输入GitHub用户名: " username
        read -p "请输入仓库名称: " repo_name
        git remote add origin "https://github.com/$username/$repo_name.git"
    fi
    echo "✅ 远程仓库配置完成"
else
    echo "✅ 远程仓库已配置"
fi

# 设置主分支名称
echo "🌿 设置主分支..."
git branch -M main

# 推送到GitHub
echo "🚀 推送到GitHub..."
if git push -u origin main; then
    echo "✅ 项目已成功上传到GitHub！"
    echo ""
    echo "🎉 恭喜！您的院前急救助手系统已成功上传到GitHub"
    echo ""
    echo "📋 下一步建议："
    echo "1. 访问您的GitHub仓库页面"
    echo "2. 检查README.md是否正确显示"
    echo "3. 设置仓库描述和标签"
    echo "4. 邀请协作者（如果需要）"
    echo "5. 配置GitHub Pages（可选）"
    echo ""
    echo "🔗 您的仓库地址："
    git remote get-url origin
else
    echo "❌ 推送失败"
    echo "请检查："
    echo "1. 网络连接是否正常"
    echo "2. GitHub仓库是否已创建"
    echo "3. 权限是否正确"
    echo "4. 如果使用SSH，SSH密钥是否已配置"
fi 