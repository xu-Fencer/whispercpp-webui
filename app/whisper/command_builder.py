from __future__ import annotations
from typing import Dict, List, Any
from app.config import config


def _truthy(v: Any) -> bool:
    if isinstance(v, bool):
        return v
    if v is None:
        return False
    s = str(v).strip().lower()
    return s in ("1", "true", "yes", "on")


def build_whisper_command(input_file: str, output_format: str, whisper_params: Dict[str, Any]) -> List[str]:
    """
    生成 whisper 命令行（数组形式）。
    - 可执行文件：始终使用 settings.json 的 whisper_path
    - 模型：优先 whisper_params.model，否则回退 settings.json 的 model_path
    - 参数兼容前端：threads, beam_size, best_of, language, translate
    - output_format 单独传入（srt/vtt/json/txt），根据你的 CLI 实际参数名必要时调整
    """
    exe = config.get("whisper_path") or ""
    if not exe:
        raise ValueError("whisper_path is not configured in settings.json")
    model = whisper_params.get("model") or config.get("model_path") or ""
    if not model:
        raise ValueError("model path is not provided (whisper_params.model or settings.json model_path)")

    # 你原来的 CLI 例子用法参考：
    # whisper-cli -f <input> -o <output_base> --model <model> --threads N --beam-size N --best-of N --language xx --translate
    # 如果 output_base 需要，默认使用 "output"（会在任务目录内执行）
    output_base = whisper_params.get("output_file", "output")
# aa#这个-o不对
    cmd: List[str] = [exe, "-f", input_file, "-o", output_base, "--model", model]

    # 数值参数
    if "threads" in whisper_params and whisper_params["threads"] is not None:
        cmd += ["--threads", str(whisper_params["threads"])]
    if "beam_size" in whisper_params and whisper_params["beam_size"] is not None:
        cmd += ["--beam-size", str(whisper_params["beam_size"])]
    if "best_of" in whisper_params and whisper_params["best_of"] is not None:
        cmd += ["--best-of", str(whisper_params["best_of"])]

    # 语言
    language = whisper_params.get("language")
    if language and str(language).lower() != "auto":
        cmd += ["--language", str(language)]

    # 布尔开关：translate
    if _truthy(whisper_params.get("translate")):
        cmd += ["--translate"]

    # 输出格式（如果你的 CLI 用法不同，请在此改为对应参数）
    # 例如有的 CLI 用 --output-format，有的用 -of 等
    if output_format:
        cmd += ["--output-format", output_format]

    return cmd
