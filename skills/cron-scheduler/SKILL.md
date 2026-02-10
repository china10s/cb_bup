---
name: Cron Scheduler
description: Manage OpenClaw cron jobs for scheduled tasks, reminders, and automated workflows. Supports timezone-aware scheduling, system events, and isolated agent turns.
read_when:
  - Creating scheduled tasks or reminders
  - Setting up automated backups or syncs
  - Creating recurring notifications
  - Managing periodic workflows
metadata: {"clawdbot":{"emoji":"⏰","requires":{"tools":["cron"]}}}
allowed-tools: cron(*)
---

# Cron Scheduler

OpenClaw 的 cron 系统用于创建和管理定时任务。支持一次性提醒、周期性任务、自动降级确保送达。

## 基本概念

### 任务类型

1. **systemEvent**: 向主会话注入系统事件（提醒、命令）
   - 适用于：简单提醒、需要主会话上下文的任务
   - sessionTarget 必须是 `main`

2. **agentTurn**: 运行一个独立的子 agent 会话
   - 适用于：复杂的自动化任务、发送消息、API 调用
   - sessionTarget 必须是 `isolated`

### 调度类型

1. **at**: 一次性任务，指定绝对时间
   ```json
   {"kind": "at", "at": "2026-02-10T02:00:00Z"}
   ```

2. **every**: 周期性任务，间隔执行
   ```json
   {"kind": "every", "everyMs": 86400000, "anchorMs": 0}
   ```

3. **cron**: 使用 cron 表达式
   ```json
   {"kind": "cron", "expr": "0 18 * * *", "tz": "UTC"}
   ```

## 🔒 焊死的配置规则（必须遵守）

以下规则基于 OpenClaw 官方文档和实际使用经验，创建任务时必须严格遵守：

### 1. 时区必须明确指定

```json
"schedule": {
  "kind": "cron",
  "expr": "0 18 * * *",
  "tz": "UTC"  // 必须！如果省略，使用 Gateway 主机时区
}
```

**规则**:
- **必须明确指定 `tz`**，避免依赖主机默认值
- 文档明确：ISO 时间戳省略时区时，被视为 UTC
- 北京时间 = UTC + 8 小时

### 2. sessionTarget 与 payload.kind 必须匹配

```json
// ✅ 正确：main + systemEvent
{
  "sessionTarget": "main",     // 必须是 main
  "payload": {
    "kind": "systemEvent"       // 必须是 systemEvent
  }
}

// ✅ 正确：isolated + agentTurn
{
  "sessionTarget": "isolated",  // 必须是 isolated
  "payload": {
    "kind": "agentTurn"        // 必须是 agentTurn
  }
}
```

**规则**:
- **sessionTarget 必须是 "main" 或 "isolated" 并且必须匹配 payload.kind**
- main → systemEvent
- isolated → agentTurn

### 3. agentTurn 必须有 message 字段

```json
// ✅ 正确
{
  "payload": {
    "kind": "agentTurn",
    "message": "明确的执行指令"  // agentTurn 必须有 message
  }
}

// ❌ 错误
{
  "payload": {
    "kind": "agentTurn"
    // 缺少 message
  }
}
```

**规则**:
- agentTurn 的 payload **必须包含 message 字段**
- message 是执行的指令内容

### 4. delivery 配置（isolated jobs 必须）

```json
{
  "delivery": {
    "mode": "announce",        // 必须设置（announce 或 none）
    "channel": "feishu",      // 可选：指定频道
    "to": "ou_xxx...",         // 可选：指定接收者
    "bestEffort": true         // 可选：避免发送失败导致任务失败
  }
}
```

**规则**:
- **delivery 只对 isolated jobs 有效**
- 如果省略 delivery，OpenClaw 默认为 "announce"
- delivery.mode 可以是 "announce" 或 "none"

### 5. wakeMode 控制

```json
"wakeMode": "now"              // 立即触发 heartbeat（默认）
"wakeMode": "next-heartbeat"    // 等待下一个计划 heartbeat
```

**规则**:
- 对于 main session jobs，wakeMode 控制心跳何时触发
- 对于 isolated jobs，wakeMode 控制主会话摘要何时发布
- 默认是 "now"

### 6. 执行指令必须明确

```json
// ❌ 错误：模糊提醒
{
  "message": "提醒：执行 git 同步"
}

// ✅ 正确：直接执行
{
  "message": "执行以下操作：\n1. cd /root/.openclaw/workspace\n2. git add -A\n3. git commit -m '例行化备份'\n4. git push origin main\n\n完成后报告结果。"
}
```

**规则**:
- **payload.message 必须是执行指令，不是提醒**
- 必须包含完整的步骤，不要做一半
- 子 agent 会直接执行这些指令

### 7. 消息发送参数完整

```json
// ✅ 必须包含所有参数
{
  "message": "使用 message tool 发送飞书消息，参数如下：\n- action: send\n- channel: feishu\n- to: ou_5c7144a360f68b2db0e434749f5a9945\n- message: 要下班了\n\n发送成功后报告结果。"
}
```

