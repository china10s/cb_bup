import asyncio
import json
from playwright.async_api import async_playwright
from playwright.async_api import async_playwright

# YouTube视频URL
youtube_url = "https://www.youtube.com/watch?v=iSSHmP0ySBY"
target_url = "https://notegpt.io/youtube-video-summarizer"

async def main():
    print("="*60)
    print("启动 Playwright 浏览器")
    print(f"目标URL: {youtube_url}")
    print(f"目标平台: NoteGPT")
    print("="*60)
    
    # 启动浏览器
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("\n[步骤1] 导航到NoteGPT页面...")
            await page.goto(youtube_url, wait_until="domcontentloaded", timeout=30000)
            
            print(f"[步骤2] 导航到NoteGPT工具页面...")
            await page.goto(target_url, wait_until="domcontentloaded", timeout=30000)
            
            # 等待页面加载
            await page.wait_for_timeout(5000)
            
            # 查找输入框（可能有不同的选择器）
            print(f"\n[步骤3] 查找YouTube链接输入框...")
            
            # 尝试多个可能的输入框选择器
            input_selectors = [
                "input[type='text']",
                "textarea[name='prompt']",
                "textarea[placeholder*='Video' i*='URL']",
                "#url",
                "input[placeholder*='url']",
                "input[name*='url']",
            ]
            
            # 查找"Generate"按钮
            button_selectors = [
                "button:has-text('Generate')",
                "button[type='submit']",
                "button[onclick*='generate']",
                "button[aria-label*='Generate']",
            ]
            
            for selector in input_selectors:
                try:
                    element = await page.query_selector(selector, timeout=10000)
                    if element:
                        print(f"  找到输入框: {selector}")
                        await element.fill(youtube_url)
                        print(f"  ✓ 成功填充YouTube链接")
                        input_found = True
                        break
                except Exception as e:
                    print(f"  输入框 {selector} 未找到或操作失败: {str(e)}")
            
            if not input_found:
                print("\n警告: 所有输入框选择器都失败了")
            
            for selector in button_selectors:
                try:
                    element = await page.query_selector(selector, timeout=10000)
                    if element:
                        print(f"  找到提交按钮: {selector}")
                        print(f"  ✓ 尝试点击Generate按钮...")
                        await element.click()
                        print(f"  ✓ 成功点击Generate按钮")
                        button_clicked = True
                        break
                except Exception as e:
                    print(f"  提交按钮 {selector} 未找到或点击失败: {str(e)}")
            
            if not button_clicked:
                print("\n警告: 所有提交按钮选择器都失败了")
            
            # 等待结果生成
            print(f"\n[步骤4] 等待NoteGPT生成摘要...")
            print("  等待30秒...")
            await page.wait_for_timeout(30000)
            
            # 尝试捕获结果内容
            print(f"\n[步骤5] 捕获生成的摘要...")
            
            # 等待可能的文本内容加载
            await page.wait_for_timeout(10000)
            
            # 获取页面完整文本内容
            page_content = await page.content()
            
            # 保存原始HTML
            with open('/root/.openclaw/workspace/notegpt_page.html', 'w', encoding='utf-8') as f:
                f.write(page_content)
            
            print(f"  ✓ 页面内容已保存 (长度: {len(page_content)})")
            
            # 尝试从页面中提取摘要内容
            print(f"\n[步骤6] 分析页面内容，提取摘要...")
            
            # 查找可能的摘要容器
            summary_patterns = [
                'summary',
                'result',
                'analysis',
                'content',
                'output'
            ]
            
            # 使用正则表达式提取摘要内容
            import re
            
            # 模式1: 查找包含关键字的div
            for pattern in [
                r'<div[^>]*summary[^>]*>([^<]+)</div>',
                r'"content":"([^"]+)"',
                r'"text":"([^"]+)"',
                r'<p[^>]*>([^<]+)</p>',
                r'<div[^>]*class="[^"]*summary[^"]*"[^>]*>([^<]+)</div>',
            ]:
                matches = re.findall(pattern, page_content)
                if matches:
                    print(f"  找到摘要内容 (模式: {pattern[:50]}...):")
                    for match in matches[:3]:  # 只显示前3个匹配
                        # 清理HTML实体
                        clean_text = re.sub(r'<[^>]+>', ' ', match)
                        clean_text = re.sub(r'&nbsp;', ' ', clean_text)
                        clean_text = re.sub(r'\s+', ' ', clean_text)
                        print(f"  匹配内容: {clean_text[:200]}...")
                    
            print("\n" + "="*60)
            print("Playwright 任务完成")
            print("="*60)
            
        except Exception as e:
            print(f"\n[错误] 发生异常: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
