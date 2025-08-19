from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer
from PIL import Image, ImageQt

class GifLabel(QLabel):
    def __init__(self, gif_path, parent=None):
        super().__init__(parent)
        self.gif = Image.open(gif_path)   # Load GIF with Pillow
        self.frames = []
        self.durations = []

        try:
            while True:
                frame = self.gif.copy().convert("RGBA")
                self.frames.append(ImageQt.ImageQt(frame))  # Convert to Qt format
                self.durations.append(self.gif.info.get("duration", 100))  # Frame delay
                self.gif.seek(self.gif.tell() + 1)
        except EOFError:
            pass

        self.current_frame = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(self.durations[0])  # Start with first frame’s duration

        self.setPixmap(QPixmap.fromImage(self.frames[0]))

    def next_frame(self):
        self.current_frame = (self.current_frame + 1) % len(self.frames)
        self.setPixmap(QPixmap.fromImage(self.frames[self.current_frame]))
        self.timer.start(self.durations[self.current_frame])  # Use correct delay
