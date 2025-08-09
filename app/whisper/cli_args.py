def map_ui_params_to_whisper_cli_params(ui_params):
    """
    将 UI 中的参数映射为 whisper-cli 的命令行参数
    """
    whisper_params = []
    
    if "language" in ui_params:
        whisper_params.append(f"--language {ui_params['language']}")
    if "model" in ui_params:
        whisper_params.append(f"--model {ui_params['model']}")
    if "temperature" in ui_params:
        whisper_params.append(f"--temperature {ui_params['temperature']}")
    if "output_srt" in ui_params and ui_params["output_srt"]:
        whisper_params.append("--output-srt")
    
    # 更多参数的映射...
    
    return whisper_params
