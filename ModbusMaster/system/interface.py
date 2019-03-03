import pickle
from ModbusMaster.system.conf import Configuration
import sys
from prettytable import PrettyTable
from ModbusMaster.system.utils import UserOutput, UserInput
import os

class MainMenu:
    # COMMANDS = ['help', 'import', 'export', 'start', 'show', 'create', 'default', 'exit']
    helpCommand = [
        ['help', 'Help menu'],
        ['new', 'Create new Master configuration'],
        ['export', 'Export to file Master configuration'],
        ['import', 'Import Master configuration from file'],
        ['default', 'Load default configuration for Master'],
        ['show', 'Show current configuration'],
        ['edit', 'Edit current configuration'],
        ['start', 'Start the master with specified configuration parameters'],
        ['exit', 'Exit the console']
    ]

    def __init__(self):
        self.finished = False
        self.loaded_configuration = None

    def switcher(self, option):
        switcher = {
            'help': self.help,
            'import': self.conf_import,
            'export': self.conf_export,
            'start': self.start,
            'show': self.show,
            'edit': self.edit,
            'default': self.default,
            'new': self.create_configuration,
            'exit': self.exit
        }
        return switcher.get(option)

    def start_menu(self):
        UserOutput.banner()
        while not self.finished:
            option = UserInput.command_input("MASTER >> ")
            # option = input("MASTER >> ")
            func = self.switcher(option.lower())
            if func:
                func()
            else:
                pass
        return self.loaded_configuration


    def help(self):
        table = PrettyTable()
        table.field_names = ["COMMAND", "DESCRIPTION"]
        for i in self.helpCommand:
            table.add_row(i)
        table.align['COMMAND'] = "l"
        table.align['DESCRIPTION'] = "l"
        print(table)

    def conf_import(self):
        confdir_path = "./config/"
        body = ''
        for x in os.listdir(confdir_path):
            body += "\t%s \n\t" % x
        UserOutput.information_resume("FILES", body)

        filename = UserInput.value_input("Enter configuration file name", type=str, default=None, required=True)
        path = confdir_path + filename
        with open(path, 'rb') as handle:
            self.loaded_configuration = pickle.load(handle)
        pass

    def edit(self):
        if not self.loaded_configuration:
            if UserInput.value_input("There is no configuration loaded, "
                                     "what you to create a new one? (Y/N)", type=str) == 'y':
                self.create_configuration()
            else:
                pass
        else:
            self.loaded_configuration.edit_configuration()

    def conf_export(self):
        conf_dir = './config/'
        if not self.loaded_configuration:
            UserOutput.response_output("There is no configuration to export. You must create one before.", type='error')
        else:
            filename = UserInput.value_input("Select a name for configuration file: ", type=str)
            with open(conf_dir + filename, 'wb') as fp:
                pickle.dump(self.loaded_configuration, fp, protocol=pickle.HIGHEST_PROTOCOL)

    def start(self):
        if not self.loaded_configuration:
            UserOutput.response_output("There is no configuration loaded. You must create or import one before.",
                                       type='error')
        else:
            self.finished = True

    def show(self):
        if self.loaded_configuration:
            self.loaded_configuration.show()
        else:
            UserOutput.response_output("There is no configuration loaded. You must create or import one before.",
                                       type='error')

    def default(self):
        print("To do...")
        pass

    def create_configuration(self):
        new_conf = Configuration()
        new_conf.edit_configuration()
        self.loaded_configuration = new_conf

    def exit(self):
        o = UserInput.value_input("Are you sure you want to exit? (Y/N) > ", type=str)
        # o = input()
        if o.lower() == 'y':
            self.loaded_configuration = None
            sys.exit(0)

class WorkingMenu:

    @staticmethod
    def handle(master_thread):
        while True:
            op = input("MASTER (Running) > ")
            if op.lower() == "stop":
                master_thread.stop()
                break
            elif op.lower() == "help":
                print("TODO: show help")
            else:
                pass
