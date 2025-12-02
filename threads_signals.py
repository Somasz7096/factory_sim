import sys
from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal, QTimer
from PyQt5.QtWidgets import (QPushButton, QLabel, QWidget, QProgressBar, QLineEdit,
                             QFrame, QHBoxLayout, QMainWindow, QApplication, QVBoxLayout,
                             QPlainTextEdit, QSpinBox)

import database_folder.database as db
from database_folder.database import session
from database_folder.models import Item, Order


class MainWindow(QMainWindow):
    speed_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.multiplier_value = 100
        self.workers = []
        self.threads = []
        self.orders = []
        self.is_running = False



        self.initUI()
        self.initThreads()



    def initUI(self):

        line = QFrame()


    # Time Layout#
        self.setWindowTitle("Taki mały program")
        time_layout = QVBoxLayout()

        self.startBtn = QPushButton("Start timer")
        self.startBtn.clicked.connect(self.start_timer)
        time_layout.addWidget(self.startBtn)

        self.pauseBtn = QPushButton("Pause")
        self.pauseBtn.clicked.connect(self.pause)
        time_layout.addWidget(self.pauseBtn)

        self.stopBtn = QPushButton("Stop")
        self.stopBtn.clicked.connect(self.stop)
        time_layout.addWidget(self.stopBtn)

        time_layout.addWidget(line)

        self.speed_value_input = QLineEdit()
        self.speed_value_input.setPlaceholderText("Enter time multiplier...")
        time_layout.addWidget(self.speed_value_input)

        self.set_multiplierBtn = QPushButton("Set multiplier")
        self.set_multiplierBtn.clicked.connect(self.speed_multiplier)
        time_layout.addWidget(self.set_multiplierBtn)

        self.multiplier_label = QLabel(str(self.multiplier_value))
        time_layout.addWidget(self.multiplier_label)


        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 60)
        self.progressBar.setTextVisible(False)
        time_layout.addWidget(self.progressBar)


    #Produce layout
        produce_layout = QVBoxLayout()

        self.items_id_input = QLineEdit()
        self.items_id_input.setPlaceholderText("Items ID...")
        produce_layout.addWidget(self.items_id_input)


        self.items_to_make_input = QSpinBox()
        self.items_to_make_input.setMaximum(2147483647) #QSpinBox limit
        produce_layout.addWidget(self.items_to_make_input)

        self.produceBtn = QPushButton("Place order")
        self.produceBtn.clicked.connect(self.add_order)
        produce_layout.addWidget(self.produceBtn)

        self.items_made_label = QLabel("0")
        self.items_made_label.setAlignment(Qt.AlignRight)
        produce_layout.addWidget(self.items_made_label)


        self.list_widget = QPlainTextEdit()
        self.list_widget.setDisabled(True)
        self.list_widget.setMaximumBlockCount(10)

        produce_layout.addWidget(self.list_widget)

        produce_layout.addWidget(line)

    #add to db layout
        db_layout = QVBoxLayout()

        self.item_type_input = QLineEdit()
        self.item_type_input.setPlaceholderText("Item type...")
        db_layout.addWidget(self.item_type_input)

        self.volume_input = QLineEdit()
        self.volume_input.setPlaceholderText("Volume...")
        db_layout.addWidget(self.volume_input)

        self.color_input = QLineEdit()
        self.color_input.setPlaceholderText("Color...")
        db_layout.addWidget(self.color_input)

        self.items_per_cycle_input = QSpinBox()
        self.items_per_cycle_input.setValue(0)
        db_layout.addWidget(self.items_per_cycle_input)



        self.db_add_button = QPushButton("Add item to database")
        self.db_add_button.clicked.connect(self.db_add)
        db_layout.addWidget(self.db_add_button)

        db_layout.addWidget(line)

    #Full layout
        hbox = QHBoxLayout()
        hbox.addLayout(time_layout)
        hbox.addLayout(produce_layout)
        hbox.addLayout(db_layout)

        central_widget = QWidget()
        central_widget.setLayout(hbox)
        self.setCentralWidget(central_widget)

    def initThreads(self):
        self.thread = QThread()
        self.thread.start()
        self.timer = QTimer()


        self.cycle_timer = Clock()
        self.cycle_timer.moveToThread(self.thread)

        self.cycle_timer.progress_signal.connect(self.progressBar.setValue)
        self.cycle_timer.finished.connect(lambda: self.progressBar.setValue(0))
        self.cycle_timer.finished.connect(self.timer.stop)


        self.timer.timeout.connect(self.cycle_timer.add_progress)

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
            self.multiplier_value = int(self.speed_value_input.text())
            self.multiplier_label.setText(str(self.multiplier_value))

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

class Clock(QObject):
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

