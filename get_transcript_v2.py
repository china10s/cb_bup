import youtube_transcript_api

# YouTube视频ID
video_id = "iSSHmP0ySBY"

try:
    # 获取可用的转录信息
    transcript_list = youtube_transcript_api.list_transcripts(video_id)
    
    print(f"找到 {len(transcript_list)} 个转录语言版本")
    print(f"可用的语言: {[t['language'] for t in transcript_list]}")
    
    # 尝试获取中文或英文转录
    target_transcript = None
    
    # 优先尝试中文
    for transcript in transcript_list:
        if 'zh' in transcript['language']:
            target_transcript = transcript
            print(f"\n使用中文转录: {transcript['language']}")
            break
    
    # 如果没有中文，使用英文
    if target_transcript is None and transcript_list:
        target_transcript = transcript_list[0]
        print(f"\n使用转录: {target_transcript['language']} (默认)")
    
    if target_transcript:
        # 获取转录数据
        transcript_data = target_transcript.fetch()
        
        print(f"\n转录信息:")
        print(f"- 语言: {target_transcript['language']}")
        print(f"- 类型: {target_transcript['type']}")
        print(f"- 生成方式: {target_transcript['generated']}")
        
        print(f"\n字幕统计:")
        print(f"- 总长度: {len(transcript_data)} 字符")
        print(f"- 字幕片段数: {len(transcript_data)}")
        
        # 保存完整字幕到文件
        with open('/root/.openclaw/workspace/transcript_full.txt', 'w', encoding='utf-8') as f:
            f.write(transcript_data)
        print(f"\n✓ 完整字幕已保存到 transcript_full.txt")
        
        # 显示前1000个字符
        print(f"\n前1000个字符预览:")
        print(transcript_data[:1000])
        
        # 保存字幕片段列表（每个片段包含文本和时间信息）
        with open('/root/.openclaw/workspace/transcript_segments.json', 'w', encoding='utf-8') as f:
            segments_info = []
            for i, segment in enumerate(transcript_data):
                segments_info.append({
                    'index': i,
                    'text': segment.text,
                    'start': segment.start,
                    'duration': segment.duration,
                    'end': segment.start + segment.duration
                })
            
            import json
            json.dump(segments_info, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 字幕片段已保存到 transcript_segments.json")
        
    else:
        print("未找到可用的转录")
    
except Exception as e:
    print(f"发生错误: {str(e)}")
    print(f"错误类型: {type(e).__name__}")
    
    # 打印详细错误信息
    import traceback
    traceback.print_exc()

