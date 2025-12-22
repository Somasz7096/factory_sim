import time
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QSize
from PyQt6.QtGui import QColor, QAction, QIcon
from PyQt6.QtWidgets import (QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton, QLineEdit,
                             QGridLayout,
                             QComboBox, QTabWidget, QGraphicsEffect, QToolBar, QSplitter)

from .custom_widgets import LabeledInput


class Materials_ui(QWidget):
    save_signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.initUI()
        self.new_item = None



    def initUI(self):

        # # główna ramka
        top_frame = QFrame()
        top_frame.setFixedHeight(32)
        top_frame.setFrameShape(QFrame.Shape.StyledPanel)
        top_frame.setStyleSheet("background-color: white;")

        self.left_frame = QFrame()
        self.left_frame.setMaximumWidth(600)
        self.left_frame.setMinimumWidth(200)
        self.left_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.left_frame.setStyleSheet("background-color: white;")

        right_frame = QFrame()
        right_frame.setFrameShape(QFrame.Shape.StyledPanel)
        right_frame.setStyleSheet("background-color: white;")


        # layout ramki głównej
        full_box = QVBoxLayout()
        full_box.setContentsMargins(5, 18, 5, 0)
        full_box.setSpacing(5)
        self.setLayout(full_box)

        full_box.addWidget(top_frame)


        top_box = QHBoxLayout(top_frame)
        top_box.setContentsMargins(0, 0, 0, 0)

        self.left_box = QVBoxLayout(self.left_frame)
        self.left_box.setContentsMargins(5, 5, 5, 5)
        self.left_box.setSpacing(5)
        self.left_frame.setHidden(True)

        right_box = QVBoxLayout(right_frame)
        right_box.addWidget(QLabel("big AF placeholder"))
        right_box.addStretch()

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.left_frame)
        splitter.addWidget(right_frame)
        splitter.setSizes([200, 500])
        splitter.setChildrenCollapsible(False) #blokuje możliwość schowania widgetu

        full_box.addWidget(splitter)



        # ------------ TOOLBAR -----------------------#
        top_toolbar = QToolBar("Top toolbar")
        top_box.addWidget(top_toolbar)
        top_toolbar.setIconSize(QSize(16, 16))
        top_toolbar.setMovable(False)
        top_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)


        # *--------------* TOOLBAR PLACEHOLDERS *------------*

        button_action = QAction(QIcon("gui/icons/plus.png"), "new button", self)
        button_action.setStatusTip("This is target button")
        button_action.triggered.connect(self.add_new)
        top_toolbar.addAction(button_action)

        top_toolbar.addSeparator()

        button_action2 = QAction(QIcon("gui/icons/globe.png"), "Globe button", self)
        button_action2.setCheckable(True)
        button_action2.setStatusTip("This is globe button")
        top_toolbar.addAction(button_action2)

        # *--------------* TOOLBAR PLACEHOLDERS *------------*


    def add_new(self):
        pass
        try:
            self.new_item = NewItem(self.save_signal)
            self.left_box.addWidget(self.new_item)
            self.left_frame.show()
        except Exception as e:
            print(e)

class NewItem(QWidget):
    def __init__(self, save_signal):
        super().__init__()
        self.save_signal = save_signal

        self.data = {}
        self.inputs = []
        try:
            layout = QVBoxLayout()
            self.setLayout(layout)
            header_label = QLabel("Add new item:")
            layout.addWidget(header_label)
            self.id_input = LabeledInput("material_id", input_name="id_input", max_length=16, digits_only=True,
                                         placeholder="ID - opcjonalnie")
            self.inputs.append(self.id_input)
            layout.addWidget(self.id_input)

            options = ("1000",
                       "1100",
                       "1200",
                       "1300",
                       )
            self.warehouse_input = LabeledInput("warehouse", input_type="combo_box", combo_box_options=options,
                                                input_name="warehouse_input", placeholder=" ")
            self.inputs.append(self.warehouse_input)
            layout.addWidget(self.warehouse_input)

            self.name_input = LabeledInput("name", input_name="name_input", max_length=16, placeholder="Nazwa")
            self.inputs.append(self.name_input)
            layout.addWidget(self.name_input)

            self.details_input = LabeledInput("details", input_name="details_input", max_length=16, placeholder="Szczegóły")
            self.inputs.append(self.details_input)
            layout.addWidget(self.details_input)

            self.supplier_input = LabeledInput("supplier", input_name="supplier_input", max_length=16, digits_only=True,
                                               placeholder="ID dostawcy")
            self.inputs.append(self.supplier_input)
            layout.addWidget(self.supplier_input)

            # ---------> Cancel / Save buttons <-----------------#

            buttons_layout = QHBoxLayout()
            buttons_layout.setContentsMargins(5, 5, 5, 5)
            buttons_layout.setSpacing(10)
            cancel_button = QPushButton("Cancel")
            save_button = QPushButton("Save")
            save_button.setDefault(True)
            buttons_layout.addWidget(cancel_button)
            buttons_layout.addWidget(save_button)
            layout.addLayout(buttons_layout)
            buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

            save_button.clicked.connect(self._save)
            cancel_button.clicked.connect(self.deleteLater)

            # ----------> Feedback label <-----------------#
            self.feedback_label = QLabel()
            self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.feedback_label)
            layout.addStretch()
        except Exception as e:
            print(e)

    def _save(self):
        if not self._validate_inputs():
            return
        self.data = {}  # czyszczenie z nieaktualnych danych
        for i in self.inputs:
            self.data[str(i)] = i.text()

        self.save_signal.emit(self.data)

    def _validate_inputs(self):
        for i in self.inputs:
            if i == self.id_input:
                continue
            elif not i.text() or i.text().isspace():
                self._display_error(i)
                self.data = {}
                return False
        return True

    def _display_error(self, i: LabeledInput):
        i.focus()
        self.feedback_label.setText(f"{i} cannot be blank")

    def display_confirmation(self, data):
        message = "New material added:\n\n"
        for key, value in data.items():
            message += f"{key}: {value}\n"
        self.feedback_label.setText(message)

        for i in self.inputs:
            i.setText("")
