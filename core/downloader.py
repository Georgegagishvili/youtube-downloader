from pytubefix import YouTube
import tkinter as tk
from typing import Optional
from .ffmpeg import merge_video_audio
from .progress import ProgressTracker

# Cache for YouTube instances by URL
_yt_cache: dict[str, YouTube] = {}


def get_yt_instance(url: str) -> YouTube:
    if url not in _yt_cache:
        _yt_cache[url] = YouTube(url)
    return _yt_cache[url]


def fetch_resolutions(video_url: str) -> list[str]:
    yt = get_yt_instance(video_url)
    streams = yt.streams.filter(progressive=False, file_extension='mp4', only_video=True)
    resolutions = {s.resolution for s in streams if s.resolution and s.resolution.endswith("p")}
    return sorted(resolutions, key=lambda x: int(x.replace("p", "")), reverse=True)


def fetch_audio_qualities(video_url: str) -> list[str]:
    yt = get_yt_instance(video_url)
    streams = yt.streams.filter(only_audio=True)
    bit_rates = {s.abr for s in streams if s.abr and s.abr.endswith("kbps")}
    return sorted(bit_rates, key=lambda x: int(x.replace("kbps", "")), reverse=True)


def make_on_progress_callback(total_size: int, tracker: ProgressTracker, root: tk.Tk):
    print(f"Total size for download: {total_size} bytes")

    def on_progress(_, __, bytes_remaining):
        bytes_downloaded = total_size - bytes_remaining
        print(f"Downloaded {bytes_downloaded} of {total_size} bytes ({(bytes_downloaded / total_size) * 100:.2f}%)")
        root.after(0, lambda: tracker.update(bytes_downloaded, total_size))

    return on_progress


def download_video(url: str, resolution: str, tracker: ProgressTracker, root: tk.Tk):
    yt = get_yt_instance(url)
    stream = yt.streams.filter(
        progressive=False, file_extension='mp4', resolution=resolution
    ).first()

    if not stream:
        raise Exception(f"Video stream not found for resolution {resolution}.")

    yt.register_on_progress_callback(make_on_progress_callback(stream.filesize or 0, tracker, root))
    stream.download(output_path=".", filename="video_only.mp4")

    print("Note: This is a video-only file and may not play properly in some players.")


def download_audio(url: str, tracker: ProgressTracker, root: tk.Tk, abr: Optional[str] = None):
    yt = get_yt_instance(url)
    stream_query = yt.streams.filter(only_audio=True)

    if abr:
        stream_query = stream_query.filter(abr=abr)

    stream = stream_query.order_by('abr').desc().first()

    if not stream:
        raise Exception(f"No audio stream found for quality '{abr or 'best'}'.")

    yt.register_on_progress_callback(make_on_progress_callback(stream.filesize or 0, tracker, root))
    stream.download(output_path=".", filename="audio_only.mp4")


def download_video_audio(url: str, resolution: str, tracker: ProgressTracker, merge_label, root):
    yt = get_yt_instance(url)

    video_stream = yt.streams.filter(progressive=False, file_extension='mp4', resolution=resolution).first()
    if not video_stream:
        raise Exception(f"Video stream not found for resolution {resolution}.")

    yt.register_on_progress_callback(make_on_progress_callback(video_stream.filesize or 0, tracker, root))
    video_stream.download(output_path=".", filename="temp_video.mp4")

    root.after(0, lambda: tracker.update(0, 1))
    root.after(0, root.update_idletasks)

    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    if not audio_stream:
        raise Exception("No audio stream found.")

    yt.register_on_progress_callback(make_on_progress_callback(audio_stream.filesize or 0, tracker, root))
    audio_stream.download(output_path=".", filename="temp_audio.mp4")

    root.after(0, lambda: merge_label.config(text="Merging video and audio..."))
    root.after(0, root.update_idletasks)

    merge_video_audio(label=merge_label)

    root.after(0, lambda: merge_label.config(text="Merging complete!"))
    root.after(0, lambda: tracker.update(audio_stream.filesize or 0, audio_stream.filesize or 0))
