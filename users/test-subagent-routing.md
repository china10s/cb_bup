# 子会话路由测试

## 测试目标

验证使用 `sessions_spawn` 创建的子会话能否正确回复到飞书消息。

## 测试步骤

### 1. 创建测试子会话

```javascript
sessions_spawn({
  task: "你好！这是一个测试。请直接回复'测试成功'",
  label: "test_routing",
  agentId: "main",
  model: "zai/glm-4.7",
  runTimeoutSeconds: 30
})
```

### 2. 检查结果

- 子会话是否创建成功？
- 子会话的结果是否发回主会话？
- 结果中是否包含"测试成功"？

### 3. 如果子会话无法自动回复

**问题：** 子会话的回复无法自动路由到飞书

**解决方案 A：** 子会话返回结构化结果，主会话再发送到飞书

```javascript
sessions_spawn({
  task: "处理消息，并以JSON格式返回：{\"reply\": \"你的回复内容\", \"to\": \"用户ID\"}",
  label: "tech_feishu_dm",
  agentId: "main"
})

// 主会话收到结果后，解析 JSON，再调用 message 工具
message({
  channel: "feishu",
  action: "send",
  to: result.to,
  message: result.reply
})
```

**解决方案 B：** 子会话直接调用 message 工具（如果子会话有权限）

```javascript
sessions_spawn({
  task: "处理消息，并使用 message 工具直接回复到飞书",
  label: "tech_feishu_dm",
  agentId: "main"
})
```

## 当前状态

### 测试 1：基础测试（已执行）

**时间：** 2026-02-08 03:38 UTC

**操作：**
```javascript
sessions_spawn({
  task: "返回 JSON: {\"reply\": \"测试成功\"}",
  label: "test_routing",
  agentId: "main"
})
```

**结果：**
- ✅ 子会话创建成功
- ✅ Child Session Key: `agent:main:subagent:e13ed7f3-7300-42a3-b4f6-c2f674241114`
- ✅ Run ID: `7d287e29-0afb-4157-8112-97fd194f0047`
- ⏳ 等待子会话完成和 delivery 通知
- ⏳ sessions_list 未显示子会话（可能还在运行）

### 测试 2：用户特定的子会话

**待执行**
- Spawn tech 的子会话
- Spawn wwn 的子会话

### 测试 3：并发测试

**待执行**
- 同时给两个用户发消息
- 验证子会话是否并发处理

## 待测试

- [x] 测试 1：基础子会话创建
- [ ] 测试 1.1：等待子会话 delivery 通知
- [ ] 测试 1.2：验证 delivery 内容格式
- [ ] 测试 2：Spawn tech 的子会话
- [ ] 测试 3：Spawn wwn 的子会话
- [ ] 测试 4：验证主会话能收到子会话的 delivery
- [ ] 测试 5：验证 message 工具能正确发送到飞书
- [ ] 测试 6：并发测试 - 同时给两个用户发消息
