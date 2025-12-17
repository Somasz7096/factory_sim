import time
from PyQt6.QtCore import Qt, pyqtSignal, QObject
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton, QLineEdit, QGridLayout,
                             QComboBox, QTabWidget, QGraphicsEffect)

from .custom_widgets import LabeledInput
from database_folder.models import Materials
import asyncio





class NewItemUI(QWidget):

    save_signal = pyqtSignal(list)


    def __init__(self):
        super().__init__()
        self.combined_data = []
        self.data = {}
        self.inputs = []
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

        self.id_input = LabeledInput("material_id", input_name="id_input", max_length=16, digits_only=True,
                                     placeholder="ID - opcjonalnie")
        self.inputs.append(self.id_input)
        left_box.addWidget(self.id_input)

        options = ("1000",
                   "1100",
                   "1200",
                   "1300",
                   )
        self.warehouse_input = LabeledInput("warehouse",input_type="combo_box",combo_box_options=options, input_name="warehouse_input", placeholder=" ")
        self.inputs.append(self.warehouse_input)
        left_box.addWidget(self.warehouse_input)

        self.name_input = LabeledInput("name", input_name="name_input", max_length=16, placeholder="Nazwa")
        self.inputs.append(self.name_input)
        left_box.addWidget(self.name_input)

        self.details_input = LabeledInput("details", input_name="details_input", max_length=16, placeholder="Szczegóły")
        self.inputs.append(self.details_input)
        left_box.addWidget(self.details_input)

        self.supplier_input = LabeledInput("supplier", input_name="supplier_input", max_length=16, digits_only=True,
                                placeholder="ID dostawcy")
        self.inputs.append(self.supplier_input)
        left_box.addWidget(self.supplier_input)

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

        save_button.clicked.connect(self._save)
        cancel_button.clicked.connect(self.deleteLater)

        #----------> Error label <-----------------#
        self.error_label = QLabel()
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        left_box.addWidget(self.error_label)
        left_box.addStretch()

        right_box = QVBoxLayout(right_frame)
        full_box.addLayout(right_box)
        right_box.addWidget(QLabel("big AF placeholder"))
        right_box.addStretch()

        full_box.setStretch(0,1)
        full_box.setStretch(1,4)


    def _save(self):
        if not self._validate_inputs():
            return
        for i in self.inputs:
            self.data[str(i)] = i.text()


        self.combined_data.append(Materials)
        self.combined_data.append(self.data)
        self.save_signal.emit(self.combined_data)

    def _validate_inputs(self):
        for i in self.inputs:
            if i == self.id_input:
                continue
            elif not i.text() or i.text().isspace():
                self._display_error(i)
                self.combined_data = []
                return False
        return True

    def _display_error(self, i: LabeledInput):
        self.error_label.setText(f"{i} cannot be blank")
        i.focus()
        print(f"empty input for {i}")
        time.sleep(1)
        self.error_label.setText("")









