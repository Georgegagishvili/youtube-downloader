import os
import subprocess
from imageio_ffmpeg import get_ffmpeg_exe


def merge_video_audio(label):
    label.config(text="Merging video and audio...")
    label.update()
    ffmpeg_path = get_ffmpeg_exe()

    video_name = 'temp_video.mp4'
    audio_name = 'temp_audio.mp4'
    subprocess.run([
        ffmpeg_path,
        "-y",
        "-i", video_name,
        "-i", audio_name,
        "-c:v", "copy",
        "-c:a", "aac",
        "video.mp4"
    ])

    os.remove(video_name)
    os.remove(audio_name)

    label.config(text="Merging complete!")
    label.update()
