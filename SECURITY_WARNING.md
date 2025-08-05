# ⚠️ 安全警告

## 🚨 当前配置仅适用于开发/演示环境

### 问题说明
当前系统使用了 `dangerouslyAllowBrowser: true` 配置，允许在浏览器中直接调用 DeepSeek API。

### ⚠️ 安全风险
- API 密钥暴露在客户端代码中
- 任何人都可以查看和使用您的 API 密钥
- 可能导致意外的 API 费用

### 📋 生产环境解决方案

#### 方案1：后端代理（推荐）
```javascript
// 前端调用后端接口
const response = await fetch('/api/triage', {
  method: 'POST',
  body: JSON.stringify(triageData)
})

// 后端处理（Node.js/Python/等）
app.post('/api/triage', async (req, res) => {
  const openai = new OpenAI({
    baseURL: 'https://api.deepseek.com',
    apiKey: process.env.DEEPSEEK_API_KEY  // 服务器环境变量
  })
  
  const result = await openai.chat.completions.create({...})
  res.json(result)
})
```

#### 方案2：Serverless函数
- 使用 Vercel Functions
- 使用 Netlify Functions  
- 使用 AWS Lambda

#### 方案3：环境变量保护
```javascript
// 仅在开发环境暴露API密钥
const apiKey = import.meta.env.DEV ? 
  'your-dev-key' : 
  undefined  // 生产环境不包含密钥
```

### 🎯 当前演示目的
本系统用于展示智能分诊功能的前端实现，在实际部署时需要：

1. 将 API 调用移至后端
2. 使用环境变量管理密钥
3. 移除 `dangerouslyAllowBrowser` 配置

### 💡 临时解决方案
如果您需要立即测试，可以：
1. 使用临时/测试 API 密钥
2. 限制 API 密钥的使用额度
3. 测试完成后立即更换密钥 