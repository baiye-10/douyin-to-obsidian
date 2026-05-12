***

name: douyin-to-obsidian
description: "抖音视频自动下载和转录工具（优化版） - 解析链接、下载视频、提取音频、Whisper本地语音识别、自动修正错字、直接保存到Obsidian。已解决Python依赖问题。"
--------------------------------------------------------------------------------------------------

# 抖音视频转 Obsidian 工具（优化版）

## 优化内容

✅ **直接保存到 Obsidian** - 笔记自动保存到 `D:/TRAE_SOLO/obsidian文件`  
✅ **自动修正错字** - 内置常见语音识别错误修正表  
✅ **解决 Python 依赖** - 使用指定 Python 路径 `D:/python.org/python.exe`  
✅ **更友好的格式** - 自动生成 Frontmatter 和笔记模板

## 工作方式

### 1. Skill 脚本负责（机械性工作）
- ✅ 解析抖音链接，获取视频ID和标题
- ✅ 下载无水印视频
- ✅ 从视频中提取音频
- ✅ 使用 Whisper 进行本地语音识别
- ✅ 自动修正常见错字（避允→毕昇、音乐局儿→Claude）
- ✅ **直接保存到 Obsidian 目录**（带 Frontmatter）

### 2. AI 助手负责（智能性工作）
- ✅ 读取转录文件
- ✅ 智能分析内容，提取重点
- ✅ 生成结构化 Obsidian 笔记

***

## 使用方法

### 方法1：在对话中直接使用（推荐）

直接跟 AI 说：
```
总结这个抖音视频：[抖音链接]
把这个视频导入Obsidian：[抖音链接]
处理这个抖音：[抖音链接]
```

AI 会自动：
1. 调用此 skill 进行下载和转录
2. 文件直接保存到 Obsidian
3. 读取文件并智能总结

### 方法2：命令行使用

```bash
# 完整处理（下载+转录）
python douyin_to_obsidian.py --link "抖音分享链接"

# 保留临时文件
python douyin_to_obsidian.py --link "抖音分享链接" --keep-temp

# 仅保存视频信息（跳过音频）
python douyin_to_obsidian.py --link "抖音分享链接" --no-audio
```

#### 参数说明
- `--link`: 抖音分享链接（必填）
- `--keep-temp`: 保留临时文件（视频、音频）
- `--no-audio`: 跳过音频处理，仅保存视频信息

***

## 输出文件

| 文件 | 路径 | 说明 |
| ---- | ---- | ---- |
| Obsidian 笔记 | `D:/TRAE_SOLO/obsidian文件/{日期}-{视频ID}.md` | 带 Frontmatter 的完整笔记 |

***

## 配置说明

脚本开头可修改以下配置：

```python
# Obsidian 仓库路径
OBSIDIAN_PATH = Path("D:/TRAE_SOLO/obsidian文件")

# 临时文件目录
TEMP_PATH = Path("D:/一人公司/自媒体/douyin_temp")

# Whisper 模型大小
WHISPER_MODEL = "base"

# 指定的 Python 路径（解决依赖问题）
PYTHON_PATH = "D:/python.org/python.exe"
```

### 常见错字自动修正

内置的修正表（可在脚本中修改）：
- 避允 → 毕昇
- 音乐局儿/音乐局 → Claude
- 米游/米友 → 米哈游
- 崩铁 → 星穹铁道
- 崩三 → 崩坏3
- AI/GPT/Claude/Transformer 等技术名词保持原样

***

## 依赖环境

### Python 包（已配置到指定 Python）
- requests
- moviepy
- openai-whisper
- imageio-ffmpeg

### 解决依赖问题
如果 SOLO 内置 Python 缺少依赖，脚本会自动使用 `D:/python.org/python.exe` 执行 Whisper 识别。

***

## 注意事项

- ⚠️ 首次运行会自动下载 Whisper base 模型（约 150MB）
- ⚠️ 所有处理在本地完成，保护隐私
- ⚠️ 请遵守抖音相关服务条款
- ⚠️ **文件会直接保存到 Obsidian**，无需手动复制！
