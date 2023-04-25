from interface.server import MainMenu, WorkingMenu
from system.core import Master

menu = MainMenu()
configuration = menu.start_menu()
master = Master(configuration)
master.start()

WorkingMenu.handle(master)

master.join()
