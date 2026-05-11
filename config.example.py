
"""
抖音转Obsidian配置文件示例
请复制此文件为 config.py 并修改配置
"""
from pathlib import Path
import os

# ==================== 配置区域 ====================

# Obsidian 仓库路径（必须修改）
# 示例：
# Windows: Path("D:/TRAE_SOLO/obsidian文件")
# macOS: Path("~/Documents/ObsidianVault")
# Linux: Path("~/Documents/ObsidianVault")
OBSIDIAN_PATH = Path("D:/TRAE_SOLO/obsidian文件")

# 临时文件目录（可以使用相对路径）
TEMP_PATH = Path("douyin_temp")

# 默认分类目录
DEFAULT_CATEGORY = "产品资讯"

# ==================== 高级配置 ====================

# Whisper 模型大小（可选：tiny, base, small, medium, large）
WHISPER_MODEL = "base"

# ==================== 自动配置 ====================

# 确保目录存在
TEMP_PATH.mkdir(parents=True, exist_ok=True)

# 自动配置 FFmpeg 路径
def setup_ffmpeg():
    """自动配置 FFmpeg 路径"""
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        ffmpeg_dir = Path(ffmpeg_path).parent
        os.environ['PATH'] = str(ffmpeg_dir) + os.pathsep + os.environ['PATH']
        return True
    except:
        print("警告: 无法自动配置 FFmpeg")
        return False

setup_ffmpeg()

