
# 抖音转Obsidian Skill

一键完成抖音视频处理全流程：解析链接 → 下载视频 → 提取音频 → Whisper语音识别 → 生成Obsidian结构化笔记。

## ✨ 功能特性

- 🚀 **完整流程自动化**：从抖音链接到Obsidian笔记，一键搞定
- 🔊 **本地语音识别**：使用Whisper本地模型，无需API密钥
- 📝 **智能笔记生成**：自动生成结构化Obsidian笔记
- 🔧 **灵活配置**：支持自定义路径和参数

## 📦 安装

### 1. 克隆或下载

```bash
# 如果是GitHub项目
git clone https://github.com/你的用户名/douyin-to-obsidian.git
```

### 2. 安装依赖

```bash
pip install requests moviepy openai-whisper
```

### 3. 配置

复制配置文件示例：

```bash
cp config.example.py config.py
```

编辑 `config.py`，修改为你自己的路径：

```python
# Obsidian 仓库路径（必须修改）
OBSIDIAN_PATH = Path("D:/TRAE_SOLO/obsidian文件")  # Windows
# OBSIDIAN_PATH = Path("~/Documents/ObsidianVault")  # macOS/Linux
```

### 4. 确保依赖Skill存在

这个Skill依赖 `douyin-video` 技能，请确保它在同一目录下：

```
.trae/skills/
├── douyin-video/          ← 必须存在
│   └── scripts/
│       └── douyin_downloader.py
└── douyin-to-obsidian/    ← 这个技能
    ├── config.py
    ├── douyin_to_obsidian.py
    └── SKILL.md
```

## 🚀 使用方法

### 方法1：在对话中使用（推荐）

直接跟AI说：
- "总结这个抖音视频：[链接]"
- "把这个视频导入Obsidian：[链接]"
- "处理这个抖音：[链接]"

### 方法2：命令行使用

```bash
# 完整处理流程
python douyin_to_obsidian.py --link "抖音分享链接"

# 指定保存目录
python douyin_to_obsidian.py --link "抖音分享链接" --category "产品资讯"

# 保留临时文件
python douyin_to_obsidian.py --link "抖音分享链接" --keep-temp
```

## 📁 文件结构

```
douyin-to-obsidian/
├── SKILL.md              # Skill说明文档
├── README.md             # 这个文件
├── config.example.py     # 配置文件示例
├── config.py             # 你的配置（不会上传到Git）
├── douyin_to_obsidian.py # 主脚本
└── .gitignore           # Git忽略文件
```

## ⚙️ 配置说明

### config.py 配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `OBSIDIAN_PATH` | Obsidian仓库路径（必填） | - |
| `TEMP_PATH` | 临时文件目录 | `douyin_temp` |
| `DEFAULT_CATEGORY` | 默认分类目录 | `产品资讯` |
| `WHISPER_MODEL` | Whisper模型大小 | `base` |

### Whisper模型选项

| 模型 | 大小 | 速度 | 质量 |
|------|------|------|------|
| `tiny` | ~39MB | 最快 | 一般 |
| `base` | ~74MB | 快 | 良好 |
| `small` | ~244MB | 中等 | 好 |
| `medium` | ~769MB | 慢 | 很好 |
| `large` | ~1550MB | 最慢 | 最好 |

## 📄 输出格式

生成的Obsidian笔记包含：

- ✅ Frontmatter（标题、标签、日期、视频ID）
- ✅ 视频信息Callout
- ✅ 核心内容区域
- ✅ 完整转录文本

## 🔄 工作流程

1. **解析链接**：获取视频信息和下载地址
2. **下载视频**：保存无水印视频到临时目录
3. **提取音频**：从视频中提取MP3音频
4. **语音识别**：使用Whisper本地模型转录
5. **生成笔记**：创建Obsidian格式的Markdown文件
6. **更新索引**：自动更新知识索引

## ⚠️ 注意事项

- 首次运行会自动下载Whisper模型（约150MB for base模型）
- 语音识别使用本地模型，保护隐私
- 请遵守抖音相关服务条款

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

