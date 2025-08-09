def build_whisper_command(input_file, output_format, whisper_params):
    """
    生成 whisper-cli 命令行
    """
    command = [
        "whisper-cli",
        "-f", input_file,
        "-o", whisper_params.get("output_file", "output"),
        "--model", whisper_params["model"],
    ]
    
    # 动态附加命令行参数
    for param, value in whisper_params.items():
        if param in ["output_file", "model"]:
            continue  # 已经加过了
        command.extend([f"--{param}", str(value)])

    return command
