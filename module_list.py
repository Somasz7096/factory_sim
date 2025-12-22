from gui.clock import Clock
from gui.orders import Orders
try:
    from gui.materials_ui import Materials_ui
    from modules.materials import Materials_logic
except Exception as e:
    print(e)

modules_list = [
    # ("Button text", icon path, UI, logic)
    ("Materials", "gui/icons/plus.png", Materials_ui, Materials_logic),
    # ("Clock", "gui/icons/address-book-blue.png", Clock),
    # ("Orders", "gui/icons/address-book.png", Orders),
    # ("Warehouse", "gui/icons/address-book-blue.png", Clock),
    # ("Items", "gui/icons/address-book.png", Clock),
    # ("Packing", "gui/icons/address-book-blue.png", Clock)
]
open_modules = {}
module_counter = 0