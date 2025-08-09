import os

def is_valid_file_path(file_path: str, task_dir: str) -> bool:
    """
    验证文件路径是否在指定的任务目录内
    """
    # 确保文件路径在任务目录内，避免路径穿越攻击
    return os.path.commonpath([file_path, task_dir]) == task_dir

def check_file_size(file_path: str, max_size_mb: int) -> bool:
    """
    检查文件大小，防止上传过大的文件
    """
    file_size = os.path.getsize(file_path) / (1024 * 1024)  # 转换为 MB
    return file_size <= max_size_mb

def check_file_mime(file_path: str, allowed_mime_types: list) -> bool:
    """
    检查文件 MIME 类型，防止上传不允许的文件类型
    """
    import mimetypes
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type in allowed_mime_types
