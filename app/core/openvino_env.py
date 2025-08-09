import subprocess
import os
import json

def run_openvino_script():
    """执行 OpenVINO 脚本，并测试环境变量"""
    # 读取 settings 文件
    with open("app/settings.json", "r") as f:
        settings = json.load(f)

    script = settings.get("openvino_script_path")
    if not script or not os.path.exists(script):
        return False, "OpenVINO script not found"

    # 执行 OpenVINO 脚本
    try:
        result = subprocess.check_output([script], shell=True, stderr=subprocess.STDOUT)
        return True, result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return False, e.output.decode('utf-8')
