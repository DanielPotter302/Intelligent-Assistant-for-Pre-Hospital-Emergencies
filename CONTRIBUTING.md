# 贡献指南

感谢您对院前急救助手系统的关注！我们欢迎所有形式的贡献，包括但不限于：

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复
- ✨ 开发新功能

## 🚀 快速开始

### 1. Fork 项目

1. 点击页面右上角的 "Fork" 按钮
2. 克隆您的 Fork 到本地：

```bash
git clone https://github.com/YOUR_USERNAME/pre-hospital-assistant.git
cd pre-hospital-assistant
```

### 2. 设置开发环境

请参考 [开发环境搭建指南](./docs/development/setup.md) 配置本地开发环境。

### 3. 创建分支

```bash
# 创建并切换到新分支
git checkout -b feature/your-feature-name

# 或者修复bug
git checkout -b fix/bug-description
```

## 📋 贡献类型

### Bug 报告

在提交 Bug 报告前，请：

1. 检查是否已有相关 Issue
2. 确保使用最新版本
3. 提供详细的复现步骤

**Bug 报告模板**：

```markdown
## Bug 描述

简要描述遇到的问题

## 复现步骤

1. 进入页面...
2. 点击按钮...
3. 看到错误...

## 预期行为

描述您期望发生的情况

## 实际行为

描述实际发生的情况

## 环境信息

- 操作系统: [例如 Windows 11]
- 浏览器: [例如 Chrome 120]
- Node.js 版本: [例如 18.17.0]
- Python 版本: [例如 3.11.0]

## 附加信息

- 错误截图
- 控制台错误信息
- 相关日志
```

### 功能建议

**功能建议模板**：

```markdown
## 功能描述

简要描述建议的新功能

## 使用场景

描述什么情况下需要这个功能

## 解决方案

描述您认为的实现方案

## 替代方案

描述其他可能的实现方式

## 附加信息

- 相关截图或原型
- 参考资料链接
```

## 💻 代码贡献

### 代码规范

#### 前端代码规范

1. **Vue 组件**

   - 使用 Composition API
   - 组件名使用 PascalCase
   - 文件名使用 PascalCase
   - 使用 TypeScript

2. **代码风格**

   - 遵循 ESLint 配置
   - 使用 Prettier 格式化
   - 2 空格缩进
   - 单引号字符串

3. **命名规范**
   - 变量和函数使用 camelCase
   - 常量使用 UPPER_SNAKE_CASE
   - 类型定义使用 PascalCase

#### 后端代码规范

1. **Python 代码**

   - 遵循 PEP 8 规范
   - 使用类型注解
   - 4 空格缩进
   - 最大行长度 88 字符

2. **命名规范**

   - 变量和函数使用 snake_case
   - 类名使用 PascalCase
   - 常量使用 UPPER_SNAKE_CASE
   - 私有成员使用下划线前缀

3. **文档字符串**
   - 使用 Google 风格的 docstring
   - 为所有公共函数和类添加文档

### 提交规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<类型>[可选的作用域]: <描述>

[可选的正文]

[可选的脚注]
```

#### 提交类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式修改
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

#### 示例

```bash
feat(auth): 添加用户注册功能

- 实现用户注册API
- 添加邮箱验证
- 更新用户模型

Closes #123
```

### 代码审查

所有代码变更都需要通过代码审查：

1. **自我检查**

   - 代码符合规范
   - 添加必要的测试
   - 更新相关文档
   - 确保所有测试通过

2. **提交 PR**

   - 填写详细的 PR 描述
   - 关联相关 Issue
   - 添加适当的标签

3. **审查过程**
   - 至少需要 1 个审查者批准
   - 所有 CI 检查必须通过
   - 解决所有审查意见

## 🧪 测试要求

### 前端测试

```bash
# 运行单元测试
npm run test:unit

# 运行E2E测试
npm run test:e2e

# 生成测试覆盖率报告
npm run test:unit -- --coverage
```

### 后端测试

```bash
cd backend

# 运行所有测试
python -m pytest

# 运行特定测试
python -m pytest tests/test_auth.py

# 生成覆盖率报告
python -m pytest --cov=app --cov-report=html
```

### 测试要求

- 新功能必须包含单元测试
- 测试覆盖率不低于 80%
- 关键功能需要集成测试
- API 变更需要更新测试用例

## 📝 文档贡献

### 文档类型

1. **API 文档** - 接口说明和示例
2. **用户文档** - 功能使用指南
3. **开发文档** - 技术实现说明
4. **部署文档** - 部署和运维指南

### 文档规范

- 使用 Markdown 格式
- 包含完整的示例代码
- 提供清晰的截图说明
- 保持文档与代码同步更新

## 🔄 开发流程

### 1. 准备工作

```bash
# 同步最新代码
git checkout main
git pull upstream main

# 创建功能分支
git checkout -b feature/your-feature
```

### 2. 开发过程

```bash
# 定期提交代码
git add .
git commit -m "feat: 添加新功能"

# 推送到远程分支
git push origin feature/your-feature
```

### 3. 提交 PR

1. 在 GitHub 上创建 Pull Request
2. 填写 PR 模板
3. 等待代码审查
4. 根据反馈修改代码
5. 合并到主分支

### 4. 清理工作

```bash
# 删除本地分支
git branch -d feature/your-feature

# 删除远程分支
git push origin --delete feature/your-feature
```

## 🏷️ Issue 和 PR 标签

### Issue 标签

- `bug` - Bug 报告
- `enhancement` - 功能增强
- `documentation` - 文档相关
- `good first issue` - 适合新手
- `help wanted` - 需要帮助
- `priority: high` - 高优先级
- `priority: low` - 低优先级

### PR 标签

- `feature` - 新功能
- `bugfix` - Bug 修复
- `docs` - 文档更新
- `refactor` - 代码重构
- `breaking change` - 破坏性变更

## 🎯 开发优先级

### 高优先级

- 安全漏洞修复
- 关键功能 Bug 修复
- 性能优化
- 用户体验改进

### 中优先级

- 新功能开发
- 代码重构
- 测试覆盖率提升
- 文档完善

### 低优先级

- 代码风格优化
- 依赖更新
- 开发工具改进

## 🤝 社区准则

### 行为准则

我们致力于为所有人提供友好、安全和欢迎的环境，请：

- 使用友好和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

### 沟通方式

- **GitHub Issues** - Bug 报告和功能建议
- **GitHub Discussions** - 一般讨论和问答
- **Pull Requests** - 代码审查和讨论
- **邮件** - 私人或敏感问题

## 📞 获取帮助

如果您在贡献过程中遇到问题，可以：

1. 查看 [FAQ](./docs/FAQ.md)
2. 搜索现有的 Issues
3. 在 GitHub Discussions 中提问
4. 联系项目维护者

## 🙏 致谢

感谢所有为项目做出贡献的开发者！您的贡献让这个项目变得更好。

---

再次感谢您的贡献！🎉
