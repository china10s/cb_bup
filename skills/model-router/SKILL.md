---
name: model-router
description: 根据任务阶段自动切换模型
read_when:
  - 用户需要根据任务阶段（规划/实施/验收）自动选择不同模型
  - 规划阶段用高端模型
  - 实施阶段用低成本模型
  - 验收阶段用高端模型
metadata: {"version": "1.0"}
allowed-tools: Bash(*), sessions_spawn
---

# 智能模型路由

这个skill可以根据用户提供的任务阶段自动切换模型。

## 配置

在开始使用前，先配置好模型别名：

```bash
openclaw models aliases add 规划 anthropic/claude-opus-4.5
openclaw models aliases add 实施 zai/glm-4.7
openclaw models aliases add 验收 openai/gpt-5.2
```

## 使用方式

### 方式1：显式指定阶段

在对话中明确说明阶段：

```
[规划] 请帮我设计这个系统
[实施] 现在帮我写代码
[验收] 检查一下这个实现
```

### 方式2：任务阶段标签

使用以下标签格式：

```
#规划 任务描述
#实施 具体实现
#验收 检查结果
```

### 方式3：关键词检测

根据用户消息中的关键词自动选择：

**规划阶段关键词：**
- 设计、规划、架构、方案、strategy、design、plan

**实施阶段关键词：**
- 实现、代码、implementation、code、write、execute

**验收阶段关键词：**
- 检查、验收、review、check、verify、test

## 模型配置示例

### 配置文件结构

```bash
cat <<'EOF' > ~/.openclaw/openclaw.json
{
  "agent": {
    "model": {
      "primary": "anthropic/claude-opus-4.5",
      "fallbacks": [
        "openai/gpt-4.1",
        "zai/glm-4.7"
      ]
    }
  }
}
EOF
```

### 阶段对应模型

| 阶段 | 模型 | 特点 | 适用场景 |
|-------|------|------|---------|
| **规划** | Claude-Opus-4.5 | 最强推理 | 架构设计、方案规划 |
| **实施** | GLM-4.7 | 低成本中文 | 代码实现、文档编写 |
| **验收** | GPT-5.2 | 最强能力 | 代码审查、测试验证 |

## 实现逻辑

伪代码：

```javascript
function selectModel(message) {
  const phase = detectPhase(message);

  switch(phase) {
    case 'planning':
      return '规划';  // Claude-Opus-4.5
    case 'implementation':
      return '实施';  // GLM-4.7
    case 'review':
      return '验收';  // GPT-5.2
    default:
      return '规划';  // 默认高端
  }
}

function detectPhase(message) {
  // 规划阶段关键词
  const planningKeywords = ['设计', '规划', '架构', '方案', 'design', 'plan', 'strategy'];
  // 实施阶段关键词
  const implKeywords = ['实现', '代码', 'implementation', 'code', 'write', 'execute'];
  // 验收阶段关键词
  const reviewKeywords = ['检查', '验收', 'review', 'check', 'verify', 'test'];

  // 检查关键词
  for (const keyword of planningKeywords) {
    if (message.toLowerCase().includes(keyword)) return 'planning';
  }
  for (const keyword of implKeywords) {
    if (message.toLowerCase().includes(keyword)) return 'implementation';
  }
  for (const keyword of reviewKeywords) {
    if (message.toLowerCase().includes(keyword)) return 'review';
  }

  // 默认返回规划阶段
  return 'planning';
}
```

## 使用示例

### 示例1：规划阶段

**用户输入：**
```
#规划 我需要设计一个用户认证系统，包括登录、注册、密码重置等功能
```

**自动选择：** Claude-Opus-4.5（规划模型）

**系统行为：**
```bash
openclaw models set anthropic/claude-opus-4.5
```

### 示例2：实施阶段

**用户输入：**
```
#实施 根据上面的设计，帮我实现登录和注册功能
```

**自动选择：** GLM-4.7（实施模型）

**系统行为：**
```bash
openclaw models set zai/glm-4.7
```

### 示例3：验收阶段

**用户输入：**
```
#验收 检查一下实现的代码是否有问题，帮我review一下
```

**自动选择：** GPT-5.2（验收模型）

**系统行为：**
```bash
openclaw models set openai/gpt-5.2
```

## 成本优化

按项目周期计算成本：

假设一个项目：
- 规划阶段：100次调用 × $15/M tokens = $1.5
- 实施阶段：500次调用 × $0.5/M tokens = $2.5
- 验收阶段：50次调用 × $15/M tokens = $0.75

**总计：$4.75**

如果全部用高端模型：
- 650次调用 × $15/M tokens = $9.75

**节省：$5（50%成本）**

## 手动切换

如果自动检测不准，可以手动切换：

```bash
# 切换到规划模型
/model 规划

# 切换到实施模型
/model 实施

# 切换到验收模型
/model 验收
```

## 注意事项

1. **模型可用性**：确保配置的模型都有对应的API密钥
2. **上下文保持**：切换模型可能会丢失之前对话的上下文
3. **fallback机制**：主模型失败时，会自动尝试fallback中的模型
4. **测试配置**：使用 `openclaw models status` 检查配置是否正确

## 进阶：动态调整

可以结合项目规模进一步细化：

```javascript
function selectAdvancedModel(message, project) {
  const phase = detectPhase(message);

  if (phase === 'implementation') {
    // 根据项目大小选择不同的实施模型
    if (project.complexity === 'high') {
      return '实施复杂';  // GPT-4.1
    } else if (project.complexity === 'medium') {
      return '实施';  // GLM-4.7
    } else {
      return '实施简单';  // GPT-4o-mini
    }
  }

  // 规划和验收阶段始终用高端模型
  return '规划';  // Claude-Opus-4.5
}
```

## 总结

这个智能路由方案可以实现：
1. ✅ 根据任务阶段自动选择模型
2. ✅ 规划和验收用高端模型（保证质量）
3. ✅ 实施阶段用低成本模型（节省成本）
4. ✅ 支持手动干预
5. ✅ 保持成本可控

开始使用前，先确保：
1. 配置好API密钥
2. 添加模型别名
3. 测试各模型是否可用
