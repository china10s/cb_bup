#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright
import json
import re

url = "https://www.xiaohongshu.com/explore/6983de3f000000000b01060b?xsec_token=CB-3pixIsTD-KikqxDNCUh5tpiX37oKupsvqtHGCq4koU="

async def run():
    print("[PLAYWRIGHT] 启动浏览器...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print(f"[PLAYWRIGHT] 访问URL: {url}")
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        
        # 等待JavaScript执行
        print("[PLAYWRIGHT] 等待页面加载...")
        await page.wait_for_timeout(5000)
        
        # 获取页面内容
        content = await page.content()
        print(f"[PLAYWRIGHT] 页面长度: {len(content)}")
        
        # 保存完整内容
        with open("/root/.openclaw/workspace/xhs_playwright_full.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("[PLAYWRIGHT] ✓ 已保存完整页面")
        
        # 尝试提取所有JSON数据
        json_matches = re.findall(r'\{[^{}]*"[^"]*":\s*{[^{}]*\}', content)
        print(f"[PLAYWRIGHT] 找到{len(json_matches)}个JSON片段")
        
        # 搜索关键词
        keywords = ["AI", "AGI", "生态", "Manus", "视频", "title"]
        for kw in keywords:
            if kw in content:
                print(f"[PLAYWRIGHT] ✓ 页面包含关键词: {kw}")
        
        # 尝试提取视频相关信息
        video_patterns = [
            r'"videoId":"([^"]+)"',
            r'"duration":(\d+)',
            r'"url":"(https://[^"]+\.mp4[^"]*)"',
            r'"title":"([^"]+)"',
            r'"desc":"([^"]+)"'
        ]
        
        print("\n[PLAYWRIGHT] 尝试提取视频信息...")
        for pattern in video_patterns:
            matches = re.findall(pattern, content)
            if matches:
                print(f"[PLAYWRIGHT] 模式: {pattern[:30]}")
                print(f"[PLAYWRIGHT] 匹配: {matches[:5]}")
        
        await browser.close()
        print("[PLAYWRIGHT] ✓ 完成")

if __name__ == "__main__":
    asyncio.run(run())
