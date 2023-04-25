from threading import Thread
from system.utils import UserInput, UserOutput
from prettytable import PrettyTable
from system.conf import SlaveConfiguration as Configuration
from slavesys import Slave
from system.handler import Handler
import pickle
import os


class Menu(Thread):
    """
    This class manages program promt, selected configuration and active slaves threads.

    Atributes:
        Configuring (bool): Boolean that shows configuration process.

        Active (bool): Boolean that shows current slave thread status. Stopped/running.

        CurrentSlave (class): Managed slave class object.

        Config (class): Set configuration class.
    """

    Prompt = "SLAVE >> "

    helpCommand = [
        ['help', 'Help menu'],
        ['new', 'Create new Slave configuration'],
        ['export', 'Export to file Slave configuration'],
        ['import', 'Import Slave configuration from file'],
        ['default', 'Load default configuration for Slave'],
        ['edit', 'Edit current configuration'],
        ['status', 'Show slave current status'],
        ['start', 'Start the Slave with specified configuration parameters'],
        ['exit', 'Exit the console']
    ]

    def __init__(self):
        Thread.__init__(self)
        self.Configuring = True
        self.Active = False
        self.CurrentSlave = None
        self.Config = None

    def run(self):
        self.__get_commands()

    def __get_commands(self):
        """
        Ask user for program configuration. It will be in loop until configuration ends.
        :return:
        """
        while self.Configuring:
            command = self.__switcher(UserInput.command_input(Menu.Prompt))
            if command:
                command()

    def __create_configuration(self):
        """
        Creates a new configuration object and show configuration prompt to user.
        :return:
        """
        new_conf = Configuration()
        config_menu = ConfigurationMenu(new_conf)
        config_menu.edit()
        self.Config = new_conf

    def __help(self):
        """
        Show help command of the current menu.
        :return:
        """
        table = PrettyTable()
        table.field_names = ["COMMAND", "DESCRIPTION"]
        for i in self.helpCommand:
            table.add_row(i)
        table.align['COMMAND'] = "l"
        table.align['DESCRIPTION'] = "l"
        print(table)

    def __start(self):
        """
        Starts the slave with set configuration.
        :return:
        """
        self.CurrentSlave = Slave(self.Config)
        handler = Handler(self.Config.coils_table,
                          self.Config.discrete_inputs_table,
                          self.Config.input_registers_table,
                          self.Config.holding_registers_table)
        handler.start()
        self.Active = True
        self.CurrentSlave.start()
        self.__get_commands()
        handler.join()
        self.CurrentSlave.join()

    def __show(self):
        """
        Shows current configuration object parameters.
        :return:
        """
        if not self.Config:
            UserOutput.response_output("No configuration yet.", "error")
        else:
            print("\t\tLocal Address %s\n\t\tLocal Port %d\n\t\tSupported Codes %s"
                  % (self.Config.Address, self.Config.Port,
                     str(self.Config.SupportedFunctionCodes)))
            print("\t\tCoils:\n\t\t\tCodes: %s\n\t\t\tBlocks: %s" % (str(self.Config.SupportedFunctionCodes),
                                                                     self.Config.CoilsMask.show_blocks()))

    def __status(self):
        """
        Show the status (running/stopped) of current slave.
        :return:
        """
        if self.Active:
            UserOutput.information_resume("SLAVE STATUS", "Slave is currently running")
        else:
            UserOutput.information_resume("SLAVE STATUS", "Slave not running")

    def __stop(self):
        if self.Active:
            UserOutput.response_output("TO DO: make slave run under a start/stop flag.", type='info')
        else:
            UserOutput.response_output("Slave is not running", type='error')

    def __edit(self):
        """
        Goes to editing configuration menu of the current configuration object.
        :return:
        """
        if not self.Config:
            UserOutput.response_output("No configuration yet", "error")
        else:
            config_menu = ConfigurationMenu(self.Config)
            config_menu.edit()

    def __exit(self):
        self.Configuring = False

    def __export(self):
        """
        Exports the current cofiguration object to a binary file.
        :return:
        """
        confdir_path = "./config/"
        if not os.path.exists(confdir_path):
            os.mkdir(confdir_path)

        filename = UserInput.value_input("Select a file name", type=str, default=None, required=True)
        path = os.path.join(confdir_path, filename)
        with open(path, 'wb') as handle:
            pickle.dump(self.Config, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def __import(self):
        """
        Imports a configuration object from a binary file.
        :return:
        """
        confdir_path = "./conf/"
        body = ''
        for x in os.listdir(confdir_path):
            body += "\t%s \n\t" % x
        UserOutput.information_resume("FILES", body)

        filename = UserInput.value_input("Enter configuration file name", type=str, default=None, required=True)
        path = confdir_path + filename
        with open(path, 'rb') as handle:
            self.Config = pickle.load(handle)

    def __switcher(self, option):
        """
        Switch/case function.
        :param option: selected input string for prompt option.
        :return: selected function.
        """
        switcher = {
            'help': self.__help,
            'import': self.__import,
            'export': self.__export,
            'start': self.__start,
            'show': self.__show,
            'edit': self.__edit,
            'default': self.__help,
            'new': self.__create_configuration,
            'exit': self.__exit,
            'status': self.__status
        }
        return switcher.get(option)


class ConfigurationMenu:
    """
    Menu to configuration object manipulation.

    Atributes:
        EditingConfiguration (object): The object that is currently configuring.

        Editing (bool): A flag to show the status of the object.
    """

    Prompt = "SLAVE > CONFIGURATION >> "

    helpCommand = [
        ['help', 'Help menu'],
        ['show', 'Show current configuration'],
        ['laddr', 'Change listening local address'],
        ['lport', 'Change listening local address'],
        ['data', 'Edit data type tables'],
        ['exit', 'Back to main menu'],
        ['done', 'Save current configuration']
    ]

    def __init__(self, configuration):
        self.EditingConfiguration = configuration
        self.Editing = True

    def edit(self):
        while self.Editing:
            command = self.__switcher(UserInput.command_input(ConfigurationMenu.Prompt))
            if command:
                command()

    def __exit(self):
        self.Editing = False

    def __done(self):
        self.Editing = False

    def __lport(self):
        self.EditingConfiguration.Port = UserInput.value_input("Listening Port", type=int,
                                                               default=self.EditingConfiguration.Port)

    def __laddr(self):
        self.EditingConfiguration.Address = UserInput.value_input("Listening Address", type=str,
                                                                  default=self.EditingConfiguration.Address)

    def __data(self):
        data_menu = DataMenu(self.EditingConfiguration)
        data_menu.edit()
        pass

    def __show(self):
        ConfigurationResume.print_general(self.EditingConfiguration.Address, self.EditingConfiguration.Port,
                                          self.EditingConfiguration.SupportedFunctionCodes)
        if self.EditingConfiguration.CoilsMask.Blocks:
            ConfigurationResume.print_blocks("COILS", self.EditingConfiguration.CoilsMask.Blocks)
        if self.EditingConfiguration.InputRegistersMask.Blocks:
            ConfigurationResume.print_blocks("INPUT REGISTERS", self.EditingConfiguration.InputRegistersMask.Blocks)

        if self.EditingConfiguration.HoldingRegistersMask.Blocks:
            ConfigurationResume.print_blocks("HOLDING REGISTERS", self.EditingConfiguration.HoldingRegistersMask.Blocks)

        if self.EditingConfiguration.DiscreteInputsMask.Blocks:
            ConfigurationResume.print_blocks("DISCRETE INPUTS", self.EditingConfiguration.DiscreteInputsMask.Blocks)

    def __help(self):
        table = PrettyTable()
        table.field_names = ["COMMAND", "DESCRIPTION"]
        for i in self.helpCommand:
            table.add_row(i)
        table.align['COMMAND'] = "l"
        table.align['DESCRIPTION'] = "l"
        print(table)

    def __switcher(self, option):
        switcher = {
            'help': self.__help,
            'show': self.__show,
            'laddr': self.__laddr,
            'lport': self.__lport,
            'data': self.__data,
            'exit': self.__exit,
            'done': self.__done
        }
        return switcher.get(option)


class DataMenu:

    Prompt = "SLAVE > CONFIGURATION > DATA >> "

    helpCommand = [
        ['help', 'Help menu'],
        ['show', 'Show current configuration'],
        ['coils', 'Add coils data block'],
        ['iregisters', 'Add input register data block'],
        ['hregisters', 'Add holding register data block'],
        ['dinputs', 'Add discrete inputs data block'],
        ['exit', 'Back to main menu'],
        ['done', 'Save current configuration']
    ]

    # Each Data table will have 10000 available addresses
    TablesDefaultSize = 10000

    def __init__(self, configuration):
        self.EditingConfifugration = configuration
        self.Editing = True

    def edit(self):
        while self.Editing:
            command = self.__switcher(UserInput.command_input(DataMenu.Prompt))
            if command:
                command()

    def __switcher(self, option):
        switcher = {
            'help': self.__help,
            'show': self.__show,
            'coils': self.__add_coils,
            'iregisters': self.__add_input_registers,
            'hregisters': self.__add_holding_registers,
            'dinputs': self.__add_discrete_inputs,
            'exit': self.__exit,
            'done': self.__done
        }
        return switcher.get(option)

    def __add_function_codes(self, array):
        """
        Append codes to configuration supported function codes array.
        :param array: An array of integers to be added in current configuration supported function codes.
        :return:
        """
        for i in array:
            if i not in self.EditingConfifugration.SupportedFunctionCodes:
                self.EditingConfifugration.SupportedFunctionCodes += [i]

    def __add_coils(self):
        # (value_name, type, default=None, required=False):
        start_addr = UserInput.value_input("Starting Address", type=int, required=True)
        quantity = UserInput.value_input("Quantity", type=int, required=True)

        # Create accessible mask
        self.EditingConfifugration.CoilsMask.add_block(start_addr, start_addr + quantity)

        # Notify active block (for handler)
        self.EditingConfifugration.coils_table.add_block(start_addr, start_addr + quantity)

        # Add function codes.
        self.__add_function_codes([1, 5, 15])

    def __add_input_registers(self):
        # (value_name, type, default=None, required=False):
        start_addr = UserInput.value_input("Starting Address", type=int, required=True)
        quantity = UserInput.value_input("Quantity", type=int, required=True)

        # Create accessible mask
        self.EditingConfifugration.InputRegistersMask.add_block(start_addr, start_addr + quantity)

        # Notify active block (for handler)
        self.EditingConfifugration.input_registers_table.add_block(start_addr, start_addr + quantity)

        self.__add_function_codes([4])

    def __add_holding_registers(self):
        # (value_name, type, default=None, required=False):
        start_addr = UserInput.value_input("Starting Address", type=int, required=True)
        quantity = UserInput.value_input("Quantity", type=int, required=True)

        # Create accessible mask
        self.EditingConfifugration.HoldingRegistersMask.add_block(start_addr, start_addr + quantity)

        # Notify active block (for handler)
        self.EditingConfifugration.holding_registers_table.add_block(start_addr, start_addr + quantity)

        # Add function codes.
        self.__add_function_codes([3, 6, 16])

    def __add_discrete_inputs(self):
        # (value_name, type, default=None, required=False):
        start_addr = UserInput.value_input("Starting Address", type=int, required=True)
        quantity = UserInput.value_input("Quantity", type=int, required=True)

        # Create accessible mask
        self.EditingConfifugration.DiscreteInputsMask.add_block(start_addr, start_addr + quantity)

        # Notify active block (for handler)
        self.EditingConfifugration.discrete_inputs_table.add_block(start_addr, start_addr + quantity)

        # Add function codes.
        self.__add_function_codes([2])

    def __exit(self):
        self.Editing = False

    def __done(self):
        self.Editing = False

    def __show(self):
        UserOutput.response_output("To Do...", "warning")

    def __help(self):
        table = PrettyTable()
        table.field_names = ["COMMAND", "DESCRIPTION"]
        for i in self.helpCommand:
            table.add_row(i)
        table.align['COMMAND'] = "l"
        table.align['DESCRIPTION'] = "l"
        print(table)


class ConfigurationResume:

    TITLE = '''
    
                    SLAVE CONFIGURATION
                
                Local Address       %s
                Local Port          %d
                Supported Codes     %s
    '''

    @staticmethod
    def print_general(laddr, lport, scodes):
        print(ConfigurationResume.TITLE % (laddr, lport, scodes))

    @staticmethod
    def print_blocks(title, blocks):
        output_string = '''\t\t\t\t%s\n''' % title
        for i in blocks:
            output_string += "\t\t\t\t\tFrom    %d to   %d\n" % (i[0], i[1])
        print(output_string)


