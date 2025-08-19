import random
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtGui import QMovie, QMouseEvent
from PyQt6.QtCore import Qt, QTimer, QPoint, QSize
from queue import Empty

from gif_label import GifLabel
from prompt_window import PromptWindow, ResponseBubble

class DeskoraEntity(QWidget):
    def __init__(self, prompt_queue, response_queue):
        super().__init__()
        self.prompt_queue = prompt_queue
        self.response_queue = response_queue

        # --- Window Properties ---
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)


        # Label for the animated GIF
        # self.entity_label = QLabel(self)
        # self.movie = QMovie("entity2.gif")
        # self.entity_label.setMovie(self.movie)
        # self.movie.start()
        # print("DEBUG ",self.movie.isValid())

        self.entity_label = GifLabel("entity.gif", self)

        # Initial size based on the GIF
        frame_size = self.entity_label.frames[0].size()  # QSize from first frame
        self.initial_size = QSize(frame_size.width(), frame_size.height())
        self.setGeometry(100, 100, self.initial_size.width(), self.initial_size.height())

        # Random Movement Logic
        self.movement_timer = QTimer(self)
        self.movement_timer.timeout.connect(self.update_behavior)
        self.movement_timer.start(1000)

        self.is_moving = False
        self.direction = 1
        self.speed = 2
        self.steps_left = 0
        self.old_pos = QPoint()

        # Prompt & Response UI
        self.prompt_window = PromptWindow()
        self.prompt_window.prompt_submitted.connect(self.handle_prompt)
        self.response_bubble = ResponseBubble()
        self.response_bubble.setFixedWidth(200)

        # Check for backend responses
        self.response_check_timer = QTimer(self)
        self.response_check_timer.timeout.connect(self.check_for_response)
        self.response_check_timer.start(100)

        self.response_timer = QTimer(self)
        self.response_timer.setSingleShot(True)
        self.response_timer.timeout.connect(self.response_bubble.hide)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()
        elif event.button() == Qt.MouseButton.RightButton:
            self.open_prompt_window()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def open_prompt_window(self):
        if not self.prompt_window.isVisible():
            entity_geometry = self.geometry()
            prompt_x = entity_geometry.x() + (entity_geometry.width() - self.prompt_window.width()) // 2
            prompt_y = entity_geometry.y() - self.prompt_window.height() - 10
            self.prompt_window.move(prompt_x, prompt_y)
            self.prompt_window.show()
            self.prompt_window.activateWindow()

    def handle_prompt(self, prompt):
        print(f"Main process received prompt: '{prompt}'")

        self.prompt_queue.put(prompt)
        self.prompt_window.close()

    def check_for_response(self):
        try:
            while True:
                response = self.response_queue.get_nowait()
                print(f"Main process received response: '{response}'")
                if response == "__SHUTDOWN__":
                    print("Shutting down Deskora GUI...")
                    QApplication.quit()  # Closes the application
                    return
                self.show_response(response)
        except Empty:
            pass

    def show_response(self, response: str):
        self.response_bubble.setText(response)
        self.response_bubble.adjustSize()
        entity_global_pos = self.mapToGlobal(QPoint(0, 0))
        bubble_x = entity_global_pos.x() + (self.width() - self.response_bubble.width()) // 2
        bubble_y = entity_global_pos.y() - self.response_bubble.height() - 10
        self.response_bubble.move(bubble_x, bubble_y)
        self.response_bubble.show()
        self.response_timer.start(5000)

    def update_behavior(self):
        if self.is_moving:
            self.move_entity()
        else:
            if random.random() < 0.3:
                self.start_new_movement()

    def start_new_movement(self):
        self.is_moving = True
        self.direction = random.choice([-1, 1])
        self.steps_left = random.randint(50, 200)

    def move_entity(self):
        if self.steps_left > 0:
            screen_rect = QApplication.primaryScreen().geometry()
            new_x = self.x() + self.direction * self.speed

            if new_x <= 0:
                self.direction = 1
            elif new_x + self.width() >= screen_rect.width():
                self.direction = -1

            self.move(new_x, self.y())
            self.steps_left -= 1
        else:
            self.is_moving = False

    def closeEvent(self, event):
        self.prompt_queue.put(None)
        event.accept()
