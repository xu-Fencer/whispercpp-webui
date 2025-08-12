import subprocess
import os
import json

def run_openvino_script():
    """
    仅执行 OpenVINO 初始化脚本并返回输出结果，用于“测试脚本”按钮。
    实际在任务运行时会在同一 shell 会话中先执行脚本再执行 whisper（见 process_runner）。
    """
    with open("app/settings.json", "r", encoding="utf-8") as f:
        settings = json.load(f)

    script = settings.get("openvino_script_path")
    if not script or not os.path.exists(script):
        return False, "OpenVINO script not found"

    try:
        # Windows .bat 通常需要通过 cmd 调用；Linux/Mac 通过 bash 调用
        if os.name == "nt":
            result = subprocess.check_output(f'cmd /C call "{script}"', shell=True, stderr=subprocess.STDOUT)
        else:
            result = subprocess.check_output(f'bash -lc \'source "{script}" && env\'', shell=True, stderr=subprocess.STDOUT)
        return True, result.decode('utf-8', errors='ignore')
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8', errors='ignore')
