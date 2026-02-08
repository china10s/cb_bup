# 用户隔离实施计划

## 目标
实现 tech 和 wwn 的用户数据隔离，确保：
1. ✅ 每个用户有独立的上下文和记忆
2. ✅ 每个用户只能看到自己的信息
3. ✅ 每个用户的消息不被其他用户看到

## 当前状态
- ❌ 所有用户共享 `agent:main:main` 会话
- ❌ 所有用户的上下文混合在一起
- ⚠️ 子会话路由方案无法工作（测试证实）

## 实施方案：主会话 + 用户特定数据隔离

### 步骤 1：创建用户特定的记忆文件

**文件结构：**
```
/root/.openclaw/workspace/
├── memory/
│   ├── tech/
│   │   ├── 2026-02-08.md      # tech 的每日记录
│   │   ├── preferences.md      # tech 的偏好
│   │   └── reminders.md        # tech 的提醒
│   └── wwn/
│       ├── 2026-02-08.md      # wwn 的每日记录
│       ├── preferences.md      # wwn 的偏好
│       └── reminders.md        # wwn 的提醒
```

**实施命令：**
```bash
# 创建用户目录
mkdir -p /root/.openclaw/workspace/memory/tech
mkdir -p /root/.openclaw/workspace/memory/wwn

# 创建偏好文件
echo "# tech 的用户偏好" > /root/.openclaw/workspace/memory/tech/preferences.md
echo "# wwn 的用户偏好" > /root/.openclaw/workspace/memory/wwn/preferences.md

# 创建提醒文件
echo "# tech 的提醒任务" > /root/.openclaw/workspace/memory/tech/reminders.md
echo "# wwn 的提醒任务" > /root/.openclaw/workspace/memory/wwn/reminders.md
```

### 步骤 2：更新 USER.md

在 USER.md 中添加用户特定的数据路径：

```markdown
## 📝 用户数据路径

### tech
- **每日记录：** `memory/tech/YYYY-MM-DD.md`
- **用户偏好：** `memory/tech/preferences.md`
- **提醒任务：** `memory/tech/reminders.md`

### wwn
- **每日记录：** `memory/wwn/YYYY-MM-DD.md`
- **用户偏好：** `memory/wwn/preferences.md`
- **提醒任务：** `memory/wwn/reminders.md`

## 🤖 AI 行为规则

### 记录用户数据

**当记录信息时：**
1. 识别当前用户（通过 origin.from）
2. 将信息写入对应用户的文件：
   - 每日记录 → `memory/{user}/YYYY-MM-DD.md`
   - 偏好 → `memory/{user}/preferences.md`
   - 提醒 → `memory/{user}/reminders.md`

**示例：**
```javascript
const user = identifyUser(); // tech 或 wwn
const today = new Date().toISOString().split('T')[0];

// 记录每日记录
write({
  path: `/root/.openclaw/workspace/memory/${user}/${today}.md`,
  content: `## ${currentTime}\n\n用户消息：\n${message}\n\nAI 回复：\n${response}`
});
```

### 查询用户数据

**当查询信息时：**
1. 识别当前用户
2. 只读取该用户的文件
3. 不读取其他用户的文件

**示例：**
```javascript
const user = identifyUser();

// 读取用户偏好
const prefs = read({
  path: `/root/.openclaw/workspace/memory/${user}/preferences.md`
});

// 读取提醒任务
const reminders = read({
  path: `/root/.openclaw/workspace/memory/${user}/reminders.md`
});
```

### 隐私保护

**严格遵循：**
- ❌ 不在回复中提及其他用户
- ❌ 不读取其他用户的文件
- ❌ 不泄露其他用户的信息
- ✅ 只访问和回复当前用户的数据
```

### 步骤 3：更新 SOUL.md

在 SOUL.md 中添加用户隔离的行为指导：

```markdown
## 多用户行为

**隐私优先：**
- 每个用户都有独立的记忆空间
- 绝不泄露其他用户的信息
- 只处理当前用户的消息

**用户识别：**
- 通过 `origin.from` 识别用户
- tech: `ou_5c7144a360f68b2db0e434749f5a9945`
- wwn: `ou_725f66654653d6c7061d5f99eb8f4df7`

**数据隔离：**
- 每个用户有独立的文件目录：`memory/{user}/`
- 只读和写当前用户的文件
- 不要跨用户访问数据
```

### 步骤 4：实施脚本

创建一个自动化脚本来初始化用户数据：

```javascript
// /root/.openclaw/workspace/init-user-data.js

const fs = require('fs');
const path = require('path');

const USERS = {
  tech: {
    userId: "ou_5c7144a360f68b2db0e434749f5a9945",
    dir: "/root/.openclaw/workspace/memory/tech"
  },
  wwn: {
    userId: "ou_725f66654653d6c7061d5f99eb8f4df7",
    dir: "/root/.openclaw/workspace/memory/wwn"
  }
};

// 创建目录
for (const [user, config] of Object.entries(USERS)) {
  if (!fs.existsSync(config.dir)) {
    fs.mkdirSync(config.dir, { recursive: true });
    console.log(`✅ 创建目录：${config.dir}`);
  }
  
  // 创建偏好文件
  const prefsPath = path.join(config.dir, 'preferences.md');
  if (!fs.existsSync(prefsPath)) {
    fs.writeFileSync(prefsPath, `# ${user} 的用户偏好\n\n## 个人信息\n- 名称：${user}\n- 用户ID：${config.userId}\n\n## 偏好设置\n\n`, 'utf-8');
    console.log(`✅ 创建文件：${prefsPath}`);
  }
  
  // 创建提醒文件
  const remindersPath = path.join(config.dir, 'reminders.md');
  if (!fs.existsSync(remindersPath)) {
    fs.writeFileSync(remindersPath, `# ${user} 的提醒任务\n\n## 活跃提醒\n\n## 已完成提醒\n\n`, 'utf-8');
    console.log(`✅ 创建文件：${remindersPath}`);
  }
}

console.log('\n✅ 用户数据初始化完成！');
```

## 优点

**数据隔离：**
- ✅ 每个用户有独立的文件空间
- ✅ 用户数据完全隔离
- ✅ 不会发生数据泄露

**简单可靠：**
- ✅ 不需要修改飞书插件
- ✅ 不需要创建多个机器人
- ✅ 不需要复杂的路由机制

**可扩展：**
- ✅ 可以轻松添加更多用户
- ✅ 每个用户可以有独立的配置
- ✅ 支持用户特定的功能

## 缺点

**并发处理：**
- ❌ 仍然是串行处理
- ❌ 两个用户同时发消息，一个需要等待

**上下文隔离：**
- ⚠️ 虽然数据隔离了，但会话历史仍然混合
- ⚠️ 用户 A 可能会看到用户 B 的对话历史

## 后续优化

**如果需要真正的并发处理：**
1. 为每个用户创建独立的飞书机器人
2. 每个机器人有独立的会话
3. 实现真正的并发和隔离

**长期方案：**
1. 联系飞书插件开发者
2. 请求实现 `dmScope` 支持
3. 实现真正的会话隔离
