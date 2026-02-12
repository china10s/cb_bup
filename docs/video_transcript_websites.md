# YouTube视频文稿获取网站列表

## 可爬取平台

以下网站可以尝试获取YouTube视频的文稿：

### 1. **B站（哔哩哔哩）**
- **网址**：https://www.bilibili.com
- **方法**：
  - 视频页面通常有"更多"按钮，点击后可找到"字幕"或"稿件"
  - 可以通过API获取：https://api.bilibili.com/x/v2/view?aid=视频ID&bvid=分PID
- **脚本格式**：B站通常提供JSON格式字幕

### 2. **公众号文案提取**
- **网址**：搜索 `mp.weixin.qq.com/<文章ID>`
- **方法**：
  - 直接在浏览器中打开文章页面
  - 查看页面源代码，文案通常在 `<script>` 标签中
  - 使用正则表达式提取：`<script[^>]*>([\\s\\S]*?)</script>`
  - 或者查看页面DOM中的文案容器

### 3. **YouTube自动字幕**
- **工具**：yt-dlp
- **命令**：`yt-dlp --write-subs --write-auto-subs --skip-download --sub-lang zh-Hans,zh-Hant,en "视频URL"`
- **问题**：需要认证或cookies
- **替代方案**：
  - 使用 `--cookies-from-browser chrome`
  - 使用 `--cookies-from-browser brave`
  - 导出浏览器cookies：Chrome设置 > 隐私和安全 > Cookies和网站数据 > 导出

### 4. **第三方字幕下载网站**
#### YouTube Subtitle Downloader
- **网址**：https://youtubesubtititledownloader.com/
- **方法**：粘贴视频链接，下载SRT或VTT格式字幕

#### SaveSubs
- **网址**：https://savesubs.com/
- **方法**：下载字幕（包括翻译）

#### Downsub
- **网址**：https://downsub.com/

### 5. **YouTube Data API**
- **需要**：YouTube Data API v3 (Project: YouTube Report)
- **申请地址**：https://console.cloud.google.com/apis/credentials
- **功能**：可以获取视频详细信息、字幕、评论等
- **限制**：需要审核，有配额

### 6. **YouTube IFrame API**
- **功能**：嵌入视频页面获取内容
- **限制**：需要API密钥，有配额
- **实现难度**：中等

### 7. **字幕转换工具**
#### 字幕转文本
- **工具**：ffmpeg
- **命令**：`ffmpeg -i input.srt -f srt -c:v text -c:a copy -t 00:00:10 -vn 1`
- **提取音频**：`ffmpeg -i input.mp4 -vn 1 -f mp3 -ab 192k -vn 1 -c:a copy output.mp3`
- **音频转文字**：使用Whisper等AI工具

### 8. **AI转录服务**
#### AssemblyAI
- **网址**：https://www.assemblyai.com/
- **功能**：音频转录、说话人识别、情感分析
- **优势**：高准确率、支持多语言
- **成本**：按分钟计费

#### Sonix AI
- **网址**：https://sonix.ai/
- **功能**：实时转录、字幕生成
- **优势**：快速响应、API接入

#### Otter.ai
- **网址**：https://otter.ai/
- **功能**：AI转录、编辑、导出
- **优势**：针对会议优化

### 9. **网页抓取工具**
#### Puppeteer
- **工具**：Puppeteer（无头Chrome）
- **优点**：可以执行JavaScript、绕过部分反爬
- **方法**：
  - 启动无头浏览器
  - 访问视频页面
  - 执行JavaScript提取字幕元素
  - 保存为JSON或文本

#### Playwright
- **工具**：Playwright（Python库）
- **优点**：支持多浏览器、强大的选择器
- **方法**：
  - 编写Python脚本
  - 模拟用户操作
  - 提取字幕、文案等元素

#### Selenium
- **工具**：Selenium（Python库）
- **优点**：成熟、文档丰富
- **方法**：
  - 编写爬虫脚本
  - 定位字幕元素
  - 批量处理多个视频

### 10. **综合建议

#### 最可靠的方法（按推荐顺序）
1. **YouTube Data API v3** - 最官方、最可靠
2. **yt-dlp + cookies** - 开源、功能强大
3. **NoteGPT登录** - AI转录、总结
4. **AI转录服务** - AssemblyAI、Sonix AI等
5. **网页抓取** - 最后手段，可能被封

#### 注意事项
- 遵守YouTube ToS（服务条款）
- 不要过度请求，避免IP被封
- 使用cookies时注意隐私和合规
- 对于商业用途，考虑购买授权

## 实现代码示例

### 使用yt-dlp提取字幕
```bash
#!/bin/bash

VIDEO_URL="https://www.youtube.com/watch?v=xxxxx"

# 提取字幕（包括自动生成和人工上传）
yt-dlp --write-subs --write-auto-subs --skip-download --sub-lang zh-Hans,zh-Hant,en "$VIDEO_URL"

# 仅下载字幕（不下载视频）
yt-dlp --write-subs --write-auto-subs --skip-download "$VIDEO_URL"

# 下载所有可用字幕
yt-dlp --list-subs --write-auto-subs "$VIDEO_URL"
```

