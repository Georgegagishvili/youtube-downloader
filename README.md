# YouTube Downloader

A simple Python application to download YouTube videos with a GUI interface.

## Project Structure

```plaintext
assets/
└── yt.ico               # Application icon

core/
├── __init__.py
├── downloader.py        # YouTube video download logic
├── ffmpeg.py            # Video/audio merging utilities using ffmpeg
├── progress.py          # Download progress tracking
└── utils.py             # Helper functions

gui/
├── __init__.py
├── main_window.py       # Main GUI window implementation
└── widgets.py           # (Empty, ToDo) Custom widgets for GUI
```

## Requirements

- Python 3.13
- tkinter
- pytubefix
- imageio_ffmpeg

## Usage

Run the application:

```bash
python app.py
```


## TODO
- Implement custom widgets in gui/widgets.py
- Add more features and improve UI/UX

