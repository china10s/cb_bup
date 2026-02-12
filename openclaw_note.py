import subprocess
import json

# 目标URL
youtube_url = "https://www.youtube.com/watch?v=iSSHmP0ySBY"
note_gpt_url = "https://notegpt.io/youtube-video-summarizer"

print("="*60)
print("尝试使用 OpenClaw 浏览器工具")
print(f"目标URL: {youtube_url}")
print(f"NoteGPT URL: {note_gpt_url}")
print("="*60)

try:
    # 步骤1：启动OpenClaw浏览器
    print("\n[步骤1] 启动OpenClaw浏览器...")
    result = subprocess.run(
        ["openclaw", "browser", "start"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        print(f"  ✗ 启动失败: {result.stderr}")
    else:
        print("  ✓ 浏览器已启动")
        # 保存会话ID以便后续操作
        session_id = json.loads(result.stdout).get("sessionId", "")
        print(f"  ✓ 会话ID: {session_id}")
    
    # 步骤2：打开YouTube页面（获取页面状态）
    print(f"\n[步骤2] 导航到YouTube页面...")
    result = subprocess.run(
        ["openclaw", "browser", "open", youtube_url],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        print(f"  ✗ 导航失败: {result.stderr}")
    else:
        print("  ✓ YouTube页面已打开")
    
    # 步骤3：打开NoteGPT页面
    print(f"\n[步骤3] 导航到NoteGPT页面...")
    result = subprocess.run(
        ["openclaw", "browser", "open", note_gpt_url],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        print(f"  ✗ NoteGPT导航失败: {result.stderr}")
    else:
        print("  ✓ NoteGPT页面已打开")
    
    # 步骤4：使用Agent Tools尝试点击输入框
    print(f"\n[步骤4] 尝试查找并填充输入框...")
    
    # 尝试查找输入框（基于常见的input selector）
    result = subprocess.run(
        ["openclaw", "browser", "act", 
         "--json", 
         '{"tool":"click","selector":"input[type=\'text\']"}'],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        print(f"  ✗ 点击操作失败: {result.stderr}")
    else:
        print(f"  ✓ 点击指令已发送")
    
    # 步骤5：填充YouTube链接
    result = subprocess.run(
        ["openclaw", "browser", "act",
         "--json",
         '{"tool":"type","text":"' + youtube_url + '"}'],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        print(f"  ✗ 填充失败: {result.stderr}")
    else:
        print(f"  ✓ YouTube链接已填充")
    
    # 步骤6：查找并点击Generate按钮
    print(f"\n[步骤5] 查找并点击Generate按钮...")
    result = subprocess.run(
        ["openclaw", "browser", "act",
         "--json",
         '{"tool":"click","selector":"button:has-text(\'Generate\')"}'],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        print(f"  ✗ 点击Generate失败: {result.stderr}")
    else:
        print(f"  ✓ Generate按钮已点击")
    
    # 步骤7：等待结果生成
    print(f"\n[步骤6] 等待NoteGPT生成摘要...")
    print("  等待10秒...")
    
    import time
    time.sleep(10)
    
    # 步骤8：获取页面截图
    print(f"\n[步骤7] 获取页面截图...")
    result = subprocess.run(
        ["openclaw", "browser", "screenshot", 
         "/root/.openclaw/workspace/notegpt_screenshot.png"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        print(f"  ✗ 截图失败: {result.stderr}")
    else:
        print(f"  ✓ 截图已保存")
    
    # 步骤9：保存页面内容
    print(f"\n[步骤8] 保存当前页面内容...")
    result = subprocess.run(
        ["openclaw", "browser", "snapshot", 
         "--format", "html"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    # 保存输出到文件
    with open("/root/.openclaw/workspace/openclaw_result.json", "w") as f:
        f.write(result.stdout)
    
    print(f"\n  ✓ 操作完成，结果已保存")
    
except Exception as e:
    print(f"\n[错误] 发生异常: {str(e)}")
    import traceback
    traceback.print_exc()

