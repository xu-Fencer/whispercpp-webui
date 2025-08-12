from typing import Dict, List, Any
from app.config import config
from app.whisper.cli_args import WHISPER_CLI_ARGS, TYPE_BOOL


def build_whisper_command(
    input_file: str, 
    output_file_base: str, 
    whisper_params: Dict[str, Any]
) -> List[str]:
    """
    根据 WHISPER_CLI_ARGS 和用户输入参数，生成 whisper.cpp 命令行。
    """
    exe = config.get("whisper_path")
    if not exe:
        raise ValueError("Whisper 可执行文件路径未在设置中配置")

    model_path = config.get("model_path")
    if not model_path:
        raise ValueError("模型路径未在设置中配置")

    cmd = [exe, "-m", model_path, "-f", input_file, "-of", output_file_base]

    for key, definition in WHISPER_CLI_ARGS.items():
        user_value = whisper_params.get(key)

        # 如果用户未提供值，则跳过（不使用默认值）
        if user_value is None:
            continue

        cli_flag = definition["cli"][0]  # 使用第一个 flag
        param_type = definition["type"]

        if param_type == TYPE_BOOL:
            if user_value:
                cmd.append(cli_flag)
        else:
            # 对于非布尔类型，如果值不为空，则添加
            if user_value:
                cmd.extend([cli_flag, str(user_value)])

    return cmd

