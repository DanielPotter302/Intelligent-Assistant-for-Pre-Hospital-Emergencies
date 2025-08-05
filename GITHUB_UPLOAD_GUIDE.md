# GitHub上传操作指南

## 🚑 院前急救助手系统 - GitHub上传完整指南

### 📋 准备工作

1. **等待开发者工具安装完成**
   - 系统正在安装Xcode命令行工具
   - 安装完成后，Git命令将可用
   - 可以通过运行 `git --version` 检查是否安装完成

2. **准备GitHub账户**
   - 确保您有GitHub账户
   - 记住您的GitHub用户名

### 🔧 方法一：使用自动化脚本（推荐）

当开发者工具安装完成后，运行以下命令：

```bash
# 运行自动化上传脚本
./upload_to_github.sh
```

脚本会自动完成以下操作：

- ✅ 检查Git是否可用
- ✅ 初始化Git仓库
- ✅ 配置Git用户信息
- ✅ 添加所有文件
- ✅ 提交更改
- ✅ 配置远程仓库
- ✅ 推送到GitHub

### 🔧 方法二：手动操作

如果脚本无法运行，可以按照以下步骤手动操作：

#### 步骤1：初始化Git仓库

```bash
# 初始化Git仓库
git init

# 配置用户信息（如果是第一次使用Git）
git config user.name "您的GitHub用户名"
git config user.email "您的邮箱地址"
```

#### 步骤2：添加文件并提交

```bash
# 添加所有文件
git add .

# 提交更改
git commit -m "Initial commit: 院前急救助手系统

- 添加Vue.js前端应用
- 添加FastAPI后端服务
- 添加智能聊天功能
- 添加分诊系统
- 添加知识库管理
- 添加紧急指南
- 添加用户认证系统"
```

#### 步骤3：在GitHub上创建仓库

1. 访问 [GitHub](https://github.com)
2. 点击右上角 "+" 号，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `Pre_hospital_assistant_front`
   - **Description**: `院前急救助手系统 - 基于Vue.js和FastAPI的智能急救辅助系统`
   - **Visibility**: 选择 Public 或 Private
   - **不要**勾选 "Add a README file"
   - **不要**勾选 "Add .gitignore"
4. 点击 "Create repository"

#### 步骤4：连接并推送到GitHub

```bash
# 添加远程仓库（HTTPS方式）
git remote add origin https://github.com/您的用户名/Pre_hospital_assistant_front.git

# 或者使用SSH方式（如果配置了SSH密钥）
git remote add origin git@github.com:您的用户名/Pre_hospital_assistant_front.git

# 设置主分支名称
git branch -M main

# 推送到GitHub
git push -u origin main
```

### 🔐 SSH密钥配置（可选但推荐）

为了更方便地推送代码，建议配置SSH密钥：

#### 生成SSH密钥

```bash
# 生成SSH密钥
ssh-keygen -t ed25519 -C "您的邮箱地址"

# 启动ssh-agent
eval "$(ssh-agent -s)"

# 添加SSH密钥到ssh-agent
ssh-add ~/.ssh/id_ed25519

# 复制公钥到剪贴板
pbcopy < ~/.ssh/id_ed25519.pub
```

#### 添加到GitHub

1. 访问 GitHub Settings > SSH and GPG keys
2. 点击 "New SSH key"
3. 粘贴公钥内容
4. 点击 "Add SSH key"

### ✅ 验证上传成功

1. 访问您的GitHub仓库页面
2. 确认所有文件都已上传
3. 检查README.md是否正确显示
4. 查看项目结构是否完整

### 📁 项目文件结构

上传后，您的GitHub仓库应该包含以下主要文件和目录：

```
Pre_hospital_assistant_front/
├── README.md                    # 项目说明文档
├── .gitignore                   # Git忽略文件配置
├── upload_to_github.sh          # 自动化上传脚本
├── GITHUB_UPLOAD_GUIDE.md      # 本指南文档
├── src/                         # 前端源码
│   ├── components/              # Vue组件
│   ├── views/                   # 页面视图
│   ├── stores/                  # 状态管理
│   ├── router/                  # 路由配置
│   └── api/                     # API接口
├── backend/                     # 后端源码
│   ├── app/                     # FastAPI应用
│   ├── requirements.txt         # Python依赖
│   └── ...
├── docs/                        # 项目文档
├── public/                      # 静态资源
└── nginx/                       # Nginx配置
```

### 🎯 上传后的下一步

1. **完善项目信息**
   - 在GitHub仓库页面添加项目描述
   - 设置项目标签（Topics）
   - 添加项目网站链接（如果有）

2. **配置GitHub Pages（可选）**
   - 在仓库设置中启用GitHub Pages
   - 选择部署分支（通常是main）
   - 访问生成的网站地址

3. **邀请协作者（如果需要）**
   - 在仓库设置中添加协作者
   - 设置适当的权限级别

4. **设置分支保护（推荐）**
   - 保护main分支
   - 要求代码审查
   - 启用状态检查

### 🆘 常见问题解决

#### 问题1：Git命令不可用

**解决方案**：等待Xcode命令行工具安装完成

#### 问题2：推送失败

**可能原因**：

- 网络连接问题
- GitHub仓库未创建
- 权限不足
- SSH密钥未配置

**解决方案**：

```bash
# 检查远程仓库配置
git remote -v

# 重新配置远程仓库
git remote remove origin
git remote add origin https://github.com/用户名/仓库名.git

# 重新推送
git push -u origin main
```

#### 问题3：大文件上传失败

**解决方案**：

- 检查.gitignore文件是否正确配置
- 移除大文件或使用Git LFS

#### 问题4：SSH连接问题

**解决方案**：

```bash
# 测试SSH连接
ssh -T git@github.com

# 如果失败，重新配置SSH密钥
ssh-keygen -t ed25519 -C "邮箱地址"
```

### 📞 获取帮助

如果在操作过程中遇到问题：

1. 检查本指南的相关章节
2. 查看GitHub官方文档
3. 搜索相关错误信息
4. 联系项目维护者

---

**🎉 恭喜！** 完成这些步骤后，您的院前急救助手系统就成功上传到GitHub了！
