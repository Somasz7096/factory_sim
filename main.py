import sys


from PyQt6.QtGui import QPalette, QColor, QAction, QIcon, QKeySequence
from PyQt6.QtCore import Qt, QThread, QObject, pyqtSignal, QTimer, QSize
from PyQt6.QtWidgets import (QPushButton, QLabel, QWidget, QLineEdit,
                             QFrame, QHBoxLayout, QMainWindow, QApplication, QVBoxLayout,
                             QPlainTextEdit, QSpinBox, QStatusBar, QToolBar, QSizePolicy,
                             QListWidget, QListWidgetItem, QStackedLayout, QToolButton,
                             QDockWidget)

from functools import partial

import database_folder.database as db
from database_folder.models import Item
from gui.clock import Clock
from module_list import modules_list


class MainWindow(QMainWindow):
    speed_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.multiplier_value = 100
        self.workers = []
        self.threads = []
        self.orders = []
        self.is_running = False


        self.open_modules = {}
        self.module_counters = 0

        self.initUI()

        # self.initThreads()






    def initUI(self):
        self.setMinimumSize(1200, 800)
        self.setWindowTitle("Taki mały program")
        self.init_layout()
        self.init_menubar()
        self.init_toolbar()
        self.setStatusBar(QStatusBar(self))
        self.init_list_menu()
        # self.init_module_field()
        self.statusBar().showMessage("Wellcome to factory_sim app")

    def init_layout(self):
        # self.hbox = QHBoxLayout()
        start_label = QLabel("WELLCOME TO FACTORY_SIM")
        self.hbox = QStackedLayout()
        self.hbox.addWidget(start_label)
        central_widget = QWidget()
        central_widget.setLayout(self.hbox)
        central_widget.setContentsMargins(0,0,0,0)
        self.setCentralWidget(central_widget)


    def init_menubar(self):
        menu = self.menuBar()


        # *--------------* PLACEHOLDERS *------------*

        file_menu = menu.addMenu("Plik")
        edit_menu = menu.addMenu("Edycja")

        file_menu.addAction("Nowy")
        file_menu.addAction("Otwórz")
        file_menu.addAction("Zapisz")
        file_menu.addSeparator()
        file_menu.addAction("Wyjście", self.close)

        edit_menu.addAction("Kopiuj")
        edit_menu.addAction("Wklej")
        edit_menu.addAction("Wytnij")

        # *--------------* PLACEHOLDERS *------------*


    def init_toolbar(self):

        top_toolbar = QToolBar("Top toolbar")
        top_toolbar.setIconSize(QSize(16, 16))
        top_toolbar.setMovable(False)
        top_toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.addToolBar(top_toolbar)

        # *--------------* PLACEHOLDERS *------------*

        button_action = QAction(QIcon("gui/icons/target.png"), "Target button", self)
        button_action.setCheckable(True)
        button_action.setStatusTip("This is target button")
        # button_action.triggered.connect(self.toolbar_button_clicked)
        button_action.setShortcut(QKeySequence("Ctrl+Shift+q"))
        top_toolbar.addAction(button_action)

        top_toolbar.addSeparator()

        button_action2 = QAction(QIcon("gui/icons/globe.png"), "Globe button", self)
        button_action2.setCheckable(True)
        button_action2.setStatusTip("This is globe button")
        # button_action2.triggered.connect(self.toolbar_button_clicked)
        button_action2.setShortcut(QKeySequence("Ctrl+q"))
        top_toolbar.addAction(button_action2)

        # *--------------* PLACEHOLDERS *------------*


    def init_list_menu(self):
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.Shape.StyledPanel)  # ramka panelu
        sidebar.setStyleSheet("background-color: white;")
        sidebar.setFixedWidth(150)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(5, 5, 5, 5)
        sidebar_layout.setSpacing(2)


        for text, icon_path, cls in modules_list:
            button = QToolButton()
            button.setText(text)
            button.setIcon(QIcon(icon_path))
            button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            button.clicked.connect(partial(self.init_module, cls))
            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        dock = QDockWidget("Modules", self)
        dock.setWidget(sidebar)
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, dock)

    def init_module_field(self):
        start_label = QLabel("WELLCOME TO FACTORY_SIM")
        module_layout = QStackedLayout()

        module_layout.addWidget(test_label)
        self.hbox.addLayout(module_layout)

    def init_module(self, module_cls):
        try:
            module_counter = len(self.open_modules) + 1

            name = f"{module_cls.__name__}[{module_counter}]"
            # if name not in self.open_modules:
            print(f"Tworzę instancję: {name}")
            self.open_modules[name] = module_cls()
            print(self.open_modules)

            cls_window = self.open_modules[name]
            self.hbox.addWidget(cls_window)
            self.hbox.setCurrentWidget(cls_window)
            cls_window.show()

            cls_window.destroyed.connect(lambda: self.desstroy_module(name))
        except Exception as e:
            print(e)

    def desstroy_module(self,name):
        self.open_modules.pop(name)
        print(f"{name} destroyed")




        # module1_button = QToolButton()
        # module1_button.setText("Module 1")
        # module1_button.setIcon(QIcon("gui/icons/address-book-blue.png"))
        # module1_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        # module1_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        # module1_button.clicked.connect(self.init_module)
        #
        # module2_button = QToolButton()
        # module2_button.setText("Module 2")
        # module2_button.setIcon(QIcon("gui/icons/address-book.png"))
        # module2_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        # module2_button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        #
        # sidebar_layout.addWidget(module1_button)
        # sidebar_layout.addWidget(module2_button)




        # time_layout = QVBoxLayout()
        # time_button = QPushButton("Timer settings")
        # time_layout.addWidget(time_button)
        # self.clock_window = clock.Clock()
        # try:
        #     time_button.clicked.connect(lambda: self.clock_window.hide()
        #     if self.clock_window.isVisible() else self.clock_window.show())
        # except Exception as e:
        #     print(e)
        #
        # self.clock_window.startBtn.clicked.connect(self.start_timer)
        # self.clock_window.pauseBtn.clicked.connect(self.pause)
        # self.clock_window.stopBtn.clicked.connect(self.stop)
        # self.clock_window.set_multiplierBtn.clicked.connect(self.speed_multiplier)

        #     time_layout.addWidget(self.multiplier_label)



