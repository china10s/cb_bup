# OpenClaw 多模型智能路由配置指南

## 概述

在OpenClaw中实现多模型API配置和智能路由，可以根据任务难度自动选择不同的模型。

## 一、配置多个模型

### 1.1 基本配置结构

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "agent": {
    "model": {
      "primary": "openai/gpt-5.2",
      "fallbacks": [
        "openai/gpt-4.1",
        "anthropic/claude-sonnet-4.5",
        "zai/glm-4.7"
      ]
    },
    "imageModel": {
      "primary": "openai/gpt-4.1-vision",
      "fallbacks": [
        "anthropic/claude-3.5-sonnet-20240620"
      ]
    },
    "models": {
      // 允许的模型白名单
      "openai/gpt-5.2": {
        "alias": "GPT-5.2-高级"
      },
      "openai/gpt-4.1": {
        "alias": "GPT-4.1-标准"
      },
      "anthropic/claude-opus-4.5": {
        "alias": "Claude-Opus-最强"
      },
      "anthropic/claude-sonnet-4.5": {
        "alias": "Claude-Sonnet-平衡"
      },
      "zai/glm-4.7": {
        "alias": "GLM-4.7-国产"
      }
    }
  },
  "models": {
    "providers": {
      "openai": {
        "apiKey": "${OPENAI_API_KEY}",
        "baseUrl": "https://api.openai.com/v1"
      },
      "anthropic": {
        "apiKey": "${ANTHROPIC_API_KEY}"
      },
      "zai": {
        "apiKey": "${ZAI_API_KEY}",
        "baseUrl": "https://open.bigmodel.cn/api/paas/v4/"
      }
    }
  }
}
```

### 1.2 环境变量配置

在 `~/.openclaw/.env` 中存储API密钥：

```bash
# OpenAI
OPENAI_API_KEY=sk-proj-xxx

# Anthropic
ANTHROPIC_API_KEY=sk-ant-xxx

# ZAI (智谱AI）
ZAI_API_KEY=your-zai-api-key

# DeepSeek
DEEPSEEK_API_KEY=sk-deepseek-xxx

# OpenRouter (多模型聚合）
OPENROUTER_API_KEY=sk-or-v1-xxx
```

## 二、智能路由实现

### 2.1 使用命令行切换模型

根据任务难度手动切换：

```bash
# 简单任务（使用GLM-4.7，经济实惠）
openclaw models set zai/glm-4.7

# 中等任务（使用GPT-4.1）
openclaw models set openai/gpt-4.1

# 复杂任务（使用Claude-Opus）
openclaw models set anthropic/claude-opus-4.5

# 编程任务（使用GPT-5.2）
openclaw models set openai/gpt-5.2
```

### 2.2 在聊天中使用模型选择

用户可以在对话中指定模型：

```
/model 2        # 选择模型2（从列表）
/model gpt        # 使用别名
/model openai/gpt-5.2    # 使用完整模型名
/model claude-opus  # 使用别名
```

### 2.3 配置模型别名

```bash
# 添加别名
openclaw models aliases add 简单 zai/glm-4.7
openclaw models aliases add 中等 openai/gpt-4.1
openclaw models aliases add 复杂 anthropic/claude-opus-4.5
openclaw models aliases add 编程 openai/gpt-5.2
openclaw models aliases add 代码审查 openai/gpt-4.2

