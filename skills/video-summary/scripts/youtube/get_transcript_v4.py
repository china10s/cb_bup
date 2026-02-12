from youtube_transcript_api import YouTubeTranscriptApi
import json

# YouTube视频ID
video_id = "iSSHmP0ySBY"

try:
    print("="*60)
    print("开始获取 YouTube 视频字幕")
    print(f"视频ID: {video_id}")
    print("="*60)
    
    # 初始化API
    yt_api = YouTubeTranscriptApi()
    
    # 获取视频的转录
    print("\n正在调用YouTube Transcribe API...")
    fetched_transcript = yt_api.fetch(video_id)
    
    print(f"\n成功获取到转录数据!")
    print(f"转录语言: {fetched_transcript.language}")
    print(f"转录语言代码: {fetched_transcript.language_code}")
    print(f"是否为自动生成: {fetched_transcript.is_generated}")
    print(f"是否可翻译: {fetched_transcript.is_translatable}")
    print(f"转录片段数量: {len(fetched_transcript)}")
    
    # 获取完整的文本内容
    transcript_text = ""
    for segment in fetched_transcript:
        transcript_text += segment.text + " "
    
    # 保存完整字幕到文件
    with open('/root/.openclaw/workspace/transcript_full.txt', 'w', encoding='utf-8') as f:
        f.write(transcript_text)
    
    print(f"\n✓ 完整字幕已保存")
    print(f"✓ 总字符数: {len(transcript_text)}")
    
    # 显示前500个字符
    print(f"\n前500个字符预览:")
    print(transcript_text[:500])
    
    # 保存结构化数据（JSON）
    segments_data = []
    for i, segment in enumerate(fetched_transcript):
        segments_data.append({
            'segment_index': i,
            'start_time': segment.start,
            'duration': segment.duration,
            'text': segment.text
        })
    
    with open('/root/.openclaw/workspace/transcript_structured.json', 'w', encoding='utf-8') as f:
        json.dump(segments_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 结构化数据已保存")
    print(f"✓ 共 {len(segments_data)} 个字幕片段")
    
    # 显示前10个片段
    print(f"\n前10个字幕片段:")
    for i, segment in enumerate(segments_data[:10]):
        print(f"{i+1}. [{segment['start_time']:.2f} - {segment['start_time'] + segment['duration']:.2f}] {segment['text'][:50]}...")
    
except Exception as e:
    print(f"\n发生错误: {str(e)}")
    print(f"错误类型: {type(e).__name__}")
    
    # 打印详细错误信息
    import traceback
    traceback.print_exc()

