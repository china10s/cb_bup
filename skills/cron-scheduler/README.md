# Cron Scheduler - OpenClaw 定时任务管理

这个 skill 提供了完整的 OpenClaw cron 任务管理指南，帮助你创建、管理和调试定时任务。

## 📁 文件结构

```
cron-scheduler/
├── SKILL.md          # 完整的 skill 文档
├── README.md         # 本文件
└── examples.sh       # 示例脚本
```

## 🎯 快速开始

### 1. 查看所有任务

```bash
cron list --includeDisabled
```

### 2. 创建一个简单的定时任务

**需求**: 每天北京时间 2 点提醒同步到 GitHub

**实现**:
```json
{
  "name": "Daily GitHub Sync",
  "schedule": {
    "kind": "cron",
    "expr": "0 18 * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "REMINDER: Run git sync"
  },
  "sessionTarget": "main",
  "enabled": true
}
```

### 3. 时区转换

**重要**: OpenClaw cron 使用 UTC 时间！

| 北京时间 | UTC 时间 | 说明 |
|---------|---------|------|
| 02:00 | 18:00 (前一天) | 深夜 |
| 08:00 | 00:00 | 凌晨 |
| 12:00 | 04:00 | 上午 |
| 20:30 | 12:30 | 下午 |

**公式**: UTC = 北京时间 - 8 小时

## 📚 核心概念

### 任务类型

1. **systemEvent**: 向主会话注入事件
   - 用于: 简单提醒、命令执行
   - 要求: sessionTarget = "main"

2. **agentTurn**: 运行独立子会话
   - 用于: 复杂任务、发送消息
   - 要求: sessionTarget = "isolated"

### 调度类型

1. **cron**: 使用 cron 表达式
   ```json
   {"kind": "cron", "expr": "0 18 * * *", "tz": "UTC"}
   ```

2. **at**: 一次性任务
   ```json
   {"kind": "at", "at": "2026-02-10T14:00:00Z"}
   ```

3. **every**: 间隔执行
   ```json
   {"kind": "every", "everyMs": 3600000}
   ```

## 🛠️ 常用命令

### 列出任务
```bash
cron list --includeDisabled
```

### 添加任务
```bash
cron add --job '{"name": "...", ...}'
```

### 更新任务
```bash
cron update <jobId> --patch '{"enabled": false}'
```

### 删除任务
```bash
cron remove <jobId>
```

### 运行任务（测试）
```bash
cron run <jobId>
```

### 查看历史
```bash
cron runs <jobId>
```

## 💡 实际案例

### 案例 1: 每天 2 点同步 GitHub

```json
{
  "name": "Daily GitHub Sync",
  "schedule": {
    "kind": "cron",
    "expr": "0 18 * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "REMINDER: cd /root/.openclaw/workspace && git add -A && git commit -m '例行化备份' && git push origin main"
  },
  "sessionTarget": "main",
  "enabled": true
}
```

### 案例 2: 每天 20:30 给 tech 发消息

```json
{
  "name": "Daily tech reminder",
  "schedule": {
    "kind": "cron",
    "expr": "30 12 * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "给tech (ou_5c7144a360f68b2db0e434749f5a9945) 发送飞书消息：要下班了。使用 message tool 发送。"
  },
  "sessionTarget": "isolated",
  "enabled": true,
  "delivery": {
    "mode": "announce"
  }
}
```

### 案例 3: 一次性会议提醒

```json
{
  "name": "Meeting Reminder",
  "schedule": {
    "kind": "at",
    "at": "2026-02-10T14:00:00Z"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "会议提醒：下午 2 点的技术评审"
  },
  "sessionTarget": "main",
  "enabled": true
}
```

## ⚠️ 常见问题

### Q: 为什么任务没有执行？

1. 检查时区是否正确（UTC vs 北京时间）
2. 检查任务是否启用（enabled: true）
3. 查看 cron 运行历史：`cron runs <jobId>`

### Q: 如何调试任务？

1. 手动运行测试：`cron run <jobId>`
2. 设置 delivery 模式：
   ```json
   {"delivery": {"mode": "announce"}}
   ```
3. 查看 gateway 日志

### Q: 如何修改任务时间？

```bash
cron update <jobId> --patch '{
  "schedule": {
    "kind": "cron",
    "expr": "30 12 * * *",
    "tz": "UTC"
  }
}'
```

### Q: 如何删除任务？

```bash
cron remove <jobId>
```

**注意**: 删除任务后，记得从脚本中移除对该 ID 的引用。

## 📖 Cron 表达式参考

```
* * * * *
│ │ │ │ │
│ │ │ │ └─ 星期几 (0-6, 0=周日)
│ │ │ └─── 月份 (1-12)
│ │ └───── 日期 (1-31)
│ └─────── 小时 (0-23)
└───────── 分钟 (0-59)
```

**常用表达式**:

| 表达式 | 含义 |
|--------|------|
| `0 0 * * *` | 每天 00:00 |
| `0 18 * * *` | 每天 18:00 |
| `30 12 * * *` | 每天 12:30 |
| `0 */2 * * *` | 每 2 小时 |
| `0 0 * * 1` | 每周一 00:00 |
| `0 0 1 * *` | 每月 1 日 00:00 |
| `0 9 * * 1-5` | 工作日 09:00 |

## 🔗 相关资源

- [OpenClaw 文档](https://docs.openclaw.ai)
- [Cron 表达式生成器](https://crontab.guru/)
- [SKILL.md](./SKILL.md) - 完整文档
- [examples.sh](./examples.sh) - 示例脚本

## 📝 更新日志

- **2026-02-09**: 初始版本，支持基本的 cron 任务管理
  - 支持三种调度类型（cron, at, every）
  - 支持两种任务类型（systemEvent, agentTurn）
  - 包含时区转换指南和实际案例
