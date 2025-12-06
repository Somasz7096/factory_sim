from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal, QTimer
from PyQt6.QtWidgets import (QPushButton, QLabel, QWidget, QProgressBar, QLineEdit,
                             QFrame, QHBoxLayout, QMainWindow, QApplication, QVBoxLayout,
                             QPlainTextEdit, QSpinBox)

class Orders(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.initUI()

    def initUI(self):

        # główna ramka
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet("background-color: white;")

        # dwie osobne ramki w środku
        frame2 = QFrame()
        frame2.setStyleSheet("background-color: #f0f0f0;")

        frame3 = QFrame()
        frame3.setStyleSheet("background-color: #e0e0e0;")

        # layout okna
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(frame)

        # layout ramki głównej
        full_box = QHBoxLayout(frame)
        full_box.addWidget(frame2)
        full_box.addWidget(frame3)

        # layouty wewnątrz paneli
        label_box = QVBoxLayout(frame2)
        button_box = QVBoxLayout(frame3)
        full_box.addStretch()



        for r in range(10):
            label = QLabel(f"Label {r}")
            label_box.addWidget(label)

        for r in range(10):
            button = QPushButton(f"Button {r}")
            button.clicked.connect(lambda: self.close())
            button_box.addWidget(button)

        label_box.addStretch()
        button_box.addStretch()

