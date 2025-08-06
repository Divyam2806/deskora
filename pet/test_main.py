# main_cli.py

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QPoint, QSize, QTimer

from prompt_window import ResponseBubble


class DeskoraEntity(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.entity_label = QLabel(self)
        self.movie = QMovie("entity.gif")
        self.entity_label.setMovie(self.movie)
        self.movie.start()

        movie_size = self.movie.currentImage().size()
        self.setGeometry(100, 100, movie_size.width(), movie_size.height())

        self.old_pos = QPoint()

        self.response_bubble = ResponseBubble(self)
        self.response_bubble.setFixedWidth(200)

        QTimer.singleShot(2000, self.test_show_bubble)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def test_show_bubble(self):
        print("Attempting to show response bubble...")
        response = "Hello from the test bubble!"

        # Prepare text and size first
        self.response_bubble.setText(response)
        self.response_bubble.adjustSize()

        # Get global position of the entity window
        entity_global_pos = self.mapToGlobal(QPoint(0, 0))

        # Calculate position ABOVE the entity, centered horizontally
        bubble_x = entity_global_pos.x() + (self.width() - self.response_bubble.width()) // 2
        bubble_y = entity_global_pos.y() - self.response_bubble.height() - 10

        print(f"Entity global pos: {entity_global_pos}")
        print(f"Bubble position: {bubble_x}, {bubble_y}")

        self.response_bubble.move(bubble_x, bubble_y)
        self.response_bubble.show_response(response, duration=3000)

        print("Bubble should be on screen now.")

        QTimer.singleShot(5000, self.response_bubble.hide)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    entity_window = DeskoraEntity()
    entity_window.show()
    sys.exit(app.exec())