**规则**:
- 发送飞书消息必须指定：action, channel, to, message
- 使用 message tool，不要用 exec/curl

### 8. 任务命名规范

```json
// ✅ 清晰描述性
"name": "Daily GitHub Sync"
"name": "Daily tech reminder"

// ❌ 模糊
"name": "task1"
"name": "job2"
```

**规则**:
- **name 必须是清晰、描述性的**
- 格式：`<频率> <功能> <对象>`
- 例如：Daily GitHub Sync, Hourly Email Check, Weekly Backup

### 9. deleteAfterRun（一次性任务）

```json
// 一次性任务默认自动删除
"deleteAfterRun": true  // 默认值

// 如果需要保留
"deleteAfterRun": false  // 会禁用但不删除
```

**规则**:
- **一次性任务（schedule.kind = "at"）默认在成功后删除**
- 设置为 false 会禁用任务但不删除

## 时区处理

**重要**: OpenClaw cron 默认使用 UTC，需要手动转换时区。

**北京时间 (UTC+8) 转换**:
- 减去 8 小时
- 例如：北京时间 02:00 → UTC 18:00 (前一天)
- 例如：北京时间 20:30 → UTC 12:30 (当天)

**快速转换表**:

| 北京时间 | UTC 时间 | Cron 表达式 (UTC) |
|---------|---------|------------------|
| 00:00 | 16:00 (前一天) | `0 16 * * *` |
| 02:00 | 18:00 (前一天) | `0 18 * * *` |
| 08:00 | 00:00 | `0 0 * * *` |
| 12:00 | 04:00 | `0 4 * * *` |
| 18:00 | 10:00 | `0 10 * * *` |
| 20:30 | 12:30 | `30 12 * * *` |
| 23:59 | 15:59 | `59 15 * * *` |

## 创建任务

### 列出所有任务

```bash
cron list --includeDisabled
```

### 创建 systemEvent 任务（简单提醒）

```json
{
  "name": "Daily Backup Reminder",
  "schedule": {
    "kind": "cron",
    "expr": "0 18 * * *",
    "tz": "UTC"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "REMINDER: Run daily backup - cd /root/workspace && ./backup.sh"
  },
  "sessionTarget": "main",
  "enabled": true
}
```

**使用场景**:
- 提醒主会话执行某项操作
- 需要访问主会话上下文
- 简单的命令执行

### 创建 agentTurn 任务（独立执行）

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

**使用场景**:
- 发送消息到外部系统
- 复杂的自动化流程
- 不需要主会话上下文的任务

### 创建一次性任务

```json
{
  "name": "One-time reminder",
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

## 管理任务

### 查看任务列表

```bash
cron list --includeDisabled
```

### 查看任务运行历史

```bash
cron runs <jobId>
```

### 立即运行任务

```bash
cron run <jobId>
```

### 更新任务

```bash
cron update <jobId> --patch '{"enabled": false}'
```

### 删除任务

```bash
cron remove <jobId>
```

## 实际案例

### 案例 1: 每天 2 点同步到 GitHub

**需求**: 北京时间每天 02:00 自动同步工作区到 GitHub

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
    "text": "REMINDER: Run git sync - cd /root/.openclaw/workspace && git add -A && git commit -m '例行化备份' && git push origin main"
  },
  "sessionTarget": "main",
  "enabled": true
}
```

**说明**:
- 北京时间 02:00 = UTC 18:00 (前一天)
- 使用 systemEvent 类型，提醒主会话执行 git 操作
- 任务会在每天 UTC 18:00 触发

### 案例 2: 每天 20:30 给 tech 发消息

**需求**: 北京时间每天 20:30 给 tech 发送"要下班了"

**实现**:
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

**说明**:
- 北京时间 20:30 = UTC 12:30
- 使用 agentTurn 类型，在独立会话中发送消息
- delivery.mode 设置为 "announce"，会将结果通知回请求者
- 消息包含 tech 的飞书 User ID

### 案例 3: 每小时检查邮件

**需求**: 每小时检查一次未读邮件

**实现**:
```json
{
  "name": "Hourly Email Check",
  "schedule": {
    "kind": "every",
    "everyMs": 3600000
  },
  "payload": {
    "kind": "agentTurn",
    "message": "检查未读邮件，如果有重要邮件立即通知用户。"
  },
  "sessionTarget": "isolated",
  "enabled": true
}
```

## 最佳实践

### 1. 时区转换

**始终指定时区**:
```json
"schedule": {
  "kind": "cron",
  "expr": "0 18 * * *",
  "tz": "UTC"  // 明确指定
}
```

**提前计算**: 在创建任务前计算好 UTC 时间，避免运行时错误。

### 2. 任务类型选择

**使用 systemEvent 当**:
- 需要主会话上下文
- 任务简单，只是提醒
- 需要访问会话内存

**使用 agentTurn 当**:
- 需要独立执行环境
- 任务复杂，可能需要多个步骤
- 需要发送消息到外部系统

### 3. 消息发送

