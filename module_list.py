from gui.clock import Clock
from gui.orders import Orders
try:
    from gui.new_item_gui import NewItemUI
    from modules.new_item import NewItem
except Exception as e:
    print(e)

modules_list = [
    # ("Button text", icon path, UI, logic)
    ("New item", "gui/icons/plus.png", NewItemUI, NewItem),
    # ("Clock", "gui/icons/address-book-blue.png", Clock),
    # ("Orders", "gui/icons/address-book.png", Orders),
    # ("Warehouse", "gui/icons/address-book-blue.png", Clock),
    # ("Items", "gui/icons/address-book.png", Clock),
    # ("Packing", "gui/icons/address-book-blue.png", Clock)
]
open_modules = {}
module_counter = 0