import os
import ttkbootstrap as ttk

from ttkbootstrap.constants import *


class URLInputFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(pady=10, padx=10, fill=X)
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="YouTube URL:", width=14, anchor="w").grid(row=0, column=0, padx=(0, 5), sticky="w")
        self.url_entry = ttk.Entry(self)
        self.url_entry.grid(row=0, column=1, sticky="ew")


class OptionsFrame(ttk.Frame):
    def __init__(self, parent, resolution_var, audio_quality_var, **kwargs):
        super().__init__(parent, **kwargs)
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Resolution:", width=14, anchor="w").grid(row=0, column=0, padx=(0, 5), sticky="w",
                                                                       pady=(0, 5))
        self.resolution_dropdown = ttk.Combobox(
            self, textvariable=resolution_var, state="disabled"
        )
        self.resolution_dropdown.grid(row=0, column=1, sticky="ew", pady=(0, 5))

        ttk.Label(self, text="Audio Quality:", width=14, anchor="w").grid(row=1, column=0, padx=(0, 5), sticky="w")
        self.audio_dropdown = ttk.Combobox(
            self, textvariable=audio_quality_var, state="disabled"
        )
        self.audio_dropdown.grid(row=1, column=1, sticky="ew")


class ButtonsFrame(ttk.Frame):
    def __init__(self, parent, fetch_command, download_video_command, download_audio_command, download_full_command,
                 **kwargs):
        super().__init__(parent, **kwargs)
        self.columnconfigure((0, 1), weight=1)

        self.fetch_button = ttk.Button(
            self, text="Show Details", command=fetch_command, bootstyle="primary"
        )
        self.fetch_button.grid(row=0, column=0, sticky="ew", padx=(0, 2), pady=(0, 5))

        self.download_video_button = ttk.Button(
            self, text="Download Video", command=download_video_command, bootstyle="secondary"
        )
        self.download_video_button.grid(row=0, column=1, sticky="ew", padx=(2, 0), pady=(0, 5))

        self.download_full_button = ttk.Button(
            self, text="Download Full", command=download_full_command, bootstyle="secondary"
        )
        self.download_full_button.grid(row=1, column=0, sticky="ew", padx=(0, 2))

        self.download_audio_button = ttk.Button(
            self, text="Download Audio", command=download_audio_command, bootstyle="secondary"
        )
        self.download_audio_button.grid(row=1, column=1, sticky="ew", padx=(2, 0))


class DownloadPathFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(pady=5, padx=10, fill=X)
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Save to:", width=14, anchor="w").grid(row=0, column=0, padx=(0, 5), sticky="w")

        self.path_var = ttk.StringVar(value=os.getcwd())
        self.path_entry = ttk.Entry(self, textvariable=self.path_var, state="readonly")
        self.path_entry.grid(row=0, column=1, sticky="ew", padx=(0, 5))

        self.browse_button = ttk.Button(self, text="Browse...")
        self.browse_button.grid(row=0, column=2)


class ProgressFrame(ttk.Frame):
    def __init__(self, parent, progress_var, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(pady=5, padx=10, fill=X)

        self.progress_bar = ttk.Progressbar(
            self,
            orient="horizontal",
            length=500,
            mode="determinate",
            variable=progress_var,
        )
        self.progress_bar.pack(pady=(10, 0), fill=X)

        self.progress_label = ttk.Label(self, text="Progress: 0%")
        self.progress_label.pack(pady=(10, 0))

        self.size_label = ttk.Label(self, text="Downloaded: 0 B / 0 B")
        self.size_label.pack(pady=2)

        self.merge_label = ttk.Label(self, text="")
        self.merge_label.pack(pady=(2, 10))
