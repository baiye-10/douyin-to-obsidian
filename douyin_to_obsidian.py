#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音视频自动下载和转录工具
功能：解析链接、下载视频、提取音频、Whisper 语音识别、自动修正错字、直接保存到 Obsidian
"""
import sys
import subprocess
import argparse
import re
import json
import os
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent

def load_config():
    config_path = SCRIPT_DIR / "config.py"
    if config_path.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("config", str(config_path))
        cfg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cfg)
        return cfg
    config_example = SCRIPT_DIR / "config.example.py"
    if config_example.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("config_example", str(config_example))
        cfg = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cfg)
        print("⚠️  未找到 config.py，使用默认配置。请复制 config.example.py 为 config.py 并修改路径。")
        return cfg
    print("⚠️  未找到配置文件，使用内置默认值。")
    return None

cfg = load_config()

OBSIDIAN_PATH = getattr(cfg, 'OBSIDIAN_PATH', None) or Path.home() / "ObsidianVault"
TEMP_PATH = getattr(cfg, 'TEMP_PATH', None) or SCRIPT_DIR / "douyin_temp"
WHISPER_MODEL = getattr(cfg, 'WHISPER_MODEL', None) or "base"
PYTHON_PATH = getattr(cfg, 'PYTHON_PATH', None) or sys.executable

TEXT_CORRECTIONS = {}
corr_file = SCRIPT_DIR / "text_corrections.json"
if corr_file.exists():
    try:
        with open(corr_file, 'r', encoding='utf-8') as f:
            corr_data = json.load(f)
            for category, corrections in corr_data.items():
                if isinstance(corrections, dict):
                    TEXT_CORRECTIONS.update(corrections)
    except Exception as e:
        print(f"警告: 无法加载修正配置: {e}")

if not TEXT_CORRECTIONS:
    TEXT_CORRECTIONS = {
        "避允": "毕昇",
        "音乐局儿": "Claude",
        "音乐局": "Claude",
        "米游": "米哈游",
        "米友": "米哈游",
        "崩铁": "星穹铁道",
        "崩三": "崩坏3",
    }

for path in [OBSIDIAN_PATH, TEMP_PATH]:
    Path(path).mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(SCRIPT_DIR))

try:
    from douyin_downloader import get_video_info, download_video
except ImportError:
    print("=" * 60)
    print("❌ 错误: 找不到 douyin_downloader.py")
    print("")
    print("本 skill 依赖 douyin_downloader.py，请确保该文件与")
    print("douyin_to_obsidian.py 在同一目录下。")
    print("")
    print(f"当前查找路径: {SCRIPT_DIR}")
    print(f"该路径下文件: {list(SCRIPT_DIR.glob('*.py'))}")
    print("=" * 60)
    sys.exit(1)


def correct_text(text):
    for wrong, correct in TEXT_CORRECTIONS.items():
        text = text.replace(wrong, correct)
    return text


def setup_ffmpeg():
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
    setup_ffmpeg()

    try:
        import whisper
        print("正在加载 Whisper 模型...")
        model = whisper.load_model(WHISPER_MODEL)
        print("正在识别语音...")
        result = model.transcribe(str(audio_path), language='zh')
        text_len = len(result['text'])
        print(f"语音识别完成，共 {text_len} 字")
        return correct_text(result['text'])
    except ImportError:
        print(f"当前 Python 环境缺少 Whisper，尝试使用指定路径: {PYTHON_PATH}")
        temp_script = Path(TEMP_PATH) / "_whisper_temp.py"
        with open(temp_script, 'w', encoding='utf-8') as f:
            f.write(f'''
import whisper
audio_path = r"{audio_path}"
model_name = "{WHISPER_MODEL}"
print(f"正在加载 {{model_name}} 模型...")
model = whisper.load_model(model_name)
print("正在识别语音...")
result = model.transcribe(audio_path, language='zh')
import json
with open(r"{Path(TEMP_PATH) / 'whisper_result.json'}", 'w', encoding='utf-8') as f:
    json.dump({{"text": result['text']}}, f)
''')
        try:
            subprocess.run([PYTHON_PATH, str(temp_script)], check=True)
            with open(Path(TEMP_PATH) / 'whisper_result.json', 'r', encoding='utf-8') as f:
                result = json.load(f)
            text = result['text']
            text_len = len(text)
            print(f"语音识别完成，共 {text_len} 字")
            return correct_text(text)
        finally:
            if temp_script.exists():
                temp_script.unlink()


def save_to_obsidian(video_id, title, transcript, video_url):
    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)[:50]

    transcript_path = OBSIDIAN_PATH / f"{date_str}-{video_id}.md"

    frontmatter = f"""---
title: {safe_title}
tags: [抖音, 视频笔记, {date_str[:4]}]
source: {video_url}
date: {date_str}
---

# {safe_title}

## 原始内容

{transcript}

## 笔记

- 
"""

    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter)

    print(f"笔记已保存到 Obsidian: {transcript_path}")
    return transcript_path


def process_douyin_video(link, keep_temp=False, no_audio=False):
    print("=" * 60)
    print("抖音视频下载和转录工具")
    print("=" * 60)

    print("\n【步骤1】解析抖音链接...")
    video_info = get_video_info(link)
    video_id = video_info['video_id']
    title = video_info['title']
    print(f"视频ID: {video_id}")
    print(f"标题: {title}")

    transcript = ""
    if not no_audio:
        print("\n【步骤2】下载视频...")
        video_path = download_video(link, str(TEMP_PATH))
        print(f"视频已保存: {video_path}")

        print("\n【步骤3】提取音频...")
        audio_path = extract_audio(video_path)

        print("\n【步骤4】语音识别...")
        transcript = transcribe_with_whisper(audio_path)
    else:
        print("⚠️  跳过音频处理，仅保存视频信息")

    print("\n【步骤5】保存到 Obsidian...")
    note_path = save_to_obsidian(video_id, title, transcript, link)

    if not keep_temp and not no_audio:
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
    print("\n文件已直接保存到 Obsidian 目录：")
    print(f"  - 笔记文件: {note_path}")

    return {
        'video_id': video_id,
        'title': title,
        'transcript': transcript,
        'note_path': note_path
    }


def main():
    parser = argparse.ArgumentParser(
        description="抖音视频下载和转录工具"
    )

    parser.add_argument("--link", "-l", required=True, help="抖音分享链接")
    parser.add_argument("--keep-temp", "-k", action="store_true",
                        help="保留临时文件（视频、音频）")
    parser.add_argument("--no-audio", "-n", action="store_true",
                        help="跳过音频处理，仅保存视频信息")

    args = parser.parse_args()

    try:
        process_douyin_video(
            link=args.link,
            keep_temp=args.keep_temp,
            no_audio=args.no_audio
        )
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
