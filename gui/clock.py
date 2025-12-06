from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal, QTimer
from PyQt6.QtWidgets import (QPushButton, QLabel, QWidget, QProgressBar, QLineEdit,
                             QFrame, QHBoxLayout, QMainWindow, QApplication, QVBoxLayout,
                             QPlainTextEdit, QSpinBox)
import modules.clock



class Clock(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.initUI()


    def initUI(self):
        line = QFrame()

        # Time Layout#
        self.setWindowTitle("Timer settings")
        time_layout = QVBoxLayout()

        self.startBtn = QPushButton("Start timer")
        self.startBtn.clicked.connect(modules.clock.test)
        time_layout.addWidget(self.startBtn)

        self.pauseBtn = QPushButton("Pause")
        # self.pauseBtn.clicked.connect(self.pause)
        time_layout.addWidget(self.pauseBtn)

        self.stopBtn = QPushButton("Stop")
        # self.stopBtn.clicked.connect(self.stop)
        self.stopBtn.clicked.connect(self.deleteLater)
        time_layout.addWidget(self.stopBtn)

        time_layout.addWidget(line)


        self.speed_value_input = QLineEdit()
        self.speed_value_input.setPlaceholderText("Enter time multiplier...")
        time_layout.addWidget(self.speed_value_input)

        self.set_multiplierBtn = QPushButton("Set multiplier")
        # self.set_multiplierBtn.clicked.connect(self.speed_multiplier)
        time_layout.addWidget(self.set_multiplierBtn)

        # self.multiplier_label = QLabel(str(multiplier_value))
        # time_layout.addWidget(self.multiplier_label)

        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 60)
        self.progressBar.setTextVisible(False)
        time_layout.addWidget(self.progressBar)

        self.setLayout(time_layout)

        # self.destroyed.connect(lambda: print("destroyed"))


