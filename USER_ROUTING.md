# 用户消息路由器

## 用户映射

```javascript
const USERS = {
  tech: {
    userId: "ou_5c7144a360f68b2db0e434749f5a9945",
    botId: "oc_f6d2e6388d34f539dd37a898b6cf00cc",
    name: "tech",
    label: "tech_feishu_dm",
    timezone: "Asia/Shanghai",
    github: "china10s"
  },
  wwn: {
    userId: "ou_725f66654653d6c7061d5f99eb8f4df7",
    botId: "oc_71e0965d0a667df9afb65f9bbcfb4453",
    name: "wwn",
    label: "wwn_feishu_dm",
    timezone: "Asia/Shanghai"
  }
};
```

## 路由逻辑

当主会话（agent:main:main）收到飞书消息时：

```javascript
// 1. 识别用户
const userId = message?.from || message?.origin?.from || "unknown";

// 2. 查找用户配置
const user = Object.values(USERS).find(u =>
  u.userId === userId ||
  `feishu:${u.userId}` === userId
);

// 3. 如果是已知用户，spawn 子会话
if (user) {
  sessions_spawn({
    task: `你是 ${user.name} 的 AI 助手。

用户信息：
- 名称：${user.name}
- 用户ID：${user.userId}
- 时区：${user.timezone}
${user.github ? `- GitHub：${user.github}` : ""}

任务：
处理用户的消息，并以正常风格回复。
直接回复即可，不需要返回 JSON 或其他格式。

原始消息：
${messageText || message}`,
    label: user.label,
    agentId: "main",
    model: "zai/glm-4.7",
    runTimeoutSeconds: 120,
    cleanup: "keep"
  });

  // 主会话不回复，让子会话处理
  return "SUBAGENT_ROUTED";
}
```

## 子会话配置

### tech 的子会话
- **Label:** `tech_feishu_dm`
- **Agent:** `main`
- **Model:** `zai/glm-4.7`
- **Timeout:** 120s
- **Cleanup:** `keep`（保留上下文）

### wwn 的子会话
- **Label:** `wwn_feishu_dm`
- **Agent:** `main`
- **Model:** `zai/glm-4.7`
- **Timeout:** 120s
- **Cleanup:** `keep`（保留上下文）

## 预期行为

### 场景 1：tech 发送消息
1. 飞书插件将消息路由到 `agent:main:main`
2. 主会话识别是 tech
3. 主会话 spawn `tech_feishu_dm` 子会话
4. 子会话处理并回复
5. **关键：** 子会话的回复如何发回飞书？

### 场景 2：wwn 发送消息
1. 飞书插件将消息路由到 `agent:main:main`
2. 主会话识别是 wwn
3. 主会话 spawn `wwn_feishu_dm` 子会话
4. 子会话处理并回复
5. **关键：** 子会话的回复如何发回飞书？

### 场景 3：并发消息
1. tech 和 wwn 同时发消息
2. 两个消息都到达 `agent:main:main`
3. 主会话串行处理消息
4. 但两个子会话会并发运行
5. **问题：** 回复顺序不确定

## 问题：子会话的回复路由

**当前未知：**
- 子会话完成后，回复会发到哪里？
- 会自动路由到飞书吗？
- 还是会发回主会话？

**需要测试：**
1. Spawn 子会话
2. 观察子会话的回复去向
3. 如果不自动路由，需要手动调用 message 工具

## 测试计划

- [ ] 测试 1：Spawn tech 子会话
- [ ] 测试 2：观察子会话回复的去向
- [ ] 测试 3：如果不自动路由，实现手动路由
- [ ] 测试 4：并发测试
