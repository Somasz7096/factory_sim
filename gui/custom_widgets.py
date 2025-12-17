from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QGridLayout, QComboBox
from PyQt6.QtGui import QIntValidator

class TextInput(QLineEdit):
    def __init__(self,input_name=None, min_w=None, max_w=None, fixed_w=None, placeholder="", digits_only=False, max_length=None):
        super().__init__()
        if input_name:
            self.setObjectName(input_name)

        if fixed_w is not None:
            self.setFixedWidth(fixed_w)
        else:
            if min_w is not None:
                self.setMinimumWidth(min_w)
            if max_w is not None:
                self.setMaximumWidth(max_w)

        if placeholder:
            self.setPlaceholderText(placeholder)

        if max_length is not None:
            self.setMaxLength(max_length)

        if digits_only:
            self.setValidator(QIntValidator())

class ComboBox(QComboBox):
    def __init__(self, input_name=None, min_w=None, max_w=None, fixed_w=None, placeholder=""):
        super().__init__()
        if input_name:
            self.setObjectName(input_name)

        if fixed_w is not None:
            self.setFixedWidth(fixed_w)
        else:
            if min_w is not None:
                self.setMinimumWidth(min_w)
            if max_w is not None:
                self.setMaximumWidth(max_w)
        if placeholder:
            self.addItem(placeholder)


class LabeledInput(QWidget):
    def __init__(
        self,
        label_text: str,
        input_type="line_edit",
        combo_box_options = set,
        input_name=None, #to set stylesheet
        min_w=100,
        max_w=400,
        fixed_w=None,
        placeholder="",
        digits_only=False,
        max_length=None,
        label_lenght=80,
    ):
        super().__init__()

        self.label = QLabel(label_text)
        self.label.setFixedWidth(label_lenght)

        if input_type == "line_edit":
            self.input = TextInput(
                input_name=input_name,
                min_w=min_w,
                max_w=max_w,
                fixed_w=fixed_w,
                placeholder=placeholder,
                digits_only=digits_only,
                max_length=max_length
            )
        elif input_type == "combo_box":
            self.input = ComboBox(
                input_name=input_name,
                min_w=min_w,
                max_w=max_w,
                fixed_w=fixed_w,
                placeholder=placeholder,
                )
            for option in combo_box_options:
                self.input.addItem(option)


        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.setStretch(0,0)
        layout.setStretch(1, 1)

        self.setLayout(layout)

    def __repr__(self):
        return f"{self.label.text()}"

    # pobieranie tekstu
    def text(self):
        try:
            return self.input.text()
        except:
            return self.input.currentText()

    # ustawianie tekstu
    def setText(self, value: str):
        self.input.setText(value)


    #focus po błędzie
    def focus(self):
        try:
            self.input.showPopup()
        except:
            pass
        self.input.setFocus()


#---------> Przykład użycia <----------------#

class ExampleForm(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()

        # Tworzymy pola
        self.name = LabeledInput("Imię:", min_w=150, max_w=250)
        self.surname = LabeledInput("Nazwisko:", min_w=150, max_w=250)
        self.age = LabeledInput("Wiek:", fixed_w=80, digits_only=True, max_length=3)
        self.city = LabeledInput("Miasto:", min_w=150, max_w=250)


        # przycisk
        btn = QPushButton("Zapisz")
        layout.addWidget(btn, 4, 0)

        self.setLayout(layout)
