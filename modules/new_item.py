from PyQt6.QtCore import QObject
from sqlalchemy import select
from database_folder.engine import SessionLocal
from database_folder import models




session = SessionLocal()

class NewItem(QObject):
    def __init__(self, ui: QWidget):
        super().__init__()
        print("New item module instanced")

        ui.save_signal.connect(self.print)

    def print(self, combined_data):
        print(combined_data, sep='\n')
        # item_type = data["Item type"]
        # try:
        #     print(item_type)
        # except Exception as e:
        #     print(e)

        model = combined_data[0]
        data = combined_data[1]

        try:
            #czyści opcjonalną wartość id żeby przypisać ją automatycznie przez sqlalchemy
            if data["material_id"] == "":
                data["material_id"] = None

            '''dodaje rekord do tabeli, ** rozpakowuje słownik, 
                klucze w słowniku muszę być równe nazwie kolumny'''
            session.add(model(**data))
            session.commit()
        except Exception as e:
            print(e)




