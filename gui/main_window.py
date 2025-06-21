import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from threading import Thread

from core import (
    fetch_resolutions,
    fetch_audio_qualities,
    download_video_audio,
    download_video,
    download_audio,
)
from core import ProgressTracker

available_resolutions: list[str] = []
available_audio_qualities: list[str] = []

selected_resolution: Optional[tk.StringVar] = None
selected_audio_quality: Optional[tk.StringVar] = None

progress_var: Optional[tk.IntVar] = None
progress_label: Optional[tk.Label] = None
size_label: Optional[tk.Label] = None
merge_label: Optional[tk.Label] = None
url_entry: Optional[tk.Entry] = None
resolution_dropdown: Optional[ttk.Combobox] = None
audio_dropdown: Optional[ttk.Combobox] = None

window_width = 620
window_height = 250


def create_main_window():
    global selected_resolution, selected_audio_quality
    global progress_var, progress_label, size_label, merge_label
    global url_entry, resolution_dropdown, audio_dropdown

    root = tk.Tk()
    root.title("YouTube Video & Audio Downloader")
    root.geometry(f"{window_width}x{window_height}")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight() - 250

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 1.5))

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    selected_resolution = tk.StringVar()
    selected_audio_quality = tk.StringVar()

    # Row 1: URL Input
    row1 = tk.Frame(root)
    row1.pack(pady=(10, 0))
    tk.Label(row1, text="YouTube URL:").pack(side='left', padx=(0, 5))
    url_entry = tk.Entry(row1, width=50)
    url_entry.pack(side='left')

    # Row 2: Resolution + Audio Quality
    row2 = tk.Frame(root)
    row2.pack(pady=(10, 0))

    tk.Label(row2, text="Resolution:").pack(side='left', padx=(5, 5))
    resolution_dropdown = ttk.Combobox(row2, textvariable=selected_resolution, state='disabled', width=15)
    resolution_dropdown.pack(side='left', padx=(0, 20))

    tk.Label(row2, text="Audio Quality:").pack(side='left', padx=(5, 5))
    audio_dropdown = ttk.Combobox(row2, textvariable=selected_audio_quality, state='disabled', width=15)
    audio_dropdown.pack(side='left')

    # Row 3: Buttons
    row3 = tk.Frame(root)
    row3.pack(pady=(15, 5))

    tk.Button(row3, text="Fetch Options", command=fetch_options).pack(side='left', padx=10)
    tk.Button(row3, text="Download Video", command=lambda: threaded_download("video", root)).pack(side='left', padx=5)
    tk.Button(row3, text="Download Audio", command=lambda: threaded_download("audio", root)).pack(side='left', padx=5)
    tk.Button(row3, text="Download Full", command=lambda: threaded_download("full", root)).pack(side='left', padx=5)

    # Progress Bar and Labels
    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(root, orient='horizontal', length=500, mode='determinate', variable=progress_var)
    progress_bar.pack(pady=(10, 0))

    progress_label = tk.Label(root, text="Progress: 0%")
    progress_label.pack(pady=(20, 0))

    size_label = tk.Label(root, text="Downloaded: 0 B / 0 B")
    size_label.pack(pady=(2, 2))

    merge_label = tk.Label(root, text="...")
    merge_label.pack(pady=(2, 10))

    root.mainloop()


def fetch_options():
    video_url = url_entry.get().strip()
    if not video_url:
        messagebox.showerror("Error", "Please enter a YouTube video URL.")
        return

    try:
        # Resolutions
        resolutions = fetch_resolutions(video_url)
        available_resolutions.clear()
        available_resolutions.extend(resolutions)
        resolution_dropdown['values'] = available_resolutions
        selected_resolution.set(available_resolutions[0])
        resolution_dropdown.config(state='readonly')

        # Audio qualities
        audio_qualities = fetch_audio_qualities(video_url)
        available_audio_qualities.clear()
        available_audio_qualities.extend(audio_qualities)
        audio_dropdown['values'] = available_audio_qualities
        selected_audio_quality.set(available_audio_qualities[0])
        audio_dropdown.config(state='readonly')

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch video/audio info:\n{e}")


def threaded_download(mode: str, root):
    thread = Thread(target=lambda: handle_download(mode, root))
    thread.start()


def handle_download(mode: str, root):
    video_url = url_entry.get().strip()
    resolution = selected_resolution.get()
    audio_quality = selected_audio_quality.get()

    if not video_url:
        root.after(0, lambda: messagebox.showerror("Error", "Please enter a YouTube video URL."))
        return

    if mode in ("video", "full") and not resolution:
        root.after(0, lambda: messagebox.showerror("Error", "Please fetch and select a resolution."))
        return

    if mode in ("audio", "full") and not audio_quality:
        root.after(0, lambda: messagebox.showerror("Error", "Please fetch and select an audio quality."))
        return

    try:
        root.after(0, lambda: progress_var.set(0))
        root.after(0, lambda: progress_label.config(text="Progress: 0%"))
        root.after(0, lambda: size_label.config(text="Downloaded: 0 B / 0 B"))
        root.after(0, lambda: merge_label.config(text=""))
        root.after(0, root.update_idletasks)

        tracker = ProgressTracker(progress_var, progress_label, size_label)

        if mode == "video":
            download_video(video_url, resolution, tracker, root)
        elif mode == "audio":
            download_audio(video_url, tracker, abr=audio_quality, root=root)
        elif mode == "full":
            download_video_audio(video_url, resolution, tracker, merge_label, root)

    except Exception as e:
        root.after(0, lambda: messagebox.showerror("Error", f"An error occurred:\n{e}"))
