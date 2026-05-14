---
name: "douyin-to-obsidian"
description: "抖音视频自动转Obsidian笔记。解析链接、下载无水印视频、Whisper本地语音识别、自动修正错字、生成结构化Obsidian笔记。触发：'总结这个抖音视频'、'把视频导入Obsidian'、'处理这个抖音'、发送抖音链接。"
---

# 抖音视频转 Obsidian 笔记

将抖音视频自动转换为结构化的 Obsidian 笔记，包含完整的语音转录和视频信息。

## 功能

- 解析抖音分享链接，获取视频信息和下载地址
- 下载无水印视频
- 使用 Whisper 本地语音识别（中文优化）
- 自动修正常见识别错误
- 生成带 Frontmatter 的 Obsidian 笔记

## 文件结构

```
douyin-to-obsidian/
├── SKILL.md                    # 本文件 - 技能定义
├── douyin_to_obsidian.py       # 主脚本 - 完整工作流
├── douyin_downloader.py        # 下载模块 - 视频解析和下载（内含，无需额外安装）
├── config.example.py           # 配置示例 - 复制为 config.py 后修改
├── text_corrections.json       # 错字修正配置
└── README.md                   # 详细文档
```

> **重要**：`douyin_downloader.py` 已包含在本 skill 目录中，无需额外下载。如果缺少此文件，脚本会给出清晰的错误提示。

## 前置依赖

### Python 包

```bash
pip install requests ffmpeg-python openai-whisper moviepy imageio-ffmpeg
```

### FFmpeg

Whisper 需要 FFmpeg。安装 `imageio-ffmpeg` 后会自动提供：

```python
import imageio_ffmpeg
print(imageio_ffmpeg.get_ffmpeg_exe())
```

### 硅基流动 API Key（可选）

如果使用云端语音识别（而非本地 Whisper），需要设置环境变量：

```bash
set API_KEY=your_siliconflow_api_key
```

## 配置

1. 复制 `config.example.py` 为 `config.py`
2. 修改以下配置项：

```python
OBSIDIAN_PATH = Path("你的Obsidian笔记仓库路径")
TEMP_PATH = Path("临时文件目录")
WHISPER_MODEL = "base"  # 可选: tiny, base, small, medium, large
PYTHON_PATH = sys.executable  # Python 解释器路径
```

> 如果不创建 `config.py`，脚本会使用默认值（Obsidian 路径为用户主目录下的 ObsidianVault）。

## 使用方式

### 方式一：对话触发（推荐）

直接对 AI 助手说：
- "总结这个抖音视频：[链接]"
- "把这个视频导入Obsidian：[链接]"
- "处理这个抖音：[链接]"

### 方式二：命令行

```bash
# 完整处理（下载+识别+保存Obsidian）
python douyin_to_obsidian.py --link "抖音分享链接"

# 仅获取视频信息，不处理音频
python douyin_to_obsidian.py --link "抖音分享链接" --no-audio

# 保留临时文件（视频、音频）
python douyin_to_obsidian.py --link "抖音分享链接" --keep-temp
```

### 方式三：单独使用下载模块

```bash
# 获取视频信息
python douyin_downloader.py --link "链接" --action info

# 下载视频
python douyin_downloader.py --link "链接" --action download --output ./videos

# 提取文案（需要 API_KEY）
python douyin_downloader.py --link "链接" --action extract --output ./output
```

## 输出格式

生成的 Obsidian 笔记包含：

```markdown
---
title: 视频标题
tags: [抖音, 视频笔记, 2026]
source: 视频链接
date: 2026-05-14
---

# 视频标题

## 原始内容

（Whisper 转录的完整文本，已自动修正错字）

## 笔记

- 
```

## 错字修正

`text_corrections.json` 中配置了常见 Whisper 识别错误及修正，可自行扩展：

```json
{
  "common": {
    "音乐局": "Claude",
    "米游": "米哈游"
  }
}
```

## 故障排除

| 问题 | 解决方案 |
|------|---------|
| `找不到 douyin_downloader.py` | 确保该文件与 `douyin_to_obsidian.py` 在同一目录 |
| Whisper 识别失败 | 检查 FFmpeg 是否安装：`python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"` |
| 视频下载失败 | 抖音链接可能过期，重新获取分享链接 |
| Obsidian 路径错误 | 检查 `config.py` 中的 `OBSIDIAN_PATH` 是否正确 |
