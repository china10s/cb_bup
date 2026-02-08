# 飞书消息路由工作流

## 用户识别映射

```javascript
const USER_MAP = {
  "ou_5c7144a360f68b2db0e434749f5a9945": {
    name: "tech",
    botId: "oc_f6d2e6388d34f539dd37a898b6cf00cc",
    label: "tech_feishu_dm"
  },
  "ou_725f66654653d6c7061d5f99eb8f4df7": {
    name: "wwn",
    botId: "oc_71e0965d0a667df9afb65f9bbcfb4453",
    label: "wwn_feishu_dm"
  }
};
```

## 消息处理流程

### 流程 A：主会话直接处理（当前方案）

```
收到飞书消息
    ↓
识别用户（通过 origin.from）
    ↓
在主会话中回复
    ↓
飞书插件发送回复
```

**优点：**
- 简单可靠
- 回复自动路由

**缺点：**
- 串行处理
- 共享会话上下文

### 流程 B：子会话并发处理（目标方案）

```
收到飞书消息
    ↓
识别用户
    ↓
Spawn 子会话（sessions_spawn）
    ↓
子会话处理消息
    ↓
子会话返回结果（delivery.announce）
    ↓
主会话收到结果
    ↓
主会话调用 message 工具发送回复到飞书
```

**优点：**
- 并发处理
- 独立会话上下文

**缺点：**
- 复杂
- 需要测试 delivery 机制

## 实现：流程 B

### 步骤 1：创建子会话任务描述

```javascript
function createUserTask(userId, userName, originalMessage) {
  return `
你正在处理 ${userName}（飞书用户ID：${userId}）的消息。

原始消息：
${originalMessage}

任务：
1. 理解用户的消息
2. 以你的正常风格回复
3. 返回格式必须严格遵循以下JSON：
   {
     "reply": "你的回复内容",
     "userId": "${userId}",
     "botId": "${USER_MAP[userId].botId}"
   }

注意：
- 只返回 JSON，不要有其他文字
- reply 字段是实际回复内容
- 不要泄露其他用户的信息
  `.trim();
}
```

### 步骤 2：Spawn 子会话

```javascript
sessions_spawn({
  task: createUserTask(userId, userName, message),
  label: USER_MAP[userId].label,
  agentId: "main",
  model: "zai/glm-4.7",
  runTimeoutSeconds: 60,
  cleanup: "keep"  // 保持子会话，保留上下文
})
```

### 步骤 3：处理子会话结果

主会话需要等待子会话完成，然后：

```javascript
// 1. 解析子会话返回的 JSON
const result = JSON.parse(subagentResponse);

// 2. 发送回复到飞书
message({
  channel: "feishu",
  action: "send",
  to: result.userId,
  message: result.reply
})
```

## 当前实施状态

**已实现：**
- ✅ 用户识别逻辑
- ✅ 子会话任务描述模板
- ✅ 测试文档

**待测试：**
- ⏳ sessions_spawn 的 delivery 机制
- ⏳ 子会话结果的处理流程
- ⏳ message 工具的调用

## 测试清单

- [ ] 测试 1：Spawn tech 的子会话，验证结果返回
- [ ] 测试 2：Spawn wwn 的子会话，验证结果返回
- [ ] 测试 3：验证主会话能收到子会话的 delivery
- [ ] 测试 4：验证 message 工具能正确发送到飞书
- [ ] 测试 5：并发测试 - 同时给两个用户发消息
