#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音视频自动下载和转录工具
功能：解析链接、下载视频、提取音频、Whisper 语音识别、保存原始转录
生成的转录文件可以交给 AI 助手进行智能总结
"""
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime

# 添加 douyin-video 技能到路径
skill_dir = Path(__file__).parent.parent / "douyin-video" / "scripts"
sys.path.insert(0, str(skill_dir))

from douyin_downloader import get_video_info, download_video

# 配置临时文件目录（固定路径，避免相对路径问题）
TEMP_PATH = Path("D:/一人公司/自媒体/douyin_temp")
TEMP_PATH.mkdir(parents=True, exist_ok=True)


def setup_ffmpeg():
    """设置 FFmpeg 路径"""
    import os
    # 先尝试添加临时目录到 PATH（那里有复制好的 ffmpeg）
    os.environ['PATH'] = str(TEMP_PATH) + os.pathsep + os.environ['PATH']
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        ffmpeg_dir = Path(ffmpeg_path).parent
        os.environ['PATH'] = str(ffmpeg_dir) + os.pathsep + os.environ['PATH']
        return True
    except:
        return False


def extract_audio(video_path, audio_path=None):
    """从视频中提取音频"""
    from moviepy import VideoFileClip

    if audio_path is None:
        audio_path = Path(video_path).with_suffix('.mp3')

    print("正在提取音频...")
    video = VideoFileClip(str(video_path))
    audio = video.audio
    audio.write_audiofile(str(audio_path))
    video.close()
    print(f"音频提取完成: {audio_path}")
    return Path(audio_path)


def transcribe_with_whisper(audio_path):
    """使用 Whisper 进行语音识别"""
    setup_ffmpeg()
    import whisper

    print("正在加载 Whisper 模型...")
    model = whisper.load_model('base')

    print("正在识别语音...")
    result = model.transcribe(str(audio_path), language='zh')

    text_len = len(result['text'])
    print(f"语音识别完成，共 {text_len} 字")
    return result['text']


def process_douyin_video(link, keep_temp=False):
    """完整处理流程：下载、转录"""
    print("=" * 60)
    print("抖音视频下载和转录工具")
    print("=" * 60)

    # 步骤1: 解析链接
    print("\n【步骤1】解析抖音链接...")
    video_info = get_video_info(link)
    video_id = video_info['video_id']
    title = video_info['title']
    print(f"视频ID: {video_id}")
    print(f"标题: {title}")

    # 步骤2: 下载视频
    print("\n【步骤2】下载视频...")
    video_path = download_video(link, str(TEMP_PATH))
    print(f"视频已保存: {video_path}")

    # 步骤3: 提取音频
    print("\n【步骤3】提取音频...")
    audio_path = extract_audio(video_path)

    # 步骤4: 语音识别
    print("\n【步骤4】语音识别...")
    transcript = transcribe_with_whisper(audio_path)

    # 步骤5: 保存原始转录
    print("\n【步骤5】保存转录文件...")
    transcript_path = TEMP_PATH / f"{video_id}_transcript.txt"
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(transcript)
    print(f"原始转录已保存: {transcript_path}")

    # 清理临时文件（如果需要）
    if not keep_temp:
        print("\n【清理】删除视频和音频文件...")
        try:
            vp = Path(video_path)
            if vp.exists():
                vp.unlink()
            ap = Path(audio_path)
            if ap.exists():
                ap.unlink()
            print("临时文件已清理")
        except Exception as e:
            print(f"警告: 清理临时文件时出错: {e}")

    print("\n" + "=" * 60)
    print("✓ 处理完成！")
    print("=" * 60)
    print("\n请将以下信息交给 AI 助手进行智能总结：")
    print(f"- 视频ID: {video_id}")
    print(f"- 视频标题: {title}")
    print(f"- 转录文件: {transcript_path}")

    return {
        'video_id': video_id,
        'title': title,
        'transcript_path': transcript_path,
        'transcript': transcript
    }


def main():
    parser = argparse.ArgumentParser(
        description="抖音视频下载和转录工具"
    )

    parser.add_argument("--link", "-l", required=True, help="抖音分享链接")
    parser.add_argument("--keep-temp", "-k", action="store_true",
                        help="保留临时文件（视频、音频）")

    args = parser.parse_args()

    try:
        process_douyin_video(
            link=args.link,
            keep_temp=args.keep_temp
        )
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
