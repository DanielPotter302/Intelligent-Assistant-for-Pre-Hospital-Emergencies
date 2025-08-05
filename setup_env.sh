#!/bin/bash

# 环境变量配置脚本
echo "🔧 配置院前急救助手系统环境变量..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 检查是否存在配置文件
if [ ! -f "backend/env.example" ]; then
    echo -e "${RED}❌ 未找到 backend/env.example 文件${NC}"
    exit 1
fi

# 生成安全的SECRET_KEY
echo -e "${GREEN}🔑 生成安全的 SECRET_KEY...${NC}"
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")

# 创建后端环境变量文件
echo -e "${GREEN}📝 创建后端环境变量文件...${NC}"
cp backend/env.example backend/.env

# 替换SECRET_KEY
sed -i.bak "s/your-super-secret-key-change-this-in-production/$SECRET_KEY/g" backend/.env

# 创建前端环境变量文件
echo -e "${GREEN}📝 创建前端环境变量文件...${NC}"
if [ ! -f "env.production" ]; then
    cp env.example env.production
fi

echo ""
echo -e "${GREEN}✅ 环境变量文件创建完成！${NC}"
echo ""
echo -e "${YELLOW}⚠️  重要提醒：${NC}"
echo ""
echo "1. 🔑 SECRET_KEY 已自动生成并配置"
echo "2. 🤖 请手动配置 DASHSCOPE_API_KEY："
echo ""
echo "   编辑 backend/.env 文件，找到这一行："
echo "   DASHSCOPE_API_KEY=your-dashscope-api-key-here"
echo ""
echo "   替换为您的实际API密钥"
echo ""
echo "3. 🌐 如需修改前端API地址，编辑 env.production 文件"
echo ""
echo -e "${GREEN}📁 配置文件位置：${NC}"
echo "   - 后端配置: backend/.env"
echo "   - 前端配置: env.production"
echo ""
echo -e "${YELLOW}🔗 获取DASHSCOPE_API_KEY的步骤：${NC}"
echo "   1. 访问 https://www.aliyun.com/"
echo "   2. 注册/登录阿里云账号"
echo "   3. 搜索并开通'通义千问'服务"
echo "   4. 在控制台创建API密钥"
echo "   5. 将密钥填入 backend/.env 文件"
echo ""
echo -e "${GREEN}🚀 配置完成后，运行以下命令启动系统：${NC}"
echo "   ./deploy.sh prod" 