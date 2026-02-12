---
name: video-summary
description: 视频内容智能总结与信息聚合技能
read_when:
  - 用户需要分析YouTube视频内容
  - 从多个来源获取信息（NoteGPT转录、B站文案、小红书等）
  - 整合所有来源生成最终summary
metadata: {"version": "1.0"}
allowed-tools: Bash(*), WebFetch(*), agent-browser
---

# 视频内容智能总结技能

这个skill可以智能聚合来自多个来源的视频信息，生成完整的中文总结。

## 核心功能

### 1. 多渠道信息获取
- **NoteGPT音频转录** - 获取完整的逐字对话
- **B站文案** - 从up主发布的文字稿
- **小红书笔记** - 收集用户分享的重点
- **其他平台** - 知乎专栏、公众号文章等

### 2. 智能信息整合
- 自动识别重复内容
- 按时间线整理对话
- 提取关键观点和金句
- 关联不同来源的信息

### 3. 结构化输出
- 生成summary markdown文档
- 包含关键信息、时间线、核心观点
- 突出争议点和有趣事实

## 使用方式

### 方式1：直接分析YouTube视频

输入视频URL，自动调用NoteGPT获取转录：

```
请分析视频：https://www.youtube.com/watch?v=xxxxx
```

### 方式2：多渠道聚合

提供多个来源的信息：

```
视频URL：https://www.youtube.com/watch?v=xxxxx
B站文案：[可选项]
小红书笔记链接：[可选项]
其他来源：[可选项]
```

### 方式3：已有转录处理

如果有现成的文本稿，直接处理：

```
现有转录文本：
[粘贴文本]
```

## 技能实现

### NoteGPT集成
- 使用agent-browser打开NoteGPT
- 粘贴YouTube链接
- 点击生成总结
- 等待处理完成
- 提取逐字转录内容

### B站文案获取
- 使用web_fetch获取up主页
- 提取专栏或动态中的文案
- 识别视频ID和标题

### 小红书信息收集
- 搜索视频相关笔记
- 提取高赞内容
- 收集用户评论要点

### 信息整合算法
```javascript
function integrateSources(transcript, biliText, xiaohongshu) {
  // 1. 提取关键信息
  const keyPoints = extractKeyPoints(transcript);

  // 2. 时间线整理
  const timeline = buildTimeline(transcript);

  // 3. 识别金句
  const quotes = extractQuotes(transcript);

  // 4. 去重和合并
  const mergedInfo = mergeInfo(transcript, biliText, xiaohongshu);

  // 5. 生成summary
  return generateSummary(mergedInfo);
}
```

## 输出格式

生成的summary包含：

### 1. 视频基本信息
- 标题
- 时长
- 频道
- 发布时间
- 观看次数

### 2. 核心主题
- 列出3-5个核心主题
- 每个主题用一句话概括

### 3. 详细时间线
- 按时间顺序整理对话内容
- 标注重要转折点

### 4. 关键观点
- 每个参与者的重要观点
- 数据支撑的具体信息

### 5. 金句收录
- 最精彩的10-15句原话
- 注明发言人和背景

### 6. 争议点
- 引发讨论的观点
- 可能的误解或争议

### 7. 数据验证
- 从多个来源交叉验证
- 标注信息可信度

### 8. 生成摘要
- 300-500字的简明摘要
- 涵盖所有核心内容

### 9. 延伸阅读
- 相关视频推荐
- 背景资料链接
- 深入分析文章

### 10. 文件保存
- 保存markdown文件到指定目录
- 格式：`yyyyMMdd_<title>_summary.md`

## 使用示例

### 示例1：单渠道分析
```
用户：请分析 https://www.youtube.com/watch?v=oCZyBAApyMo
系统：
1. 使用NoteGPT获取音频转录
2. 整理对话内容
3. 生成summary文档
4. 保存到video_summary目录
```

### 示例2：多渠道聚合
```
用户：请总结 https://www.youtube.com/watch?v=xxxxx
系统：
1. 检查B站是否有该视频文案
2. 搜索小红书相关笔记
3. 调用NoteGPT获取音频转录
4. 整合所有来源信息
5. 生成综合summary
```

### 示例3：已有转录处理
```
用户：我这里有一段视频的文本稿
系统：
1. 整理时间线
2. 提取关键点
3. 生成结构化summary
```

## 注意事项

### 信息来源标注
- 必须明确标注每个信息块的来源
- 优先级：NoteGPT转录 > B站文案 > 小红书笔记 > 其他来源
- 对于冲突的信息，标注"存在不同说法"

### 内容准确性
- 尽量使用原话，避免过度改写
- 保留数据、金额、时间等精确信息
- 对于不确定的内容，标注"根据推测"

### 版权与使用
- 仅供个人学习和研究使用
- 不得用于商业目的
- 保留原作者署名信息

## 技术栈

### 前端
- agent-browser：访问网页和NoteGPT
- web_fetch：获取B站、小红书等平台内容

### 后端
- node.js：信息处理和整合
- markdown生成：创建结构化文档

### 文件系统
- 保存路径：`/root/.openclaw/workspace/video_summary/`
- 文件命名：`YYYYMMDD_<video_title>_summary.md`

## 扩展性

### 支持更多平台
- 知乎专栏获取
- 微博内容抓取
- 头条号文章处理

### 高级功能
- 视频帧提取（关键截图）
- 字幕时间戳同步
- 多语言翻译（英文转中文）

### 数据库存储
- SQLite存储历史summary
- 按作者、主题、日期索引
- 支持快速检索

## 未来展望

### AI增强总结
- 使用AI模型（Claude/GPT-4）理解内容
- 生成深度分析和评论
- 自动提取洞察和趋势

### 多媒体处理
- 音频转录（使用Whisper）
- 视频关键帧识别
- 生成信息图

### 协作功能
- 多人同时分析视频
- 实时共享笔记和讨论
- 版本控制和差异对比

---

这个skill将持续迭代，提供更强大的视频内容分析能力。
