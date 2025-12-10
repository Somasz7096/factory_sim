from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton, QLineEdit, QGridLayout
from .custom_widgets import LabeledInput





class NewItemUI(QWidget):

    testsignal = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        # # główna ramka
        left_frame = QFrame()
        left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        left_frame.setStyleSheet("background-color: white;")

        right_frame = QFrame()
        right_frame.setFrameShape(QFrame.Shape.StyledPanel)
        right_frame.setStyleSheet("background-color: white;")


        # layout ramki głównej
        full_box = QHBoxLayout()
        full_box.setContentsMargins(5, 18, 5, 0)
        full_box.setSpacing(5)
        self.setLayout(full_box)
        full_box.addWidget(left_frame)
        full_box.addWidget(right_frame)



        left_box = QVBoxLayout(left_frame)
        left_box.setContentsMargins(5, 5, 5, 5)
        left_box.setSpacing(5)

        full_box.addLayout(left_box)



        header_label = QLabel("Add new item:")
        left_box.addWidget(header_label)

        id_input = LabeledInput("Item ID", input_name="id_input", max_length=16, digits_only=True, placeholder="ID - opcjonalnie")
        left_box.addWidget(id_input)

        name_input = LabeledInput("Item name", input_name="name_input", max_length=16, placeholder="Nazwa")
        left_box.addWidget(name_input)

        details_input = LabeledInput("Item details", input_name="detail_input", max_length=16, placeholder="Szczegóły")
        left_box.addWidget(details_input)


        options = ("1000 - surowce",
                   "1100 - nośniki",
                   "1200 - opakowania",
                   "1300 - półwyroby",
                   )
        type_input = LabeledInput("Item type",input_type="combo_box",combo_box_options=options, input_name="type_input", placeholder=" ")
        left_box.addWidget(type_input)


        supplier_input = LabeledInput("Supplier ID", input_name="supplier_input", max_length=16, digits_only=True,
                                placeholder="ID dostawcy")
        left_box.addWidget(supplier_input)

        #---------> Cancel / Save buttons <-----------------#

        buttons_layout = QHBoxLayout()
        buttons_layout.setContentsMargins(5, 5, 5, 5)
        buttons_layout.setSpacing(10)
        cancel_button = QPushButton("Cancel")
        save_button = QPushButton("Save")
        save_button.setDefault(True)
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(save_button)
        left_box.addLayout(buttons_layout)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        save_button.clicked.connect(self.test_signal_func)
        cancel_button.clicked.connect(self.deleteLater)

        #----------> Error label <-----------------#
        error_label = QLabel()
        error_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        left_box.addWidget(error_label)
        left_box.addStretch()

        right_box = QVBoxLayout(right_frame)
        full_box.addLayout(right_box)
        right_box.addWidget(QLabel("big AF placeholder"))
        right_box.addStretch()

        full_box.setStretch(0,1)
        full_box.setStretch(1,4)


    def test_signal_func(self):
        print("button clicked")
        self.testsignal.emit()














