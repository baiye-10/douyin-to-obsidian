# douyin-to-obsidian

抖音视频自动转 Obsidian 笔记的 Trae/Claude 技能。解析链接、下载无水印视频、Whisper 本地语音识别、自动修正错字、生成结构化 Obsidian 笔记。

## 功能

- 🔗 解析抖音分享链接，获取视频信息和下载地址
- 📥 下载无水印视频
- 🎙️ 使用 Whisper 本地语音识别（中文优化）
- ✏️ 自动修正常见识别错误（可自定义修正规则）
- 📝 生成带 Frontmatter 的 Obsidian 笔记

## 文件结构

```
douyin-to-obsidian/
├── SKILL.md                    # 技能定义文件
├── douyin_to_obsidian.py       # 主脚本 - 完整工作流
├── douyin_downloader.py        # 下载模块 - 视频解析和下载（内含）
├── config.example.py           # 配置示例
├── text_corrections.json       # 错字修正配置
└── README.md                   # 本文件
```

> `douyin_downloader.py` 已包含在本 skill 中，无需额外下载。

## 安装

### 1. 安装 Python 依赖

```bash
pip install requests ffmpeg-python openai-whisper moviepy imageio-ffmpeg
```

### 2. 配置

复制 `config.example.py` 为 `config.py`，修改以下配置：

```python
OBSIDIAN_PATH = Path("你的Obsidian笔记仓库路径")
TEMP_PATH = Path("临时文件目录")
WHISPER_MODEL = "base"  # tiny, base, small, medium, large
```

如果不创建 `config.py`，脚本会使用默认值。

### 3. FFmpeg

Whisper 需要 FFmpeg。安装 `imageio-ffmpeg` 后会自动提供，无需手动安装。

## 使用

### 对话触发

直接对 AI 助手说：
- "总结这个抖音视频：[链接]"
- "把这个视频导入Obsidian：[链接]"

### 命令行

```bash
# 完整处理
python douyin_to_obsidian.py --link "抖音分享链接"

# 仅获取视频信息
python douyin_to_obsidian.py --link "抖音分享链接" --no-audio

# 保留临时文件
python douyin_to_obsidian.py --link "抖音分享链接" --keep-temp
```

### 单独使用下载模块

```bash
python douyin_downloader.py --link "链接" --action info
python douyin_downloader.py --link "链接" --action download --output ./videos
python douyin_downloader.py --link "链接" --action extract --output ./output
```

## 输出示例

```markdown
---
title: 视频标题
tags: [抖音, 视频笔记, 2026]
source: https://v.douyin.com/xxx
date: 2026-05-14
---

# 视频标题

## 原始内容

（Whisper 转录的完整文本）

## 笔记

- 
```

## 自定义错字修正

编辑 `text_corrections.json`：

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
| 找不到 douyin_downloader.py | 确保该文件与 douyin_to_obsidian.py 在同一目录 |
| Whisper 识别失败 | 检查 FFmpeg：`python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"` |
| 视频下载失败 | 重新获取抖音分享链接 |
| Obsidian 路径错误 | 修改 config.py 中的 OBSIDIAN_PATH |

## License

MIT
