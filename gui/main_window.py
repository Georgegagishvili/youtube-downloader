import threading
import requests
import ttkbootstrap as ttk

from io import BytesIO
from typing import Optional
from pytubefix import YouTube
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog

from core import (
    download_video_audio,
    download_video,
    download_audio,
    ProgressTracker,
    fetch_resolutions,
    fetch_audio_qualities,
)
from .widgets import URLInputFrame, OptionsFrame, ButtonsFrame, ProgressFrame, DownloadPathFrame


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")

        self.title("YouTube Downloader")

        window_width = 800
        window_height = 360

        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)

        # Center window
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2) - 50  # Move up a bit
        self.geometry(f"+{x}+{y}")

        self.yt: Optional[YouTube] = None
        self.selected_resolution = ttk.StringVar()
        self.selected_audio_quality = ttk.StringVar()
        self.progress_var = ttk.IntVar()

        self._create_widgets()
        self._collect_interactive_widgets()

    def _create_widgets(self):
        # Create frames
        self.url_frame = URLInputFrame(self)
        
        self.download_path_frame = DownloadPathFrame(self)
        self.download_path_frame.browse_button.config(command=self._choose_download_path)

        details_frame = ttk.Frame(self)
        details_frame.pack(pady=5, padx=10, fill=ttk.X)
        details_frame.columnconfigure(0, weight=1)

        self.options_frame = OptionsFrame(details_frame, self.selected_resolution, self.selected_audio_quality)
        self.options_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.buttons_frame = ButtonsFrame(
            details_frame,
            self.fetch_options,
            lambda: self.threaded_download("video"),
            lambda: self.threaded_download("audio"),
            lambda: self.threaded_download("full")
        )
        self.buttons_frame.grid(row=1, column=0, sticky="ew")

        # Blank image as a placeholder to prevent UI displacement
        placeholder_img = Image.new('RGB', (240, 135), color='#ECECEC')
        self.placeholder_photo = ImageTk.PhotoImage(placeholder_img)
        self.thumbnail_label = ttk.Label(
            details_frame,
            image=self.placeholder_photo,
            text="Image Preview",
            compound="center",
            foreground="black"
        )
        self.thumbnail_label.grid(row=0, column=1, rowspan=2, padx=(20, 0), sticky="ne")

        self.progress_frame = ProgressFrame(self, self.progress_var)

    def _collect_interactive_widgets(self):
        self.interactive_widgets = [
            self.url_frame.url_entry,
            self.download_path_frame.browse_button,
            self.options_frame.resolution_dropdown,
            self.options_frame.audio_dropdown,
            self.buttons_frame.fetch_button,
            self.buttons_frame.download_video_button,
            self.buttons_frame.download_audio_button,
            self.buttons_frame.download_full_button,
        ]

    def _toggle_widgets_state(self, state="normal"):
        for widget in self.interactive_widgets:
            if isinstance(widget, ttk.Combobox):
                widget.config(state="readonly" if state == "normal" and widget['values'] else "disabled")
            else:
                widget.config(state=state)

    def _choose_download_path(self):
        path = filedialog.askdirectory(title="Select Download Folder")
        if path:
            self.download_path_frame.path_var.set(path)

    def fetch_options(self):
        video_url = self.url_frame.url_entry.get().strip()
        if not video_url:
            messagebox.showerror("Error", "Please enter a YouTube video URL.")
            return

        self.buttons_frame.fetch_button.config(state="disabled")
        thread = threading.Thread(target=self._fetch_data_in_thread, args=(video_url,))
        thread.start()

    def _fetch_data_in_thread(self, video_url):
        try:
            from core.downloader import get_yt_instance
            self.yt = get_yt_instance(video_url)

            # Fetch data
            resolutions = fetch_resolutions(self.yt)
            audio_qualities = fetch_audio_qualities(self.yt)
            thumbnail_url = self.yt.thumbnail_url

            # Fetch thumbnail image
            response = requests.get(thumbnail_url)
            img_data = response.content

            # Schedule UI updates on the main thread
            self.after(0, self._update_ui_with_fetched_data, resolutions, audio_qualities, img_data)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"Failed to fetch video/audio info:\n{e}"))
        finally:
            self.after(0, lambda: self.buttons_frame.fetch_button.config(state="normal"))

    def _update_ui_with_fetched_data(self, resolutions, audio_qualities, img_data):
        # Update thumbnail
        img = Image.open(BytesIO(img_data))
        img.thumbnail((240, 135))
        photo_image = ImageTk.PhotoImage(img)
        self.thumbnail_label.config(image=photo_image, text="")
        self.thumbnail_label.image = photo_image

        # Update resolution dropdown
        self.options_frame.resolution_dropdown["values"] = resolutions
        self.selected_resolution.set(resolutions[0])
        self.options_frame.resolution_dropdown.config(state="readonly")

        # Update audio quality dropdown
        self.options_frame.audio_dropdown["values"] = audio_qualities
        self.selected_audio_quality.set(audio_qualities[0])
        self.options_frame.audio_dropdown.config(state="readonly")

    def threaded_download(self, mode: str):
        thread = threading.Thread(target=lambda: self.handle_download(mode))
        thread.start()

    def handle_download(self, mode: str):
        video_url = self.url_frame.url_entry.get().strip()
        resolution = self.selected_resolution.get()
        audio_quality = self.selected_audio_quality.get()
        output_path = self.download_path_frame.path_var.get()

        if not video_url or not self.yt:
            self.after(0, lambda: messagebox.showerror("Error", "Please fetch video details first."))
            return

        if mode in ("video", "full") and not resolution:
            self.after(0, lambda: messagebox.showerror("Error", "Please fetch and select a resolution."))
            return

        if mode in ("audio", "full") and not audio_quality:
            self.after(0, lambda: messagebox.showerror("Error", "Please fetch and select an audio quality."))
            return

        self._toggle_widgets_state("disabled")
        try:
            self.after(0, lambda: self.progress_var.set(0))
            self.after(0, lambda: self.progress_frame.progress_label.config(text="Progress: 0%"))
            self.after(0, lambda: self.progress_frame.size_label.config(text="Downloaded: 0 B / 0 B"))
            self.after(0, lambda: self.progress_frame.merge_label.config(text=""))
            self.after(0, self.update_idletasks)

            tracker = ProgressTracker(
                self.progress_var, self.progress_frame.progress_label, self.progress_frame.size_label, self
            )

            if mode == "video":
                download_video(self.yt, resolution, tracker, self, output_path=output_path)
            elif mode == "audio":
                download_audio(self.yt, tracker, abr=audio_quality, root=self, output_path=output_path)
            elif mode == "full":
                download_video_audio(self.yt, resolution, tracker, self.progress_frame.merge_label, self,
                                     output_path=output_path)

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error", f"An error occurred:\n{e}"))
        finally:
            self._toggle_widgets_state("normal")
