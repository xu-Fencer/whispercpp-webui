"""
从 whisper-args.json 加载 whisper.cpp 的命令行参数定义。
"""
import json
from pathlib import Path

# 参数类型（保持不变）
TYPE_BOOL = "boolean"
TYPE_INT = "integer"
TYPE_FLOAT = "float"
TYPE_STRING = "string"

# 获取当前文件所在目录
current_dir = Path(__file__).parent.parent

# JSON 文件路径
json_path = current_dir / "whisper-args.json"

# 从 JSON 文件加载参数定义
try:
    with open(json_path, "r", encoding="utf-8") as f:
        WHISPER_CLI_ARGS = json.load(f)
except FileNotFoundError:
    # 如果文件不存在，可以抛出错误或使用一个空的默认值
    WHISPER_CLI_ARGS = {}
    print(f"Error: {json_path} not found.")
except json.JSONDecodeError:
    # 如果 JSON 解析失败
    WHISPER_CLI_ARGS = {}
    print(f"Error: Failed to decode JSON from {json_path}.")

