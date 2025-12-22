from PyQt6.QtCore import QObject
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from database_folder.engine import SessionLocal
from database_folder.models import Materials_db


class Materials_logic(QObject):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        ui.save_signal.connect(self._save)


    def _save(self, data):

        with SessionLocal(expire_on_commit=False) as session:
            try:
                #czyści opcjonalną wartość material_id żeby przypisać ją automatycznie przez sqlalchemy
                if data["material_id"] == "":
                    data["material_id"] = None

                '''dodaje rekord do tabeli, ** rozpakowuje słownik, 
                    klucze w słowniku muszę być równe nazwie kolumny'''

                new_material = Materials_db(**data)
                session.add(new_material)

                session.flush() # generuje material_id jako primary_key, jeszcze nie commituje
                assigned_id = new_material.material_id # pobiera material_id, rekord jeszcze nie zapisany w bazie
                session.commit()

                data["material_id"] = assigned_id # aktualizuje słownik rekordu

                self.ui.display_confirmation(data)

            except IntegrityError:
                session.rollback()
                self.ui.feedback_label.setText(f"material_id {self.ui.id_input.text()} already exists")

            except Exception as e:
                session.rollback()
                print(e)



