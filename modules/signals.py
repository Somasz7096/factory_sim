from PyQt6.QtCore import QObject, pyqtSignal

class AppSignals(QObject):
    # centralny sygnał, dostępny dla wszystkich modułów
    testsignal = pyqtSignal()

# tworzymy jedną instancję, którą będą importować moduły
signals = AppSignals()