#     #Produce layout
#         produce_layout = QVBoxLayout()
#
#         self.items_id_input = QLineEdit()
#         self.items_id_input.setPlaceholderText("Items ID...")
#         produce_layout.addWidget(self.items_id_input)
#
#
#         self.items_to_make_input = QSpinBox()
#         self.items_to_make_input.lineEdit().setPlaceholderText("Items to make.…")
#         self.items_to_make_input.clear()
#
#         self.items_to_make_input.setMaximum(2147483647) #QSpinBox limit
#         produce_layout.addWidget(self.items_to_make_input)
#
#         self.produceBtn = QPushButton("Place order")
#         self.produceBtn.clicked.connect(self.add_order)
#         produce_layout.addWidget(self.produceBtn)
#
#         self.items_made_label = QLabel("0")
#         self.items_made_label.setAlignment(Qt.AlignmentFlag.AlignRight)
#         produce_layout.addWidget(self.items_made_label)
#
#
#         self.list_widget = QPlainTextEdit()
#         self.list_widget.setDisabled(True)
#         self.list_widget.setMaximumBlockCount(10)
#
#         produce_layout.addWidget(self.list_widget)
#
#
#
#     #add to db layout
#         db_layout = QVBoxLayout()
#
#         self.item_type_input = QLineEdit()
#         self.item_type_input.setPlaceholderText("Item type...")
#         db_layout.addWidget(self.item_type_input)
#
#         self.volume_input = QLineEdit()
#         self.volume_input.setPlaceholderText("Volume...")
#         db_layout.addWidget(self.volume_input)
#
#         self.color_input = QLineEdit()
#         self.color_input.setPlaceholderText("Color...")
#         db_layout.addWidget(self.color_input)
#
#
#         self.items_per_cycle_input = QSpinBox()
#         self.items_per_cycle_input.lineEdit().setPlaceholderText("Items per cycle.…")
#         self.items_per_cycle_input.clear()
#         db_layout.addWidget(self.items_per_cycle_input)
#
#
#
#         self.db_add_button = QPushButton("Add item to database")
#         self.db_add_button.clicked.connect(self.db_add)
#         db_layout.addWidget(self.db_add_button)
#
#
#
#     #Full layout
#         hbox = QHBoxLayout()
#         hbox.addLayout(time_layout)
#         hbox.addLayout(produce_layout)
#         hbox.addLayout(db_layout)
#
#         central_widget = QWidget()
#         central_widget.setLayout(hbox)
#
#
#     def initThreads(self):
#         self.thread = QThread()
#         self.thread.start()
#         self.timer = QTimer()
#
#
#         self.cycle_timer = Clock_func()
#         self.cycle_timer.moveToThread(self.thread)
#
#         self.cycle_timer.progress_signal.connect(self.clock_window.progressBar.setValue)
#         self.cycle_timer.finished.connect(lambda: self.clock_window.progressBar.setValue(0))
#         self.cycle_timer.finished.connect(self.timer.stop)
#         self.timer.timeout.connect(self.cycle_timer.add_progress)
#
    def start_timer(self):
        print(f"start button, multiplier: {self.multiplier_value}")
        speed = 1000 // self.multiplier_value
        self.timer.start(speed)
        self.cycle_timer.cycle_finished.connect(self.process_order)


    def pause(self):
        print("pause button")
        self.timer.stop()
        print(f"active workers: {len(self.workers)}")
        print(f"active threads: {len(self.threads)}")


    def stop(self):
        print("stop button")
        self.cycle_timer.stop_worker()

    def speed_multiplier(self):
        try:
            self.multiplier_value = int(self.clock_window.speed_value_input.text())
            # self.multiplier_label.setText(str(self.multiplier_value))

            if self.timer.isActive():
                self.start_timer()
        except Exception as e:
            print(e)

    def produce_counter(self, i):
        print(i)
        items_produced_total = str(int(self.items_made_label.text()) + i)
        self.items_made_label.setText(str(items_produced_total))
        self.list_widget.insertPlainText(f"{str(items_produced_total)}")

    def add_order(self):

        index = self.items_id_input.text()
        result = db.load(index, Item)
        print(f"{result=}")

        if result:
            data = {
                "item_id": result.index,
                "items_per_cycle": result.items_per_cycle,
                "items_to_make": self.items_to_make_input.value()
            }
        else:
            print(f"[ERROR] no result in db for index: {index}")
            return


        print(f"** Order added **\n   ID: {data["item_id"]}\n   ({data["items_per_cycle"]}\n   Amount: {data["items_to_make"]}\n*****************")

        self.orders.append(data)
        print(self.orders)

    def remove_worker(self, worker):
        try:
            if worker in self.workers:
              self.workers.remove(worker)
        except Exception as e:
            print(e)

    def remove_thread(self, thread):
        try:
            if thread in self.threads:
                self.threads.remove(thread)
        except Exception as e:
            print(e)

    def process_order(self):
        try:
            if self.is_running:
                return
                # print("Already running")
            else:
                # if len(self.orders) == 0:
                #     self.is_running = False
                data = self.orders.pop(0)
                self.is_running = True
                self.produce_start(data)
        except:
            return
            # print("No orders")




    def produce_start(self, data):

        try:
            thread = QThread()

            produce = Produce(data)
            produce.moveToThread(thread)

            produce.items_produced.connect(self.produce_counter)
            self.cycle_timer.cycle_finished.connect(produce.run)

            produce.finished.connect(lambda: self.remove_worker(produce))
            produce.finished.connect(thread.quit)
            produce.finished.connect(produce.deleteLater)
            thread.finished.connect(thread.deleteLater)
            produce.finished.connect(lambda: self.remove_thread(thread))

            produce.is_running.connect(self.turn_off)


            self.workers.append(produce)
            self.threads.append(thread)

            thread.start()
        except Exception as e:
            print(e)

    def turn_off(self, is_running):
        if not is_running:
            self.is_running = False

        print(f"==============={is_running}")


    def db_add(self):
        item_type = self.item_type_input.text()
        volume = self.volume_input.text()
        color = self.color_input.text()
        items_per_cycle = self.items_per_cycle_input.value()

        record = Item(
            type=item_type,
            volume=volume,
            color=color,
            items_per_cycle=items_per_cycle
        )
        try:
            db.save(record)
        except Exception as e:
            print(e)

