#!/usr/bin/env python3
import requests

note_id = "6983de3f000000000b01060b"
xsec_token = "CB-3pixIsTD-KikqxDNCUh5tpiX37oKupsvqtHGCq4koU="

print(f"[TEST] 尝试访问小红书笔记...")
print(f"Note ID: {note_id}")
print(f"Token: {xsec_token}")

# Test 1: Direct discovery/item access
url1 = f"https://www.xiaohongshu.com/discovery/item/{note_id}?xsec_token={xsec_token}"
print(f"\n[TEST 1] URL: {url1}")

try:
    resp = requests.get(url1, timeout=15)
    print(f"[TEST 1] 状态码: {resp.status_code}")
    print(f"[TEST 1] 响应长度: {len(resp.text)}")
    
    # Print first 500 chars of response
    print(f"[TEST 1] 响应前500字符:")
    print(resp.text[:500])
    
    # Check for login page indicators
    if "扫码" in resp.text or "登录" in resp.text:
        print("[TEST 1] ❌ 重定向到登录页")
    elif "404" in resp.text or "不见了" in resp.text:
        print("[TEST 1] ❌ 页面不存在")
    elif "甄嬛" in resp.text or "奶茶" in resp.text:
        print("[TEST 1] ✅ 响应包含目标关键词")
    else:
        print("[TEST 1] ❓ 响应内容未知")
        
except Exception as e:
    print(f"[TEST 1] ❌ 请求失败: {e}")

# Test 2: API endpoint
api_url = "https://edith.xiaohongshu.com/api/sns/web/v1/note/feed"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Cookie": f"xsec_token={xsec_token}"
}

print(f"\n[TEST 2] API URL: {api_url}")
try:
    data = {"note_id": note_id, "xsec_token": xsec_token, "xsec_source": "web_search"}
    resp = requests.post(api_url, headers=headers, json=data, timeout=15)
    print(f"[TEST 2] API状态码: {resp.status_code}")
    print(f"[TEST 2] API响应前500字符:")
    print(resp.text[:500])
    
    try:
        result = resp.json()
        print(f"[TEST 2] API JSON: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}")
    except:
        print(f"[TEST 2] 响应不是有效JSON")
        
except Exception as e:
    print(f"[TEST 2] ❌ API请求失败: {e}")

print("\n[COMPLETE] 测试完成")
