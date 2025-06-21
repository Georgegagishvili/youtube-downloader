import os
import subprocess

from imageio_ffmpeg import get_ffmpeg_exe


def merge_video_audio(video_path: str, audio_path: str, output_path: str, label):
    label.config(text="Merging video and audio...")
    label.update()
    ffmpeg_path = get_ffmpeg_exe()

    subprocess.run([
        ffmpeg_path,
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        output_path
    ])

    os.remove(video_path)
    os.remove(audio_path)

    label.config(text="Merging complete!")
    label.update()
