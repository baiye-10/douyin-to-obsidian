
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抖音视频自动转Obsidian笔记 - 完整流程脚本
"""

import os
import sys
import argparse
import re
from pathlib import Path
from datetime import datetime

# 添加douyin-video技能到路径
skill_dir = Path(__file__).parent.parent.parent / "douyin-video" / "scripts"
sys.path.insert(0, str(skill_dir))

from douyin_downloader import get_video_info, download_video

# 配置路径
OBSIDIAN_PATH = Path("D:/TRAE_SOLO/obsidian文件")
TEMP_PATH = Path("D:/一人公司/自媒体/douyin_temp")
TEMP_PATH.mkdir(parents=True, exist_ok=True)


def setup_ffmpeg():
    """设置FFmpeg路径"""
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        ffmpeg_dir = Path(ffmpeg_path).parent
        os.environ['PATH'] = str(ffmpeg_dir) + os.pathsep + os.environ['PATH']
        return True
    except:
        return False


def extract_audio_moviepy(video_path, audio_path=None):
    """使用MoviePy从视频中提取音频"""
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
    """使用Whisper本地模型进行语音识别"""
    import whisper

    print("正在加载Whisper模型...")
    model = whisper.load_model('base')

    print("正在识别语音...")
    result = model.transcribe(str(audio_path), language='zh')

    print(f"语音识别完成，共 {len(result['text'])} 字")
    return result['text']


def generate_structured_notes(title, transcript, video_id, author="秋芝2046"):
    """生成结构化的Obsidian笔记内容"""

    # 清理标题中的特殊字符
    clean_title = re.sub(r'[\\/:*?"&lt;&gt;|]', '_', title)

    # 生成笔记内容
    notes_content = f"""---
title: {clean_title}
tags: [TRAE, AI, 效率]
date: {datetime.now().strftime('%Y-%m-%d')}
video_id: {video_id}
source: 抖音
author: {author}
---

# {clean_title}

&gt; [!info] 视频信息
&gt; - 作者：{author}
&gt; - 视频ID：{video_id}
&gt; - 内容来源：🧠 **Whisper 本地语音识别**（真实转录，非AI生成）

---

## 核心内容

&gt; [!summary] 一句话总结
&gt; （请根据内容自行填写）

---

## 完整转录

{transcript}
"""
    return notes_content


def update_knowledge_index(note_title, category="产品资讯"):
    """更新知识索引"""
    index_path = OBSIDIAN_PATH / "00-知识索引.md"

    if not index_path.exists():
        print("知识索引文件不存在，跳过更新")
        return

    print("正在更新知识索引...")

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已经有这个分类
    category_header = f"## 📱 {category}"
    if category_header not in content:
        # 添加新分类
        new_section = f"\n\n{category_header}\n\n&gt; [!note] 已整理的笔记\n\n| 序号 | 笔记 | 核心主题 |\n|------|------|----------|\n| 1 | [[{note_title}]] | {note_title} |\n"
        content = content.replace("## 🎮 游戏策划", new_section + "\n## 🎮 游戏策划")
    else:
        # 在现有分类中添加
        section_pattern = f"{category_header}.*?(?=##|$)"
        match = re.search(section_pattern, content, re.DOTALL)
        if match:
            section = match.group(0)
            # 找到表格并添加新行
            if "|------|------|----------|" in section:
                lines = section.split('\n')
                table_start = None
                table_end = None
                for i, line in enumerate(lines):
                    if "| 序号 | 笔记 | 核心主题 |" in line:
                        table_start = i
                    elif table_start is not None and line.startswith("|") and i &gt; table_start:
                        table_end = i
                    elif table_start is not None and not line.startswith("|"):
                        break

                if table_end is not None:
                    # 获取当前最大序号
                    current_rows = [line for line in lines[table_start+2:table_end+1] if line.startswith("|")]
                    next_num = len(current_rows) + 1
                    new_row = f"| {next_num} | [[{note_title}]] | {note_title} |"
                    lines.insert(table_end + 1, new_row)
                    new_section = '\n'.join(lines)
                    content = content.replace(section, new_section)

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print("知识索引已更新")


def process_douyin_video(link, category="产品资讯", keep_temp=False):
    """完整处理流程"""

    print("=" * 60)
    print("抖音视频转Obsidian笔记 - 开始处理")
    print("=" * 60)

    # 步骤1: 解析链接
    print("\n【步骤1】解析抖音链接...")
    video_info = get_video_info(link)
    print(f"✓ 视频ID: {video_info['video_id']}")
    print(f"✓ 标题: {video_info['title']}")

    # 步骤2: 下载视频
    print("\n【步骤2】下载视频...")
    video_path = download_video(link, str(TEMP_PATH))
    print(f"✓ 视频已保存: {video_path}")

    # 步骤3: 提取音频
    print("\n【步骤3】提取音频...")
    setup_ffmpeg()
    audio_path = extract_audio_moviepy(video_path)

    # 步骤4: 语音识别
    print("\n【步骤4】语音识别...")
    transcript = transcribe_with_whisper(audio_path)

    # 保存原始转录
    transcript_path = TEMP_PATH / f"{video_info['video_id']}_transcript.txt"
    with open(transcript_path, 'w', encoding='utf-8') as f:
        f.write(transcript)
    print(f"✓ 原始转录已保存: {transcript_path}")

    # 步骤5: 生成Obsidian笔记
    print("\n【步骤5】生成Obsidian笔记...")
    clean_title = re.sub(r'[\\/:*?"&lt;&gt;|]', '_', video_info['title'])
    notes_content = generate_structured_notes(
        title=clean_title,
        transcript=transcript,
        video_id=video_info['video_id']
    )

    # 保存笔记
    notes_dir = OBSIDIAN_PATH / category
    notes_dir.mkdir(parents=True, exist_ok=True)
    notes_path = notes_dir / f"{clean_title}.md"

    with open(notes_path, 'w', encoding='utf-8') as f:
        f.write(notes_content)

    print(f"✓ Obsidian笔记已生成: {notes_path}")

    # 步骤6: 更新知识索引
    print("\n【步骤6】更新知识索引...")
    update_knowledge_index(clean_title, category)

    # 清理临时文件
    if not keep_temp:
        print("\n【清理】删除临时文件...")
        try:
            vp = Path(video_path)
            if vp.exists():
                vp.unlink()
            ap = Path(audio_path)
            if ap.exists():
                ap.unlink()
            if transcript_path.exists():
                transcript_path.unlink()
            print("✓ 临时文件已清理")
        except Exception as e:
            print(f"警告: 清理临时文件时出错: {e}")

    print("\n" + "=" * 60)
    print("✓ 处理完成!")
    print(f"笔记位置: {notes_path}")
    print("=" * 60)

    return {
        "video_info": video_info,
        "notes_path": notes_path,
        "transcript": transcript
    }


def main():
    parser = argparse.ArgumentParser(
        description="抖音视频自动转Obsidian笔记"
    )

    parser.add_argument("--link", "-l", required=True, help="抖音分享链接")
    parser.add_argument("--category", "-c", default="产品资讯", help="Obsidian笔记分类目录（默认：产品资讯）")
    parser.add_argument("--keep-temp", "-k", action="store_true", help="保留临时文件")

    args = parser.parse_args()

    try:
        process_douyin_video(
            link=args.link,
            category=args.category,
            keep_temp=args.keep_temp
        )
    except Exception as e:
        print(f"\n错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

