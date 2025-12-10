from PyQt6.QtCore import QObject
from sqlalchemy import select
from database_folder.engine import SessionLocal




session = SessionLocal()

class NewItem(QObject):
    def __init__(self, ui: QWidget):
        super().__init__()
        print("New item module instanced")

        ui.testsignal.connect(self.print)

    def print(self):
        print("sygnał odebrany")


