# 文件整理说明

## 日期
2026-02-12

## 变更内容

### 1. 删除的文件夹
- `skills/SKILLS/` - 空文件夹，已删除

### 2. 融合的文件
- `difficulty_response_strategy.md` → 已融合到 `FIXED_RULES.md`（作为规则3：困难应对策略）

### 3. 移动的文件

#### XHS 相关脚本 → `skills/video-summary/scripts/xhs/`
- `xhs_direct.py`
- `xhs_playwright.py`
- `xhs_scraper.py`
- `xhs_test2.py`
- `notegpt_snapshot_raw.json`

#### YouTube 相关脚本 → `skills/video-summary/scripts/youtube/`
- `download_subs.py`
- `get_transcript.py`
- `get_transcript_v2.py`
- `get_transcript_v3.py`
- `get_transcript_v4.py`

#### Playwright 相关脚本 → `skills/agent-browser/scripts/`
- `playwright_correct.py`
- `playwright_note.py`
- `playwright_sync.py`
- `openclaw_note.py`

#### 工具项目 → `tools/`
- `XHS-Downloader/` - 小红书下载工具（完整项目）
- `YouTube-Subtitle-Downloader/` - YouTube 字幕下载工具（完整项目）

### 4. 删除的文件
- `xhs_full_response.html` - 临时测试文件
- `xhs_playwright_full.html` - 临时测试文件

## 新的目录结构

```
workspace/
├── skills/
│   ├── video-summary/
│   │   ├── scripts/
│   │   │   ├── xhs/          # 小红书相关脚本
│   │   │   └── youtube/      # YouTube 相关脚本
│   │   └── SKILL.md
│   └── agent-browser/
│       ├── scripts/          # Playwright 测试脚本
│       └── SKILL.md
├── tools/
│   ├── XHS-Downloader/       # 小红书下载工具
│   └── YouTube-Subtitle-Downloader/
└── FIXED_RULES.md             # 已包含困难应对策略
```

## 注意事项

1. **依赖路径**：如果其他文件引用了这些脚本，需要更新导入路径
2. **Git 跟踪**：XHS-Downloader 和 YouTube-Subtitle-Downloader 是独立的 Git 仓库
3. **脚本用途**：这些脚本大部分是测试脚本，供开发调试使用

## 后续优化建议

1. 在 `video-summary` skill 的 SKILL.md 中添加脚本使用说明
2. 清理不再需要的测试脚本
3. 将可复用的功能提取为独立模块