class Clock_func(QObject):
    progress_signal = pyqtSignal(int)
    finished = pyqtSignal()
    cycle_finished = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.progress = 0
    def add_progress(self):
        try:
            self.progress += 1
            self.progress_signal.emit(self.progress)

            if self.progress == 60:
                self.progress = 0
                self.cycle_finished.emit()


        except Exception as e:
            print(e)
    def stop_worker(self):
        try:
            print(f"dump progress placeholer: {self.progress}")
            self.progress = 0
            self.progress_signal.emit(self.progress)
            self.finished.emit()
        except Exception as e:
            print(e)


class Produce(QObject):
    items_produced = pyqtSignal(int)
    finished = pyqtSignal(int)
    is_running = pyqtSignal(bool)


    def __init__(self, data):
        super().__init__()
        self.item_id = data["item_id"]
        self.items_per_cycle = int(data["items_per_cycle"])
        self.items_to_make = int(data["items_to_make"])
        self.items_to_make_left = self.items_to_make

        self.items_made = None


    def run(self):
        try:
            self.items_to_make_left -= self.items_per_cycle

            self.items_made = self.items_to_make + (0 - self.items_to_make_left)
            if self.items_to_make_left >= 1:
                print(f"[{self.item_id}] production in progress - ({self.items_made} / {self.items_to_make})")

            elif self.items_to_make_left <= 0:
                print(f"[{self.item_id}] production complete, made {self.items_made} items(Overproduction - {0 - self.items_to_make_left}\n{len(window.orders)} orders left.")
                self.finished.emit(self.items_made)
                self.is_running.emit(False)

        except Exception as e:
            print(e)

def force_light_theme(app: QApplication):
    """
    Wymusza styl Fusion i jasną paletę, niezależnie od systemowego dark mode.
    Działa dla wszystkich widgetów w aplikacji.
    """
    # 1. Wymuś styl Fusion
    app.setStyle("Fusion")

    # 2. Utwórz jasną paletę
    palette = QPalette()

    # Główne kolory okien i tekstu
    palette.setColor(QPalette.ColorRole.Window, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(230, 230, 230))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.Button, QColor(230, 230, 230))
    palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.black)
    palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(122, 100, 100))

    # Kolory zaznaczeń
    palette.setColor(QPalette.ColorRole.Highlight, QColor(0, 120, 215))
    palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)

    # 3. Ustaw paletę aplikacji
    app.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    force_light_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

