import sys
import time
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QApplication, QLabel
from PyQt6.QtCore import pyqtSignal, Qt, QTimer


class PromptWindow(QWidget):
    # A custom signal to emit when the user submits a prompt
    prompt_submitted = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Prompt Deskora")
        self.setGeometry(300, 300, 400, 100)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.setFixedSize(400, 100)  # Set a fixed size to avoid resizing issues

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Type your prompt here...")
        layout.addWidget(self.prompt_input)

        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.submit_prompt)
        layout.addWidget(self.send_button)

        self.prompt_input.returnPressed.connect(self.send_button.click)



    def submit_prompt(self):
        prompt_text = self.prompt_input.text()
        if prompt_text:
            # We'll emit the signal to send the prompt to the main window
            self.prompt_submitted.emit(prompt_text)
            self.prompt_input.clear()
            self.close()  # Close the window after submitting


class ResponseBubble(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)  # No parent → independent window

        # Make it a floating tooltip-like window
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Bubble style
        self.setStyleSheet("""
            background-color: white; 
            border: 1px solid black; 
            border-radius: 10px; 
            padding: 5px;
        """)
        self.setWordWrap(True)
        self.hide()


    def show_response(self, text, duration=5000):
        self.setText(text)
        self.adjustSize()
        self.show()
        QTimer.singleShot(duration, self.hide)