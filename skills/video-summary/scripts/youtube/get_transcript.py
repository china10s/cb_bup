import youtube_transcript_api

# YouTube视频ID
video_id = "iSSHmP0ySBY"

try:
    # 获取视频的转录内容
    transcript_list = youtube_transcript_api.get_transcript(video_id, languages=['zh-CN', 'en'])
    
    # 如果找不到中文，尝试英文
    if not transcript_list:
        transcript_list = youtube_transcript_api.get_transcript(video_id, languages=['en'])
    
    # 遍历所有可用的转录
    for transcript in transcript_list:
        print(f"找到字幕语言: {transcript['language']}")
        print(f"字幕类型: {transcript['type']}")
        print(f"字幕生成方式: {transcript['generated']}")
        
        # 获取转录内容
        transcript_data = transcript.fetch()
        
        print(f"\n字幕前500字符:")
        print(transcript_data[:500])
        
        print(f"\n完整字幕长度: {len(transcript_data)} 字符")
        print(f"字幕片段数量: {len(transcript)}")
        
        # 只处理第一个字幕
        break
    
except Exception as e:
    print(f"错误: {str(e)}")
    print(f"错误类型: {type(e).__name__}")

