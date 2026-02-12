#!/usr/bin/env python3
import asyncio
import httpx
import json
from pathlib import Path

note_id = "6983de3f000000000b01060b"
xsec_token = "CB-3pixIsTD-KikqxDNCUh5tpiX37oKupsvqtHGCq4koU="
url = f"https://www.xiaohongshu.com/discovery/item/{note_id}?xsec_token={xsec_token}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.xiaohongshu.com/",
    "Cookie": f"xsec_token={xsec_token}"
}

async def test_xhs():
    print(f"[TEST] 开始测试小红书访问...")
    print(f"[TEST] URL: {url}")
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        # 尝试1: GET请求
        print(f"\n[TEST 1] 发送GET请求...")
        try:
            resp = await client.get(url, headers=headers)
            print(f"[TEST 1] 状态码: {resp.status_code}")
            print(f"[TEST 1] 响应长度: {len(resp.text)}")
            
            # 保存完整响应
            with open("/root/.openclaw/workspace/xhs_full_response.html", "w", encoding="utf-8") as f:
                f.write(resp.text)
            print(f"[TEST 1] ✓ 已保存完整响应到 xhs_full_response.html")
            
            # 尝试提取关键信息
            if "甄嬛" in resp.text:
                print(f"[TEST 1] ✓ 响应包含'甄嬛'")
            if "奶茶" in resp.text:
                print(f"[TEST 1] ✓ 响应包含'奶茶'")
            if "视频" in resp.text or "video" in resp.text:
                print(f"[TEST 1] ✓ 响应包含视频相关关键词")
            
            # 尝试提取JSON数据
            if '{"data"' in resp.text or '"note_id"' in resp.text:
                print(f"[TEST 1] ✓ 响应可能包含JSON数据")
                # 查找JSON片段
                start = resp.text.find('{"data"')
                if start > 0:
                    end = resp.text.find('}', start)
                    if end > start:
                        try:
                            json_str = resp.text[start:end+1]
                            data = json.loads(json_str)
                            print(f"[TEST 1] ✓ 成功提取JSON数据")
                            print(f"[TEST 1] JSON keys: {list(data.keys())}")
                            # 深度检查数据结构
                            if "data" in data:
                                print(f"[TEST 1] data type: {type(data['data'])}")
                                print(f"[TEST 1] data keys: {list(data['data'].keys()) if isinstance(data['data'], dict) else 'not dict'}")
                        except Exception as e:
                            print(f"[TEST 1] JSON解析失败: {e}")
            
            # 尝试API端点
            api_url = "https://edith.xiaohongshu.com/api/sns/web/v1/note/feed"
            api_data = {
                "note_id": note_id,
                "xsec_token": xsec_token,
                "xsec_source": "web_search"
            }
            print(f"\n[TEST 2] 尝试API端点: {api_url}")
            try:
                api_resp = await client.post(api_url, json=api_data, headers=headers)
                print(f"[TEST 2] API状态码: {api_resp.status_code}")
                print(f"[TEST 2] API响应: {api_resp.text[:200]}")
                try:
                    api_result = api_resp.json()
                    print(f"[TEST 2] ✓ API返回JSON: {list(api_result.keys())}")
                    # 保存API响应
                    with open("/root/.openclaw/workspace/xhs_api_response.json", "w") as f:
                        json.dump(api_result, f, ensure_ascii=False, indent=2)
                    print(f"[TEST 2] ✓ 已保存API响应到 xhs_api_response.json")
                except:
                    print(f"[TEST 2] API响应不是有效JSON")
            except Exception as e:
                print(f"[TEST 2] API请求失败: {e}")
            
        except Exception as e:
            print(f"[TEST 1] 请求失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_xhs())