**明确指定接收者**:
- 飞书消息需要 `to` 参数（User ID）
- 使用 message tool 发送，不要用 exec/curl

**示例**:
```javascript
message(action="send", to="ou_5c7144a360f68b2db0e434749f5a9945", message="要下班了")
```

### 4. 任务命名

**使用清晰、描述性的名称**:
- ✅ "Daily GitHub Sync"
- ✅ "Daily tech reminder"
- ✅ "Hourly Email Check"
- ❌ "task1", "job2", "cron3"

### 5. 错误处理

**检查任务是否存在**:
- 如果任务 ID 不存在，cron.run 会返回错误
- 删除任务后，记得从脚本或配置中移除引用

**查看任务历史**:
```bash
cron runs <jobId>
```

## 常见问题

### Q: 为什么任务没有执行？

**可能原因**:
1. 时区计算错误（北京时间忘减 8 小时）
2. 任务被禁用（enabled: false）
3. 任务已被删除
4. cron 服务未运行

**排查步骤**:
```bash
# 1. 检查任务列表
cron list --includeDisabled

# 2. 检查任务运行历史
cron runs <jobId>

# 3. 手动触发测试
cron run <jobId>

# 4. 检查 cron 状态
cron status
```

### Q: 如何调试任务执行？

**方法 1: 使用 agentTurn 并设置 delivery**
```json
{
  "delivery": {
    "mode": "announce"
  }
}
```

**方法 2: 查看 gateway 日志**
```bash
tail -f /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | grep cron
```

### Q: 一次性任务和周期性任务如何选择？

**一次性任务 (at)**:
- 会议提醒
- 临时通知
- 特定时间的一次性操作

**周期性任务 (cron/every)**:
- 日常备份
- 定期检查
- 周期性报告

### Q: 如何修改任务的执行时间？

**更新 schedule 部分**:
```bash
cron update <jobId> --patch '{
  "schedule": {
    "kind": "cron",
    "expr": "30 12 * * *",
    "tz": "UTC"
  }
}'
```

## Cron 表达式参考

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

## 注意事项

1. **时区**: OpenClaw cron 使用 UTC，必须手动转换
2. **ID 引用**: 删除任务后，记得清理引用该 ID 的脚本
3. **任务类型**: main 只能用 systemEvent，isolated 只能用 agentTurn
4. **消息发送**: 使用 message tool，不要用 exec/curl
5. **任务历史**: 定期检查任务运行历史，确保任务正常执行

## 🔒 焊死检查清单

创建任务时，必须逐项确认以下要点：

- [ ] **时区已明确指定**（tz: "UTC"）
- [ ] **时区已正确转换**（北京时间 - 8 小时）
- [ ] **sessionTarget 与 payload.kind 匹配**
  - [ ] main + systemEvent
  - [ ] isolated + agentTurn
- [ ] **agentTurn 包含 message 字段**
- [ ] **payload 是执行指令**，不是提醒
- [ ] **delivery 配置正确**（isolated jobs 必须）
  - [ ] delivery.mode 设置为 "announce" 或 "none"
  - [ ] delivery.channel 已指定（如需要）
  - [ ] delivery.to 已指定（如需要）
- [ ] **wakeMode 设置正确**（now 或 next-heartbeat）
- [ ] **消息发送包含完整的 channel/to 参数**
- [ ] **name 是清晰描述性的**
- [ ] **enabled 为 true**
- [ ] **一次性任务的 deleteAfterRun 设置正确**
- [ ] **所有参数都从 OpenClaw 文档确认过**

## 完整模板（焊死版本）

```json
{
  "name": "清晰的任务名称",           // 规则 8
  "schedule": {
    "kind": "cron",
    "expr": "cron表达式",            // 规则 1
    "tz": "UTC"                     // 规则 1：必须明确指定
  },
  "payload": {
    "kind": "agentTurn",              // 规则 2：必须匹配 sessionTarget
    "message": "直接执行的指令"      // 规则 3：必须有 message
                                      // 规则 6：必须是执行指令，不是提醒
  },
  "sessionTarget": "isolated",         // 规则 2：必须匹配 payload.kind
  "wakeMode": "next-heartbeat",       // 规则 5
  "enabled": true,                   // 检查项
  "delivery": {                     // 规则 4
    "mode": "announce",              // 规则 4
    "channel": "feishu",             // 可选
    "to": "ou_xxx..."              // 规则 7：消息发送必须完整
  }
}
```

**对于一次性任务**:
```json
{
  "name": "One-time reminder",
  "schedule": {
    "kind": "at",
    "at": "2026-02-10T14:00:00Z",
    "tz": "UTC"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "会议提醒"
  },
  "sessionTarget": "main",
  "enabled": true,
  "deleteAfterRun": true              // 规则 9：默认自动删除
}
```

## 相关工具

- `cron status` - 检查 cron 服务状态
- `cron list` - 列出所有任务
- `cron add` - 创建新任务
- `cron update` - 更新任务
- `cron remove` - 删除任务
- `cron run` - 立即运行任务
- `cron runs` - 查看任务历史
