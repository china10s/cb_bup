import subprocess
import json

# 尝试安装并使用 youtube-subtitle-downloader
print("开始安装 youtube-subtitle-downloader...")

# 方法1：尝试安装
try:
    print("方法1：尝试安装 youtube-subtitle-downloader...")
    install_result = subprocess.run(
        ["pip3", "install", "youtube-subtitle-downloader"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if install_result.returncode == 0:
        print("  ✓ 安装成功")
        
        # 方法2：尝试获取帮助
        print("\n方法2：获取使用帮助...")
        help_result = subprocess.run(
            ["pip3", "show", "youtube-subtitle-downloader"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        help_output = help_result.stdout
        
        print(f"  ✓ 帮助信息已获取:\n{help_output}")
        
        # 尝试从帮助信息中提取用法
        if "Usage" in help_output:
            print("\n发现Usage说明:")
            print("  - 如果找到正确的下载命令，可以尝试使用")
        
        # 保存帮助信息
        with open('/root/.openclaw/workspace/youtube_subtitle_help.txt', 'w', encoding='utf-8') as f:
            f.write(help_output)
        
        print("\n方法3：尝试下载字幕...")
        
        # 尝试直接下载命令
        # 假设youtube-subtitle-downloader支持CLI命令：youtube-subtitle-downloader "视频ID" --write
        # 但实际上应该是不同的命令格式
        
        # 方法4：使用Python API
        # 创建一个简单的Python脚本来调用包的API
        print("\n方法4：尝试使用Python API...")
        
except Exception as e:
    print(f"\n[错误] 发生异常: {str(e)}")
    import traceback
    traceback.print_exc()

