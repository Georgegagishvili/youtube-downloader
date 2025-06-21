from pytubefix import YouTube
from core import merge_video_audio
from core import ProgressTracker


def fetch_resolutions(video_url):
    yt = YouTube(video_url)
    streams = yt.streams.filter(progressive=False, file_extension='mp4', only_video=True)
    return sorted({s.resolution for s in streams if s.resolution}, reverse=True)


def make_on_progress_callback(total_size: int, tracker: ProgressTracker):
    def on_progress(_, __, bytes_remaining):
        bytes_downloaded = total_size - bytes_remaining
        tracker.update(bytes_downloaded, total_size)

    return on_progress


def download_video_audio(url, resolution, tracker, merge_label, root):
    yt_video = YouTube(url)

    video_stream = yt_video.streams.filter(
        progressive=False, file_extension='mp4', resolution=resolution
    ).first()

    if not video_stream:
        raise Exception(f"Video stream not found for resolution {resolution}.")

    video_progress_callback = make_on_progress_callback(video_stream.filesize or 0, tracker)
    yt_video.on_progress_callback = video_progress_callback

    video_stream.download(output_path=".", filename='temp_video.mp4')

    tracker.update(0, 1)
    root.update_idletasks()

    yt_audio = YouTube(url)
    audio_stream = yt_audio.streams.filter(only_audio=True).order_by('abr').desc().first()

    if not audio_stream:
        raise Exception("No audio stream found.")

    audio_progress_callback = make_on_progress_callback(audio_stream.filesize or 0, tracker)
    yt_audio.on_progress_callback = audio_progress_callback

    audio_stream.download(output_path=".", filename='temp_audio.mp4')

    merge_label.config(text="Merging video and audio...")
    root.update_idletasks()
    merge_video_audio(label=merge_label)
    merge_label.config(text="Merging complete!")

    tracker.update(audio_stream.filesize or 0, audio_stream.filesize or 0)
