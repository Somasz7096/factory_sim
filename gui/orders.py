from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal, QTimer
from PyQt6.QtWidgets import (QPushButton, QLabel, QWidget, QProgressBar, QLineEdit,
                             QFrame, QHBoxLayout, QMainWindow, QApplication, QVBoxLayout,
                             QPlainTextEdit, QSpinBox)

class Orders(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # główna ramka
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.StyledPanel)
        main_frame.setStyleSheet("background-color: white;")

        # layout okna
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(main_frame)
        main_layout.setContentsMargins(0, 18, 10, 0)
        main_layout.setSpacing(0)

        # layout ramki głównej
        full_box = QHBoxLayout(main_frame)
        full_box.setContentsMargins(0, 0, 0, 0)
        full_box.setSpacing(0)


        left_box = QVBoxLayout()
        left_box.setContentsMargins(0, 0, 0, 0)
        left_box.setSpacing(0)


        right_box = QVBoxLayout()
        full_box.addLayout(left_box)
        full_box.addLayout(right_box)



        for r in range(5):
            row = Row(label=r)
            left_box.addWidget(row)

        left_box.addStretch()
        full_box.addStretch()

class Row(QWidget):
    def __init__(self, label):
        super().__init__()

        # Ramka
        frame2 = QFrame()
        frame2.setFrameShape(QFrame.Shape.StyledPanel)
        frame2.setStyleSheet("background-color: #f0f0f0;")


        # Layout wewnątrz ramki
        inner_layout = QHBoxLayout()
        inner_layout.setSpacing(10)

        frame2.setLayout(inner_layout)

        # Elementy
        label = QLabel(f"{label}")
        text_input = QLineEdit()
        text_input.setObjectName(f"text_input_{label}")
        text_input.setToolTip(f"Text input for {label}")

        button = QPushButton("OK")
        button.setObjectName(f"button_{label}")
        button.setToolTip(f"Button for {label}")

        # Dodajemy elementy do ramki
        inner_layout.addWidget(label)
        inner_layout.addWidget(text_input)
        inner_layout.addWidget(button)

        # Główny layout wiersza
        row_layout = QHBoxLayout(self)
        row_layout.setContentsMargins(5, 5, 0, 0)


        row_layout.addWidget(frame2)

        self.setMaximumSize(300, 70)