### 使用NoteGPT获取转录
```python
from playwright.sync_api import PlaywrightContext

# 启动Playwright
with Playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # 访问NoteGPT
    page.goto("https://notegpt.io/youtube-video-summarizer")
    
    # 等待页面加载
    page.wait_for_load_state("networkidle")
    
    # 粘贴视频链接
    page.fill('input[placeholder*="Paste YouTube video link"]', "https://www.youtube.com/watch?v=xxxxx')
    
    # 点击生成总结
    page.click('button:has-text("Generate Summary")')
    
    # 等待处理完成（可能需要几分钟）
    page.wait_for_timeout(300000)  # 5分钟超时
    
    # 获取转录内容
    transcript = page.evaluate("""
        const transcriptTab = document.querySelector('tab:has-text("Transcript")');
        if (transcriptTab) {
            transcriptTab.click();
            return new Promise(resolve => setTimeout(resolve, 2000));
        }
        return document.querySelector('div[role="log"]')?.innerText;
    """)
    
    print("Transcript:", transcript)
    
    browser.close()
```

### B站文案提取（Python示例）
```python
import requests
from bs4 import BeautifulSoup
import re
import json

def get_bili_script(video_id):
    # 方式1: 直接API获取（需要权限）
    api_url = f"https://api.bilibili.com/x/v2/view?aid={video_id}&bvid="
    response = requests.get(api_url)
    data = response.json()
    
    # 方式2: 网页抓取
    page_url = f"https://www.bilibili.com/video/{video_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取文案（可能在script标签中）
    scripts = soup.find_all('script')
    script_content = ""
    
    for script in scripts:
        script_content += str(script)
    
    # 使用正则表达式提取JSON数据
    pattern = r'window\.__INITIAL_STATE__\s*=\{.*?\}'
    matches = re.findall(pattern, script_content)
    
    for match in matches:
        try:
            data = json.loads(match.replace('window.__INITIAL_STATE__', '').replace(';', ''))
            # 提取视频信息
            if 'videoData' in data:
                title = data['videoData']['title']
                desc = data['videoData']['desc']
                
                print(f"标题: {title}")
                print(f"描述: {desc}")
                
        except:
            pass
    
    return {
        "title": "B站视频",
        "transcript": script_content
    }

# 使用示例
# result = get_bili_script("BV1xx4117xxxxx")
# print(json.dumps(result, ensure_ascii=False, indent=2))
```

## 文件保存路径
### Linux/macOS
```bash
mkdir -p ~/youtube_transcripts
cd ~/youtube_transcripts
```

### Windows
```powershell
New-Item -ItemType Directory -Path "C:\Users\YourName\youtube_transcripts"
```

## 持久化存储方案

### 使用SQLite存储
```python
import sqlite3

def save_transcript_to_db(video_id, platform, transcript, summary=""):
    conn = sqlite3.connect('transcripts.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            platform TEXT NOT NULL,
            title TEXT,
            transcript TEXT,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        INSERT INTO transcripts (video_id, platform, title, transcript, summary, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    ''', (video_id, platform, "", transcript, summary))
    
    conn.commit()
    conn.close()
    
    print(f"已保存字幕到数据库: {video_id}")
```

## 浏览器Cookies导出指南

### Chrome
1. 安装"Get cookies.txt LOC"扩展
2. 访问YouTube
3. 登录你的账号
4. 点击扩展图标，选择"导出Cookies为JSON"
5. 保存为 `cookies.txt`
6. 放到项目目录

### Firefox
1. 访问 `about:preferences#privacy`
2. 点击"管理数据"（Manage Data）
3. 找到"Cookies和网站数据"
4. 选择"导出"
5. 保存为 `cookies.json`

### 命令行使用（配合yt-dlp）
```bash
# 导出cookies后使用
yt-dlp --cookies-from-browser cookies.txt --write-subs "https://www.youtube.com/watch?v=xxxxx"

# 或者指定浏览器
yt-dlp --cookies-from-browser chrome --write-subs "https://www.youtube.com/watch?v=xxxxx"
```

## 注意事项

1. **版权和合规**
   - 尊重内容创作者的版权
   - 仅用于个人学习和研究
   - 不要公开发布转录内容

2. **技术限制**
   - YouTube的反爬机制越来越强
   - 过度请求可能导致IP封禁
   - 考虑使用代理池或延迟请求

3. **数据验证**
   - 转录内容可能包含错误
   - 对于重要内容，建议人工核对
   - AI转录可能有幻觉，需要校验

4. **性能优化**
   - 批量处理时添加随机延迟
   - 使用异步请求减少等待时间
   - 设置合理的超时和重试机制

## 推荐工作流

1. **获取视频链接**
   - 从用户输入或数据库中获取
   - 验证URL格式和有效性

2. **多渠道并行获取**
   - NoteGPT：获取AI转录和总结
   - B站：如果适用，尝试获取官方字幕
   - 小红书：搜索相关笔记
   - 文案库：检查是否有现成文案

3. **信息整合**
   - 按时间线整理内容
   - 识别关键信息点
   - 标注数据来源和可信度

4. **生成最终summary**
   - 整合所有来源的信息
   - 突出共同观点和差异点
   - 生成结构化的markdown输出
   - 保存到指定路径

5. **质量检查**
   - 验证转录完整性
   - 检查重要信息是否遗漏
   - 确保数据格式正确

---

**最后更新时间**：2026-02-12
