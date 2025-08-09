import subprocess
import os

def ffmpeg_probe(file_path):
    """
    使用 ffprobe 探测音频文件的属性（如采样率、声道）
    """
    try:
        result = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=sample_rate,channels", "-of", "default=noprint_wrappers=1", file_path])
        return result.decode("utf-8")
    except subprocess.CalledProcessError:
        return None

def convert_audio_to_wav(input_file, output_file):
    """
    转换音频文件到 16kHz 单声道 WAV 格式
    """
    command = [
        "ffmpeg", "-i", input_file,
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", output_file
    ]
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        return False
