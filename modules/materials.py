from PyQt6.QtCore import QObject
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from database_folder.engine import SessionLocal



class NewItem(QObject):
    def __init__(self, ui: QWidget):
        super().__init__()
        self.ui = ui
        ui.save_signal.connect(self._save)
        ui.feedback_signal.connect(self._add_feedback)


    def _save(self, combined_data):

        model = combined_data[0]
        data = combined_data[1]

        with SessionLocal() as session:
            try:
                #czyści opcjonalną wartość id żeby przypisać ją automatycznie przez sqlalchemy
                if data["material_id"] == "":
                    data["material_id"] = None

                '''dodaje rekord do tabeli, ** rozpakowuje słownik, 
                    klucze w słowniku muszę być równe nazwie kolumny'''
                session.add(model(**data))
                session.commit()
                return True
            except IntegrityError:
                session.rollback()
                print(f"Integryity error")
                return False
            except Exception as e:
                session.rollback()
                print(e)
                return False

    def _add_feedback(self, feedback):
        try:
            self.ui.feedback_label.setText(f"{feedback}")
        except Exception as e:
            print(e)


