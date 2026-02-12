#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def test_xhs_access():
    note_id = "6983de3f000000000b01060b"
    xsec_token = "CB-3pixIsTD-KikqxDNCUh5tpiX37oKupsvqtHGCq4koU="
    
    print(f"[{datetime.now()}] 尝试1: 直接访问discovery/item")
    url1 = f"https://www.xiaohongshu.com/discovery/item/{note_id}?xsec_token={xsec_token}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Referer": "https://www.xiaohongshu.com/"
    }
    
    try:
        resp = requests.get(url1, headers=headers, timeout=10)
        print(f"状态码: {resp.status_code}")
        print(f"响应长度: {len(resp.text)}")
        if "甄嬛" in resp.text or "奶茶" in resp.text:
            print("响应中包含关键词")
    except Exception as e:
        print(f"请求失败: {e}")
    
    print(f"[{datetime.now()}] 尝试2: 访问API端点")
    api_url = "https://edith.xiaohongshu.com/api/sns/web/v1/note/feed"
    api_headers = {
        "User-Agent": headers["User-Agent"],
        "Content-Type": "application/json",
        "Cookie": f"xsec_token={xsec_token}"
    }
    
    try:
        data = {"note_id": note_id, "xsec_token": xsec_token, "xsec_source": "web_search"}
        resp = requests.post(api_url, headers=api_headers, json=data, timeout=10)
        print(f"API状态码: {resp.status_code}")
        print(f"API响应: {resp.text[:500] if len(resp.text) > 500 else resp.text}")
        try:
            result = resp.json()
            print(f"API JSON keys: {list(result.keys())}")
        except:
            pass
    except Exception as e:
        print(f"API请求失败: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("小红书爬虫测试")
    print("=" * 60)
    test_xhs_access()
    print("=" * 60)
    print("测试完成")
    print("=" * 60)
