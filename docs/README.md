# 项目文档

本目录包含院前急救助手系统的完整文档。

## 📁 文档结构

```
docs/
├── api/                    # API接口文档
│   ├── auth.md            # 用户认证API
│   ├── triage.md          # 智能分诊API
│   ├── emergency.md       # 应急指导API
│   ├── chat.md            # 智能问答API
│   └── knowledge.md       # 知识库API
├── deployment/            # 部署相关文档
│   ├── docker.md          # Docker部署指南
│   ├── production.md      # 生产环境部署
│   └── monitoring.md      # 监控和日志
├── development/           # 开发相关文档
│   ├── setup.md           # 开发环境搭建
│   ├── coding-standards.md # 代码规范
│   └── testing.md         # 测试指南
└── user/                  # 用户手册
    ├── user-guide.md      # 用户使用指南
    └── admin-guide.md     # 管理员指南
```

## 📖 快速导航

### API 文档

- [用户认证 API](./api/auth.md) - 注册、登录、令牌管理
- [智能分诊 API](./api/triage.md) - AI 分诊分析功能
- [应急指导 API](./api/emergency.md) - 紧急情况处理指导
- [智能问答 API](./api/chat.md) - AI 医疗问答功能
- [知识库 API](./api/knowledge.md) - 医疗知识库管理

### 部署指南

- [Docker 部署](./deployment/docker.md) - 容器化部署方案
- [生产环境部署](./deployment/production.md) - 生产环境配置
- [监控和日志](./deployment/monitoring.md) - 系统监控方案

### 开发指南

- [开发环境搭建](./development/setup.md) - 本地开发环境配置
- [代码规范](./development/coding-standards.md) - 编码标准和最佳实践
- [测试指南](./development/testing.md) - 单元测试和集成测试

### 用户手册

- [用户使用指南](./user/user-guide.md) - 系统功能使用说明
- [管理员指南](./user/admin-guide.md) - 系统管理和配置

## 🔄 文档更新

文档会随着系统功能的更新而持续维护。如果发现文档中的错误或需要补充的内容，请：

1. 提交 Issue 描述问题
2. 或直接提交 Pull Request 修正
3. 联系项目维护者

## 📝 文档规范

- 使用 Markdown 格式编写
- 遵循统一的文档结构和样式
- 包含完整的示例代码
- 及时更新版本信息
- 提供中英文对照（如需要）

---

最后更新时间：2024-01-01
