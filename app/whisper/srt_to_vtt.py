def convert_srt_to_vtt(srt_file):
    """
    将 SRT 文件转换为 VTT 文件
    """
    vtt_file = srt_file.replace(".srt", ".vtt")
    
    with open(srt_file, "r") as srt, open(vtt_file, "w") as vtt:
        vtt.write("WEBVTT\n\n")
        
        for line in srt:
            # 简单的 SRT 到 VTT 的转换（这里只是基础转换，可能需要根据 SRT 格式更复杂的处理）
            vtt.write(line)
    
    return vtt_file
