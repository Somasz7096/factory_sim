from gui.clock import Clock
from gui.orders import Orders

modules_list = [
    # ("Button text", icon path, Module Class)
    ("Clock", "gui/img/address-book-blue.png", Clock),
    ("Orders", "gui/img/address-book.png", Orders),
    ("Warehouse", "gui/img/address-book-blue.png", Clock),
    ("Items", "gui/img/address-book.png", Clock),
    ("Packing", "gui/img/address-book-blue.png", Clock)
]
open_modules = {}
module_counter = 0