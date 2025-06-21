# YouTube Downloader

An easy-to-use desktop application for downloading YouTube videos and audio.
Built with Python and `ttkbootstrap`, this tool provides a simple graphical interface to download videos in various formats and qualities.

![App Image](https://i.imgur.com/C0Mcwmv.png)

## Features

- **Download Modes**: Choose between downloading video-only, audio-only, or a complete video with merged audio.
- **Quality Selection**:
  - Automatically fetches available video resolutions (e.g., 1080p, 720p).
  - Automatically fetches available audio qualities (e.g., 128kbps).
- **Custom Download Path**: A "Browse" button allows you to select any folder on your computer to save your downloads.
- **Real-time Progress**: A progress bar and text labels provide instant feedback on download speed, size, and status.

## Download

For a simple, one-click experience, you can download the latest pre-compiled executable for your operating system
from the **[releases](https://github.com/Georgegagishvili/youtube-downloader/releases)** page.

## Getting Started

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Georgegagishvili/youtube-downloader
    cd youtube-downloader
    ```

2.  **Install the required Python packages:**
    A `requirements.txt` file is provided to easily install all necessary dependencies.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the application, execute the `app.py` script from the root directory of the project:

```bash
python app.py
```

## Project Structure

```
ytdowner/
├── app.py                  # Main application entry point
├── requirements.txt        # Project dependencies
├── assets/
│   └── yt.ico              # Application icon
├── core/
│   ├── downloader.py       # Handles YouTube video/audio fetching and downloading
│   ├── ffmpeg.py           # Manages video/audio merging with ffmpeg
│   ├── progress.py         # Logic for tracking download progress
│   └── utils.py            # Utility functions (e.g., formatting file sizes)
└── gui/
    ├── main_window.py      # The main application class and window
    └── widgets.py          # Custom ttkbootstrap widgets
```
