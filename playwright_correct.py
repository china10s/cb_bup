from playwright.sync_api import sync_playwright
import json

# 目标URL
youtube_url = "https://www.youtube.com/watch?v=iSSHmP0ySBY"
note_gpt_url = "https://notegpt.io/youtube-video-summarizer"

print("="*60)
print("使用 Playwright 同步 API")
print(f"目标URL: {youtube_url}")
print(f"NoteGPT URL: {note_gpt_url}")
print("="*60)

try:
    # 启动浏览器
    browser = sync_playwright().chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    # 步骤1：打开YouTube页面
    print("\n[步骤1] 导航到YouTube页面...")
    page.goto(youtube_url, wait_until="domcontentloaded", timeout=30000)
    print("  ✓ YouTube页面加载完成")
    
    # 步骤2：提取YouTube标题
    title = page.locator("h1").first.text_content()
    print(f"\n[步骤2] 提取YouTube标题: {title[:50]}")
    
    # 步骤3：打开NoteGPT页面
    print(f"\n[步骤3] 导航到NoteGPT页面...")
    page.goto(note_gpt_url, wait_until="domcontentloaded", timeout=30000)
    print("  ✓ NoteGPT页面加载完成")
    
    # 步骤4：查找并填充输入框
    print(f"\n[步骤4] 查找输入框并填充YouTube链接...")
    
    # 尝试多个可能的输入框选择器
    input_selectors = [
        'input[placeholder*="YouTube Video URL"]',
        'input[placeholder*="Link"]',
        'input[placeholder*="video"]',
        'input[placeholder*="url"]',
        'input[type*="text"]',
        'input[name*="prompt"]',
        'textarea[name*="prompt"]',
        'input[name*="message"]',
        'textarea[name*="url"]',
        'textarea[placeholder*="Paste"]',
        'input[placeholder*="Enter"]',
    ]
    
    input_found = False
    for selector in input_selectors:
        try:
            element = page.locator(selector).first
            if element.count() > 0:
                print(f"  ✓ 找到输入框: {selector}")
                element.fill(youtube_url)
                print(f"  ✓ 成功填充YouTube链接")
                input_found = True
                break
        except:
            continue
    
    if not input_found:
        print("\n警告: 所有输入框选择器都未找到")
        # 尝试通用方式：查找任何text input或textarea
        all_inputs = page.locator('input[type="text"], textarea').all()
        for input_elem in all_inputs:
            if input_elem.count() > 0:
                print(f"  找到文本输入: {input_elem}")
                input_elem.fill(youtube_url)
                print(f"  ✓ 填充成功")
                input_found = True
                break
    
    # 步骤5：查找并点击Generate按钮
    print(f"\n[步骤5] 查找Generate按钮并点击...")
    
    # 尝试多个可能的按钮选择器
    button_selectors = [
        'button:has-text("Generate")',
        'button:has-text("Summary")',
        'button:has-text("Submit")',
        'button[type="submit"]',
        'button[onclick*="generate"]',
        'button[onclick*="submit"]',
    ]
    
    button_clicked = False
    for selector in button_selectors:
        try:
            button = page.locator(selector).first
            if button.count() > 0:
                print(f"  ✓ 找到按钮: {selector}")
                button.click()
                print(f"  ✓ 成功点击Generate按钮")
                button_clicked = True
                break
        except:
            continue
    
    if not button_clicked:
        print("\n警告: 所有按钮选择器都未找到，尝试通用方式")
        # 尝试查找任何包含Generate或Summary的按钮
        all_buttons = page.locator('button').all()
        for btn in all_buttons:
            if btn.count() > 0:
                text = btn.text_content()
                if 'Generate' in text or 'Summary' in text:
                    print(f"  找到包含关键字的按钮: {text[:30]}")
                    btn.click()
                    print(f"  ✓ 点击成功")
                    button_clicked = True
                    break
    
    # 步骤6：等待结果生成
    print(f"\n[步骤6] 等待NoteGPT生成摘要...")
    page.wait_for_timeout(10000)
    
    # 步骤7：检查页面内容变化
    print(f"\n[步骤7] 检查页面内容变化...")
    
    # 尝试多次检查结果
    for i in range(5):
        print(f"  [检查 {i+1}] 检测摘要内容...")
        
        # 查找可能的摘要容器
        summary_keywords = ['summary', 'Summary', 'result', 'Result', 'output', 'content', 'analysis', 'generated', 'AI']
        
        found_content = False
        for keyword in summary_keywords:
            content = page.content()
            if keyword in content:
                print(f"  ✓ 检测到关键: '{keyword}'")
                found_content = True
                break
        
        if found_content:
            print(f"  ✓ 检查 {i+1} 成功：页面包含摘要内容")
            break
        
        page.wait_for_timeout(3000)
    
    # 步骤8：获取最终页面内容
    print(f"\n[步骤8] 获取最终页面内容...")
    final_content = page.content()
    
    # 保存页面内容
    with open('/root/.openclaw/workspace/notegpt_final_page.html', 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"  ✓ 页面内容已保存 (长度: {len(final_content)})")
    
    # 步骤9：尝试提取摘要文本
    print(f"\n[步骤9] 尝试提取摘要文本...")
    
    # 查找可能的摘要文本容器
    import re
    
    # 模式1：查找包含summary关键字的div/p
    summary_pattern = r'<div[^>]*summary[^>]*>([^<]+)</div>'
    matches = re.findall(summary_pattern, final_content)
    
    if matches:
        print(f"  ✓ 找到{len(matches)}个摘要div片段")
        for i, match in enumerate(matches[:3]):
            # 清理HTML标签
            clean_text = re.sub(r'<[^>]+>', ' ', match)
            clean_text = re.sub(r'&nbsp;', ' ', clean_text)
            print(f"\n  摘要{i+1}: {clean_text[:150]}...")
    
    # 模式2：查找JSON格式的摘要
    json_pattern = r'"summary":"([^"]+)"'
    json_matches = re.findall(json_pattern, final_content)
    
    if json_matches:
        print(f"  ✓ 找到{len(json_matches)}个JSON格式的摘要片段")
        for match in json_matches[:3]:
            print(f"  摘要{i+1}: {match}...")
    
    # 模式3：查找Result或content字段
    content_patterns = [
        r'"content":"([^"]+)"',
        r'"text":"([^"]+)"',
        r'"result":"([^"]+)"',
        r'"analysis":"([^"]+)"'
    ]
    
    for pattern in content_patterns:
        matches = re.findall(pattern, final_content)
        if matches:
            print(f"  ✓ 找到{len(matches)}个内容片段 (模式: {pattern[:30]}...)")
            for match in matches[:2]:
                print(f"  摘要: {match[:100]}...")
    
    # 步骤10：截图
    print(f"\n[步骤10] 截取页面截图...")
    page.screenshot(path='/root/.openclaw/workspace/notegpt_final_screenshot.png')
    print("  ✓ 截图已保存")
    
    print("\n" + "="*60)
    print("Playwright 任务完成")
    print("="*60)
    
except Exception as e:
    print(f"\n[错误] 发生异常: {str(e)}")
    print(f"错误类型: {type(e).__name__}")
    
    # 打印详细错误信息
    import traceback
    traceback.print_exc()

