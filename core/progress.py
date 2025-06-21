from .utils import format_bytes


class ProgressTracker:
    def __init__(self, progress_var, progress_label, size_label, root):
        self.progress_var = progress_var
        self.progress_label = progress_label
        self.size_label = size_label
        self.root = root
        self.animation_job = None
        self.target_percent = 0

    def update(self, downloaded, total):
        if total > 0:
            self.target_percent = int(downloaded / total * 100)
            if self.animation_job is None:
                self._animate_progress()

            self.progress_label.config(text=f"Progress: {self.target_percent}%")
            self.size_label.config(text=f"Downloaded: {format_bytes(downloaded)} / {format_bytes(total)}")
        else:
            self.target_percent = 0
            self.progress_var.set(0)
            self.progress_label.config(text="Progress: 0%")
            self.size_label.config(text="Downloaded: 0 B / 0 B")

        self.progress_label.master.update_idletasks()

    def _animate_progress(self):
        current_percent = self.progress_var.get()
        if current_percent < self.target_percent:
            self.progress_var.set(current_percent + 1)
            self.animation_job = self.root.after(10, self._animate_progress)
        elif current_percent > self.target_percent:
            self.progress_var.set(self.target_percent)
            self.animation_job = None
        else:
            self.animation_job = None
