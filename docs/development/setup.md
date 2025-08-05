# 开发环境搭建指南

## 系统要求

### 基础环境

- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Node.js**: 18.0+ (推荐使用 LTS 版本)
- **Python**: 3.8+ (推荐 3.11)
- **Git**: 2.20+

### 推荐工具

- **IDE**: VS Code, WebStorm, PyCharm
- **数据库工具**: DB Browser for SQLite, pgAdmin
- **API 测试**: Postman, Insomnia
- **容器**: Docker Desktop

## 环境安装

### 1. Node.js 安装

#### Windows/macOS

1. 访问 [Node.js 官网](https://nodejs.org/)
2. 下载 LTS 版本
3. 运行安装程序

#### Linux (Ubuntu/Debian)

```bash
# 使用NodeSource仓库
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 验证安装
node --version
npm --version
```

### 2. Python 安装

#### Windows

1. 访问 [Python 官网](https://python.org/)
2. 下载 Python 3.11
3. 安装时勾选"Add Python to PATH"

#### macOS

```bash
# 使用Homebrew
brew install python@3.11

# 或使用pyenv
brew install pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

#### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv

# 验证安装
python3 --version
pip3 --version
```

### 3. Git 配置

```bash
# 配置用户信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 配置默认分支名
git config --global init.defaultBranch main

# 配置换行符处理（Windows）
git config --global core.autocrlf true

# 配置换行符处理（macOS/Linux）
git config --global core.autocrlf input
```

## 项目设置

### 1. 克隆项目

```bash
# 克隆仓库
git clone <repository-url>
cd pre-hospital-assistant

# 查看项目结构
ls -la
```

### 2. 前端环境设置

```bash
# 安装依赖
npm install

# 复制环境配置
cp env.example .env.local

# 编辑环境配置
# 设置API地址、应用标题等
vim .env.local
```

#### 前端环境变量说明

```bash
# .env.local 文件内容
VITE_API_BASE_URL=http://localhost:8000    # 后端API地址
VITE_APP_TITLE=院前急救助手系统             # 应用标题
VITE_USE_MOCK=false                        # 是否使用Mock数据
VITE_LOG_LEVEL=info                        # 日志级别
```

### 3. 后端环境设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制环境配置
cp env.example .env

# 编辑环境配置
vim .env
```

#### 后端环境变量说明

```bash
# .env 文件内容
DATABASE_URL=sqlite:///./pre_hospital_assistant.db  # 数据库连接
SECRET_KEY=your-super-secret-key                    # JWT密钥
OPENAI_API_KEY=your-openai-api-key                  # OpenAI API密钥（可选）
DEBUG=true                                          # 调试模式
```

### 4. 数据库初始化

```bash
# 在backend目录下
python init_db.py
```

## IDE 配置

### VS Code 推荐插件

#### 前端开发

- **Vue Language Features (Volar)** - Vue 3 支持
- **TypeScript Vue Plugin (Volar)** - TypeScript 支持
- **ESLint** - 代码检查
- **Prettier** - 代码格式化
- **Tailwind CSS IntelliSense** - Tailwind 智能提示
- **Auto Rename Tag** - 标签自动重命名

#### 后端开发

- **Python** - Python 语言支持
- **Pylance** - Python 智能提示
- **Python Docstring Generator** - 文档字符串生成
- **autoDocstring** - 自动生成文档
- **SQLite Viewer** - SQLite 数据库查看

#### 通用插件

- **GitLens** - Git 增强
- **Thunder Client** - API 测试
- **Docker** - Docker 支持
- **Live Share** - 实时协作

### VS Code 配置文件

创建 `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "python.defaultInterpreterPath": "./backend/venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "files.associations": {
    "*.vue": "vue"
  },
  "emmet.includeLanguages": {
    "vue": "html"
  },
  "typescript.preferences.importModuleSpecifier": "relative"
}
```

创建 `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Frontend",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/vite",
      "args": ["--mode", "development"],
      "console": "integratedTerminal"
    },
    {
      "name": "Debug Backend",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/backend/start.py",
      "console": "integratedTerminal",
      "cwd": "${workspaceFolder}/backend",
      "env": {
        "PYTHONPATH": "${workspaceFolder}/backend"
      }
    }
  ]
}
```

## 开发流程

### 1. 启动开发服务器

#### 方式一：分别启动

```bash
# 终端1 - 启动后端
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python start.py

# 终端2 - 启动前端
npm run dev
```

#### 方式二：使用并发启动（推荐）

```bash
# 安装并发工具
npm install -g concurrently

# 同时启动前后端
npm run dev:all
```

在 `package.json` 中添加脚本：

```json
{
  "scripts": {
    "dev:all": "concurrently \"npm run dev\" \"cd backend && python start.py\"",
    "dev:backend": "cd backend && python start.py",
    "dev:frontend": "vite"
  }
}
```

### 2. 验证环境

访问以下地址确认服务正常：

- **前端**: http://localhost:5173
- **后端 API 文档**: http://localhost:8000/docs
- **后端健康检查**: http://localhost:8000/health

### 3. 运行测试

```bash
# 前端测试
npm run test:unit
npm run test:e2e

# 后端测试
cd backend
python test_api.py
```

## 常见问题

### 1. Node.js 版本问题

```bash
# 使用nvm管理Node.js版本
# 安装nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 安装并使用Node.js 18
nvm install 18
nvm use 18
```

### 2. Python 虚拟环境问题

```bash
# 删除现有虚拟环境
rm -rf venv

# 重新创建虚拟环境
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. 端口冲突

```bash
# 查看端口占用
# Windows
netstat -ano | findstr :5173
netstat -ano | findstr :8000

# macOS/Linux
lsof -i :5173
lsof -i :8000

# 杀死占用进程
# Windows
taskkill /PID <PID> /F

# macOS/Linux
kill -9 <PID>
```

### 4. 依赖安装失败

```bash
# 清理npm缓存
npm cache clean --force

# 删除node_modules重新安装
rm -rf node_modules package-lock.json
npm install

# Python依赖问题
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --force-reinstall
```

## 开发工具配置

### 1. ESLint 配置

项目已包含 ESLint 配置，支持：

- Vue 3 语法检查
- TypeScript 类型检查
- 代码风格统一

### 2. Prettier 配置

项目已包含 Prettier 配置，支持：

- 自动代码格式化
- 统一代码风格
- 保存时自动格式化

### 3. Git Hooks

建议配置 Git Hooks 确保代码质量：

```bash
# 安装husky
npm install --save-dev husky

# 初始化husky
npx husky install

# 添加pre-commit hook
npx husky add .husky/pre-commit "npm run lint && npm run type-check"
```

## 性能优化建议

### 开发环境优化

1. 使用 SSD 硬盘
2. 增加内存（推荐 16GB+）
3. 关闭不必要的后台程序
4. 使用快速的网络连接

### 工具配置优化

1. 配置 IDE 排除 node_modules 索引
2. 使用增量编译
3. 启用热重载功能
4. 配置合适的缓存策略

---

如有其他问题，请查看[故障排除文档](../troubleshooting.md)或联系开发团队。
