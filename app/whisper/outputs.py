import os

def save_output(output_dir, output_format, content):
    """
    将识别结果保存为指定格式的文件
    """
    output_path = os.path.join(output_dir, f"output.{output_format}")
    
    if output_format == "txt":
        with open(output_path, "w") as f:
            f.write(content)
    elif output_format == "json":
        import json
        with open(output_path, "w") as f:
            json.dump(content, f)
    elif output_format == "srt" or output_format == "vtt":
        with open(output_path, "w") as f:
            f.write(content)
    else:
        raise ValueError("Unsupported output format")
    
    return output_path
