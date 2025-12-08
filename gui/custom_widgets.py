from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout

from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QHBoxLayout, QGridLayout

class TextInput(QLineEdit):
    def __init__(self, min_w=None, max_w=None, fixed_w=None, placeholder="", digits_only=False, max_length=None):
        super().__init__()

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
            from PyQt6.QtGui import QIntValidator
            self.setValidator(QIntValidator())


class LabeledInput(QWidget):
    def __init__(
        self,
        label_text: str,
        min_w=None,
        max_w=None,
        fixed_w=None,
        placeholder="",
        digits_only=False,
        max_length=None
    ):
        super().__init__()

        self.label = QLabel(label_text)
        self.input = TextInput(
            min_w=min_w,
            max_w=max_w,
            fixed_w=fixed_w,
            placeholder=placeholder,
            digits_only=digits_only,
            max_length=max_length
        )

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.input)

        self.setLayout(layout)

    # pobieranie tekstu
    def text(self):
        return self.input.text()

    # ustawianie tekstu
    def setText(self, value: str):
        self.input.setText(value)

    # dodanie widgetu do siatki
    def add_to_grid(self, grid: QGridLayout, row: int, col: int, colspan=1):
        grid.addWidget(self, row, col, 1, colspan)

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

        # Wstawiamy do siatki
        self.name.add_to_grid(layout, 0, 0, colspan=2)
        self.surname.add_to_grid(layout, 1, 0, colspan=2)
        self.age.add_to_grid(layout, 2, 0, colspan=1)
        self.city.add_to_grid(layout, 3, 0, colspan=2)

        # przycisk
        btn = QPushButton("Zapisz")
        layout.addWidget(btn, 4, 0)

        self.setLayout(layout)
