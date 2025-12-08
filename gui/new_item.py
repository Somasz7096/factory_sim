from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton, QLineEdit, QGridLayout
from .custom_widgets import LabeledInput




class NewItem(QWidget):
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



        left_box = QGridLayout()
        left_box.setContentsMargins(5, 5, 5, 5)
        left_box.setSpacing(5)

        full_box.addLayout(left_box)



        header_label = QLabel("Add new item:")
        left_box.addWidget(header_label, 0, 0)


        left_box.addWidget(QLabel("Item name:"), 1,0)
        name_input = QLineEdit(self)
        name_input.setMinimumWidth(50)
        name_input.setMaximumWidth(450)
        left_box.addWidget(name_input, 1,1)

        left_box.addWidget(QLabel("Item type:"), 2,0)
        type_input = QLineEdit(self)
        left_box.addWidget(type_input, 2,1)

        left_box.addWidget(QLabel("Item price:"), 3,0)
        price_input = QLineEdit(self)
        left_box.addWidget(price_input, 3,1)

        left_box.addWidget(QLabel("Item origins:"), 4,0)
        origins_input = QLineEdit(self)
        left_box.addWidget(origins_input, 4,1)

        left_box.setColumnMinimumWidth(1, 50)
        left_box.setColumnStretch(0,0)
        left_box.setColumnStretch(1,0)

        labeled_input = LabeledInput("labeled input", label_name="labeled_input", min_w=50, max_w=250, max_length=16)
        left_box.addWidget(labeled_input,5,1)


        right_box = QVBoxLayout()
        full_box.addLayout(right_box)
        right_box.addWidget(QLabel("big AF placeholder"))
        full_box.addStretch()













