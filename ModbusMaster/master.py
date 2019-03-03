from ModbusMaster.system.interface import MainMenu, WorkingMenu
from ModbusMaster.system.core import Master

menu = MainMenu()
configuration = menu.start_menu()
master = Master(configuration)
master.start()

WorkingMenu.handle(master)

master.join()