# 列出别名
openclaw models aliases list
```

### 2.4 配置Fallback链

当主模型失败时，自动尝试备用模型：

```json
{
  "agent": {
    "model": {
      "primary": "openai/gpt-5.2",
      "fallbacks": [
        "anthropic/claude-sonnet-4.5",
        "openai/gpt-4.1"
      ]
    }
  }
}
```

## 三、按难度分类的模型配置

### 3.1 推荐配置方案

```json
{
  "agent": {
    "model": {
      "primary": "openai/gpt-4.1",
      "fallbacks": [
        "anthropic/claude-sonnet-4.5",
        "zai/glm-4.7"
      ]
    },
    "models": {
      // Level 1: 简单任务
      "openai/gpt-4o-mini": {
        "alias": "简单",
        "description": "快速、低成本"
      },
      "zai/glm-4-flash": {
        "alias": "快速",
        "description": "极速响应"
      },

      // Level 2: 中等任务
      "openai/gpt-4.1": {
        "alias": "标准",
        "description": "平衡性能和成本"
      },
      "anthropic/claude-3-5-sonnet-20240620": {
        "alias": "平衡",
        "description": "适合推理"
      },
      "zai/glm-4.7": {
        "alias": "国产",
        "description": "中文优化"
      },

      // Level 3: 复杂任务
      "openai/gpt-5.2": {
        "alias": "高级",
        "description": "最强推理能力"
      },
      "anthropic/claude-opus-4.5": {
        "alias": "最强",
        "description": "顶级性能"
      },
      "openrouter/anthropic/claude-3.7-sonnet": {
        "alias": "sonnet",
        "description": "长文本处理"
      },

      // Level 4: 特殊任务
      "openai/gpt-4.1-vision": {
        "alias": "视觉",
        "description": "图像理解"
      },
      "openai/o1-preview": {
        "alias": "推理",
        "description": "复杂推理"
      }
    }
  }
}
```

## 四、使用场景示例

### 4.1 任务难度判断

在代码中判断任务难度并选择模型：

```javascript
// 示例：根据token数量或任务类型选择模型
function selectModelForTask(task) {
  const { type, complexity, tokens } = analyzeTask(task);

  // 简单任务：快速、低成本模型
  if (complexity === 'low' && tokens < 1000) {
    return 'openai/gpt-4o-mini';  // 或 /model 简单
  }

  // 中等任务：平衡模型
  if (complexity === 'medium' || tokens < 8000) {
    return 'openai/gpt-4.1';  // 或 /model 标准
  }

  // 复杂任务：高级模型
  if (complexity === 'high' || tokens > 8000) {
    return 'anthropic/claude-opus-4.5';  // 或 /model 最强
  }

  // 编程任务
  if (type === 'coding') {
    return 'openai/gpt-5.2';  // 或 /model 编程
  }

  // 图像任务
  if (type === 'vision') {
    return 'openai/gpt-4.1-vision';  // 或 /model 视觉
  }

  // 默认
  return 'anthropic/claude-sonnet-4.5';  // 或 /model 平衡
}
```

### 4.2 成本优化配置

```json
{
  "agent": {
    "model": {
      "primary": "zai/glm-4.7",
      "fallbacks": [
        "openai/gpt-4o-mini",
        "openai/gpt-4.1"
      ]
    }
  }
}
```

**优势：**
- 主模型使用国产GLM-4.7，成本低，中文优化
- Fallback到GPT-4o-mini（超快、超便宜）
- 最后才使用GPT-4.1（标准）

### 4.3 性能优化配置

```json
{
  "agent": {
    "model": {
      "primary": "anthropic/claude-opus-4.5",
      "fallbacks": [
        "openai/gpt-5.2",
        "anthropic/claude-sonnet-4.5"
      ]
    }
  }
}
```

**优势：**
- 主模型Claude-Opus，顶级推理能力
- Fallback到GPT-5.2和Sonnet

### 4.4 使用OpenRouter聚合多个模型

OpenRouter提供统一接口访问多个模型，自动路由到最优提供商：

```json
{
  "models": {
    "providers": {
      "openrouter": {
        "apiKey": "${OPENROUTER_API_KEY}",
        "baseUrl": "https://openrouter.ai/api/v1"
      }
    }
  },
  "agent": {
    "model": {
      "primary": "openrouter/anthropic/claude-3.7-sonnet",
      "fallbacks": [
        "openrouter/openai/gpt-5.2",
        "openrouter/google/gemini-pro-1.5"
      ]
    }
  }
}
```

**优势：**
- 一个API Key访问多个模型
- 自动选择最优提供商
- 成本透明，支持fallback

## 五、常用命令

### 5.1 模型管理命令

```bash
# 查看当前模型状态
openclaw models status

# 列出所有可用模型
openclaw models list --all

# 切换模型
openclaw models set <provider/model>

# 添加fallback
openclaw models fallbacks add <provider/model>

# 列出fallback
openclaw models fallbacks list

# 清除fallback
openclaw models fallbacks clear

