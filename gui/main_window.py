import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

from core import fetch_resolutions, download_video_audio
from core import ProgressTracker

available_resolutions: list[str] = []
selected_resolution: Optional[tk.StringVar] = None

progress_var: Optional[tk.IntVar] = None
progress_label: Optional[tk.Label] = None
size_label: Optional[tk.Label] = None
merge_label: Optional[tk.Label] = None
url_entry: Optional[tk.Entry] = None
resolution_dropdown: Optional[ttk.Combobox] = None


def create_main_window():
    global selected_resolution, progress_var, progress_label, size_label, merge_label
    global url_entry, resolution_dropdown

    root = tk.Tk()
    root.title("YouTube Video & Audio Downloader")
    root.geometry("520x280")

    selected_resolution = tk.StringVar()

    tk.Label(root, text="YouTube Video URL:").pack(pady=(10, 0))
    url_entry = tk.Entry(root, width=60)
    url_entry.pack(pady=(0, 5))

    fetch_button = tk.Button(root, text="Fetch Resolutions", command=lambda: fetch_click())
    fetch_button.pack()

    tk.Label(root, text="Select Resolution:").pack(pady=(5, 0))
    resolution_dropdown = ttk.Combobox(root, textvariable=selected_resolution, state='disabled', width=20)
    resolution_dropdown.pack(pady=(0, 10))

    download_btn = tk.Button(root, text="Download", command=lambda: download_click(root))
    download_btn.pack(pady=5)

    progress_var = tk.IntVar()
    progress_bar = ttk.Progressbar(
        root, orient='horizontal', length=450, mode='determinate', variable=progress_var
    )
    progress_bar.pack(pady=(5, 0))

    progress_label = tk.Label(root, text="Progress: 0%")
    progress_label.pack(pady=(2, 0))

    size_label = tk.Label(root, text="Downloaded: 0 B / 0 B")
    size_label.pack(pady=(2, 2))

    merge_label = tk.Label(root, text="")
    merge_label.pack(pady=(2, 10))

    root.mainloop()


def fetch_click():
    video_url = url_entry.get()
    if not video_url.strip():
        messagebox.showerror("Error", "Please enter a YouTube video URL.")
        return

    try:
        resolutions = fetch_resolutions(video_url)
        available_resolutions.clear()
        available_resolutions.extend(resolutions)

        resolution_dropdown['values'] = available_resolutions
        selected_resolution.set(available_resolutions[0])
        resolution_dropdown.config(state='readonly')

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch resolutions:\n{e}")


def download_click(root):
    video_url = url_entry.get()
    resolution = selected_resolution.get()

    if not video_url.strip():
        messagebox.showerror("Error", "Please enter a YouTube video URL.")
        return

    if not resolution:
        messagebox.showerror("Error", "Please fetch and select a resolution first.")
        return

    try:
        progress_var.set(0)
        progress_label.config(text="Progress: 0%")
        size_label.config(text="Downloaded: 0 B / 0 B")
        merge_label.config(text="")
        root.update_idletasks()

        tracker = ProgressTracker(progress_var, progress_label, size_label)
        download_video_audio(video_url, resolution, tracker, merge_label, root)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")
