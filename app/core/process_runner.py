import subprocess
import os
import sys
from typing import List, Tuple
from app.config import config


def _is_windows() -> bool:
    return os.name == "nt"


def _build_shell_command_with_openvino(cmd_list: List[str]) -> Tuple[str, bool]:
    """
    将 OpenVINO 脚本与 whisper 命令拼在同一个 shell 会话中执行。
    返回：(shell_command, use_shell=True)
    """
    script = config.get("openvino_script_path") or ""
    if not script:
        # 没有脚本就返回原始命令
        return " ".join(subprocess.list2cmdline([x]) for x in cmd_list), True

    # 注意：在 Windows 需要 call，Linux/Mac 需要 source
    quoted_whisper = subprocess.list2cmdline(cmd_list)
    if _is_windows():
        # cmd /C "call script && whisper ..."
        shell_cmd = f'call "{script}" && {quoted_whisper}'
        return shell_cmd, True
    else:
        # bash -lc 'source script && whisper ...'
        # 在 Popen 中将使用: executable="/bin/bash"
        shell_cmd = f'source "{script}" && {quoted_whisper}'
        return shell_cmd, True


def run_whisper_process(command: List[str], task_dir: str):
    """
    在 task_dir 内启动 Whisper 命令行。
    如果 openvino_enabled=True，则在同一 shell 会话先执行 OpenVINO 脚本。
    """
    os.makedirs(task_dir, exist_ok=True)

    use_openvino = bool(config.get("openvino_enabled", False))

    common_popen_args = {
        "cwd": task_dir,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,  # 合并 stdout 和 stderr
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",  # 避免解码错误
    }

    if use_openvino:
        shell_cmd, _ = _build_shell_command_with_openvino(command)
        if _is_windows():
            process = subprocess.Popen(shell_cmd, **common_popen_args, shell=True)
        else:
            process = subprocess.Popen(
                ["bash", "-lc", shell_cmd], **common_popen_args
            )
        return process

    # 不使用 OpenVINO，直接运行
    process = subprocess.Popen(command, **common_popen_args)
    return process