# 管理别名
openclaw models aliases add <alias> <provider/model>
openclaw models aliases list
openclaw models aliases remove <alias>
```

### 5.2 查看模型性能

```bash
# 查看详细状态（包括auth、endpoint等）
openclaw models status
```

## 六、推荐配置方案

### 方案A：成本优先（适合大批量任务）

```json
{
  "agent": {
    "model": {
      "primary": "zai/glm-4.7",
      "fallbacks": ["openai/gpt-4o-mini", "openai/gpt-4.1"]
    }
  }
}
```

**成本排序：** GLM-4.7 < GPT-4o-mini < GPT-4.1

### 方案B：性能优先（适合复杂任务）

```json
{
  "agent": {
    "model": {
      "primary": "anthropic/claude-opus-4.5",
      "fallbacks": ["openai/gpt-5.2", "anthropic/claude-sonnet-4.5"]
    }
  }
}
```

**性能排序：** Claude-Opus > GPT-5.2 > Claude-Sonnet

### 方案C：平衡方案（推荐）

```json
{
  "agent": {
    "model": {
      "primary": "anthropic/claude-sonnet-4.5",
      "fallbacks": [
        "openai/gpt-4.1",
        "zai/glm-4.7",
        "openai/gpt-4o-mini"
      ]
    }
  }
}
```

**特点：**
- 主模型：Sonnet（性能/成本平衡）
- Fallback：GPT-4.1（标准）→ GLM-4.7（中文优化）→ GPT-4o-mini（极速/超便宜）

### 方案D：多场景专用模型

```json
{
  "agent": {
    "model": {
      "primary": "openai/gpt-4.1"
    },
    "imageModel": {
      "primary": "openai/gpt-4.1-vision"
    }
  },
  "models": {
    "openai/gpt-4o-mini": {
      "alias": "快速"
    },
    "zai/glm-4.7": {
      "alias": "中文"
    },
    "anthropic/claude-opus-4.5": {
      "alias": "复杂"
    },
    "openai/gpt-5.2": {
      "alias": "编程"
    }
  }
}
```

## 七、环境变量配置文件

创建 `~/.openclaw/.env`：

```bash
# OpenAI
OPENAI_API_KEY=sk-proj-xxx

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-xxx

# ZAI (智谱AI）
ZAI_API_KEY=your-zai-key

# DeepSeek
DEEPSEEK_API_KEY=sk-deepseek-xxx

# OpenRouter (可选，聚合平台）
OPENROUTER_API_KEY=sk-or-v1-xxx

# Google Gemini
GOOGLE_API_KEY=your-google-key
```

## 八、快速开始

### 8.1 使用配置向导

```bash
# 运行向导自动配置
openclaw onboard
```

### 8.2 应用配置

```bash
# 应用配置
openclaw gateway config.apply < config-file.json
```

## 九、注意事项

1. **模型引用规范**：使用 `provider/model` 格式，如 `openai/gpt-4.1`
2. **别名选择**：在 `agents.defaults.models` 中添加，可以使用短别名如 `/model gpt`
3. **Fallback链**：按优先级配置，先经济后性能
4. **API密钥安全**：使用环境变量存储，不要直接写在配置文件中
5. **测试配置**：使用 `openclaw models status` 检查配置是否正确
6. **成本控制**：优先使用低成本模型，复杂任务才用高级模型
7. **多模型聚合**：考虑使用OpenRouter等聚合服务简化配置

## 十、示例对话流程

### 简单任务
```
用户: 总结这篇文章
系统: 使用 GLM-4.7（默认）
AI: [返回总结]
```

### 中等任务
```
用户: 分析这段代码的问题
系统: 使用 GPT-4.1（中等）
AI: [返回分析]
```

### 复杂任务
```
用户: 设计一个完整的架构方案
系统: 使用 Claude-Opus（复杂）
AI: [返回方案]
```

### 手动指定模型
```
用户: /model 编程
系统: 切换到 GPT-5.2
用户: 写一个Python爬虫
AI: [使用GPT-5.2生成代码]
```

### 自动Fallback
```
系统: 尝试 GPT-4.1...
系统: 请求失败，尝试 Sonnet...
AI: [使用Sonnet返回结果]
```

## 总结

通过以上配置，你可以：

1. ✅ 配置多个模型API密钥
2. ✅ 设置智能fallback链
3. ✅ 根据任务难度选择模型
4. ✅ 使用别名快速切换
5. ✅ 优化成本和性能平衡
6. ✅ 在对话中动态调整模型

开始使用：
```bash
openclaw models status
openclaw models list --all
/model <alias>
```
