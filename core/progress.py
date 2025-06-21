from core import format_bytes


class ProgressTracker:
    def __init__(self, progress_var, progress_label, size_label):
        self.progress_var = progress_var
        self.progress_label = progress_label
        self.size_label = size_label

    def update(self, downloaded, total):
        percentage = int(downloaded / total * 100)
        self.progress_var.set(percentage)
        self.progress_label.config(text=f"Progress: {percentage}%")
        self.size_label.config(
            text=f"Downloaded: {format_bytes(downloaded)} / {format_bytes(total)}"
        )
        self.progress_label.update()
        self.size_label.update()
