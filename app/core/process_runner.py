import subprocess
import os

def run_whisper_process(command, job_id, task_dir):
    # 启动 Whisper 命令并将输出保存到日志文件
    log_file = os.path.join(task_dir, "log.txt")
    with open(log_file, "w") as log:
        process = subprocess.Popen(command, stdout=log, stderr=log, text=True)
    return process
