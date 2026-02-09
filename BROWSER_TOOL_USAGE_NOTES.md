# Browser 工具使用与 justrl 搜索备忘录

**创建时间：** 2026-02-09 14:15 UTC

**核心任务：** 记录 Browser 工具的限制和使用经验，以及 justrl 相关搜索的真实含义。

---

## 🔧 Browser 工具技术限制

### 1. ❌ 验证失败（多次出现）

**错误信息：**
```json
{
  "error": "Validation failed for tool \"browser\"",
  "message": "action: must be equal to one of allowed values"
}
```

**遇到的失败 Action：**
- ❌ `search` - 不在白名单中
- ❌ `goto` - 不在白名单中
- ❌ `navigate` - 不在白名单中

**根因：** Browser 工具具有严格的白名单验证机制，只允许特定的 action 值。

### 2. ✅ 允许的 Actions（根据文档）

根据 OpenClaw 官方文档，Browser 工具只允许以下 Actions：
- `status` - 检查服务状态
- `start` - 启动浏览器
- `stop` - 停止浏览器
- `tabs` - 列出标签页
- `tab` - 标签页管理
- `focus` - 聚焦到标签页
- `close` - 关闭标签页
- `click` - 点击元素
- `type` - 输入文本
- `drag` - 拖拽元素
- `select` - 选择元素
- `snapshot` - 截图
- `screenshot` - 屏幕截图
- `pdf` - 生成 PDF
- `evaluate` - 执行 JavaScript
- `wait` - 等待条件满足

### 3. ⚠️ 不允许的 Actions（当前限制）

**以下 Action 目前不支持或验证失败：**
- ❌ `navigate` - 导航到指定 URL
- ❌ `search` - 执行搜索操作
- ❌ `goto` - 跳转到指定页面
- ❌ 任何其他未列在白名单中的 action

**这意味着：** 无法使用 Browser 工具进行自由的网页导航、搜索或查看页面内容。

---

## 🔍 justrl 搜索的真实含义

### 1. ⚠️ 用户可能记错了术语

**百度搜索结果：** `justrl` 的直接结果很少，主要指向 **JustRL**（清华大学开发的极简强化学习框架）。

**可能的情况：**
- 用户想搜索的是 "justrl 博客" 或 "Justrl.com"
- 但搜索结果显示的是 JustRL 相关内容

### 2. ✅ JustRL 的核心概念

**全称：** JustRL (Just Reinforcement Learning)

**核心理念：**
- **极简主义（Minimalism）** - "Less is more"（少即是多，多即是少）
- **单阶段训练** - 摒弃复杂的多阶段训练和动态调参，只用单阶段训练和固定超参数
- **固定超参数** - 避免复杂的探索策略，保持 1.5B 参数规模（150 亿）不变
- **GRPO（群组相对策略优化）** - 使用简单的二元奖励（做对得分，不做错零分），而不是复杂的奖励函数
- **计算效率** - 只需复杂方法 50% 的计算资源，在 1.5B 模型上达到顶尖性能

**技术优势：**
- **性能突破：** 在 DeepSeek-R1-Distill-Qwen-1.5B 模型上，平均准确率从 28% 提升至 **54.87%**
- **资源节省：** 计算量仅为 ProRL-V2 的 **50%**
- **稳定性：** 4000 步无崩溃，奖励曲线单调上升
- **训练效率：** 用最简单的方法实现了 SOTA 性能

---

## 💡 经验总结

### 1. Browser 工具使用建议

**❌ 不要尝试使用受限的 Action：**
- `navigate`、`search`、`goto` 目前不支持
- 继续尝试只会失败并浪费 Token

**✅ 推荐的 Actions：**
- `tabs` - 查看当前打开的标签页
- `snapshot` - 获取页面快照（虽然可能不是可读的搜索结果）
- `status` - 检查服务是否正在运行

### 2. 外部搜索建议

**如果需要搜索 justrl 或 JustRL：**
- 使用 `web_fetch` 工具 - 可以直接获取网页内容并解析为 Markdown
- 使用 `exec` 工具运行 `curl` 命令
- 在本地浏览器中手动搜索 - 如果你有本地 Chrome 或其他浏览器环境

---

## 📋 下一步行动

**如果遇到类似困难：**
1. **先检查 Browser 工具状态** - `browser status`
2. **尝试 `web_fetch`** - 获取文档或特定网页内容
3. **使用 `exec`** - 运行本地命令（如 `curl`）
4. **参考本文档** - https://docs.openclaw.ai/tools/browser

**如果需要查找特定信息：**
- JustRL 官方论文：https://arxiv.org/abs/2512.16649v1
- 清华大学官网：https://www.tsinghua.edu
- 上海 AI 实验室官网：https://www.shlab.org
- 相关新闻报道或博客文章

---

## 🚀 关键教训

1. **Browser 工具有严格限制**
   - 白名单验证机制导致 `navigate` 和 `search` Action 不可用
   - 需要找到文档中列出的允许 Actions 并使用它们

2. **justrl 不是一个独立的搜索词**
   - 搜索结果主要指向 JustRL 框架
   - 它代表 "Just Reinforcement Learning"，不是 "justrl" 这个博客

3. **快照（Snapshot）不等于可读内容**
   - Browser 工具返回的快照只是页面结构的描述（如 textbox、img 等）
   - 无法像人类一样“阅读”搜索结果或网页的具体内容

---

## 📝 结论

**tech，我已经将这次的经验整理成备忘录并保存到文件。**

**下次遇到困难时，我会：**
1. **检查此备忘录**
2. **避免重复使用受限的 Action**
3. **优先使用可用的 Actions**（如 `tabs`、`status`、`snapshot`）
4. **使用 `web_fetch` 或 `exec` 进行外部搜索**

**备忘录已保存到：** `/root/.openclaw/workspace/BROWSER_TOOL_USAGE_NOTES.md`

**希望你满意这次的记录！** 🎉