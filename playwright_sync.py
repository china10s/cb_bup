import asyncio
import json
from playwright.sync_api import sync_playwright

# YouTube视频URL
youtube_url = "https://www.youtube.com/watch?v=iSSHmP0ySBY"
note_url = "https://notegpt.io/youtube-video-summarizer"

print("="*60)
print("启动 Playwright 浏览器 (Sync API)")
print(f"目标URL: {youtube_url}")
print(f"NoteGPT工具URL: {note_url}")
print("="*60)

try:
    # 启动浏览器
    browser = sync_playwright().chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    print("\n[步骤1] 导航到NoteGPT页面...")
    page.goto(youtube_url, wait_until="domcontentloaded", timeout=30000)
    print("  ✓ YouTube页面加载完成")
    
    print("\n[步骤2] 导航到NoteGPT工具页面...")
    page.goto(note_url, wait_until="domcontentloaded", timeout=30000)
    print("  ✓ NoteGPT页面加载完成")
    
    # 查找输入框
    print(f"\n[步骤3] 查找输入框...")
    input_selectors = [
        'input[placeholder*="YouTube Video URL"]',
        'input[placeholder*="url"]',
        'input[placeholder*="Link"]',
        'textarea[name*="prompt"]',
        'input[type*="text"]',
        'textarea[name*="message"]',
    ]
    
    input_found = False
    for selector in input_selectors:
        try:
            element = page.query_selector(selector, timeout=5000)
            if element:
                print(f"  ✓ 找到输入框: {selector}")
                element.fill(youtube_url)
                print(f"  ✓ 成功填充YouTube链接")
                input_found = True
                break
        except Exception as e:
            print(f"  输入框 {selector} 查找失败: {str(e)}")
    
    if not input_found:
        print("\n警告: 所有输入框选择器都未找到")
    
    # 查找"Generate"按钮
    print(f"\n[步骤4] 查找Generate按钮...")
    button_selectors = [
        'button:has-text("Generate")',
        'button:has-text("Summary")',
        'button:has-text("submit")',
        'button[type="submit"]',
        'button[onclick*="generate"]',
        'button[onclick*="submit"]',
    ]
    
    button_clicked = False
    for selector in button_selectors:
        try:
            element = page.query_selector(selector, timeout=5000)
            if element:
                print(f"  ✓ 找到按钮: {selector}")
                element.click()
                print(f"  ✓ 成功点击Generate按钮")
                button_clicked = True
                break
        except Exception as e:
            print(f"  按钮 {selector} 查找或点击失败: {str(e)}")
    
    if not button_clicked:
        print("\n警告: 所有按钮选择器都未找到")
    
    # 等待结果生成
    print(f"\n[步骤5] 等待NoteGPT生成摘要...")
    page.wait_for_timeout(10000)
    
    # 尝试多次检查结果（不同时间段）
    for i in range(5):
        print(f"\n[检查 {i+1}] 检查页面状态...")
        
        # 获取页面内容
        content = page.content()
        
        # 查找摘要内容的关键词
        summary_indicators = [
            '摘要',
            'summary',
            'Summary',
            'Analysis',
            'analysis',
            'result',
            'Result',
            'Generated',
            'generated',
        ]
        
        found_summary = False
        for indicator in summary_indicators:
            if indicator in content:
                print(f"  ✓ 检测到关键: '{indicator}'")
                found_summary = True
                break
        
        if found_summary:
            print(f"  ✓ 检查 {i+1} 成功：页面已包含摘要内容")
            break
        
        # 每次检查之间等待
        page.wait_for_timeout(3000)
    
    # 最终保存页面内容
    print(f"\n[步骤6] 保存页面内容...")
    with open('/root/.openclaw/workspace/notegpt_final.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ 页面内容已保存 (长度: {len(content)})")
    
    # 截图
    print(f"\n[步骤7] 截取页面截图...")
    screenshot = page.screenshot(path='/root/.openclaw/workspace/notegpt_screenshot.png')
    print(f"  ✓ 截图已保存")
    
    print("\n" + "="*60)
    print("Playwright 任务完成")
    print("="*60)
    
except Exception as e:
    print(f"\n[错误] 发生异常: {str(e)}")
    print(f"错误类型: {type(e).__name__}")
    
    # 打印详细错误信息
    import traceback
    traceback.print_exc()

