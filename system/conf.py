from prettytable import PrettyTable
from system.utils import UserInput, UserOutput
from system.exceptions import *
from system.data import BitTable, RegisterTable
from interface.slave  import ConfigurationInterface, GenericInterace
from system.data import *

class ServerConfiguration:

    Options = ['RADDR', 'RPORT', 'FUNCTION', 'BURST', 'HELP', 'EXIT']
    helpOptions = [
        ['raddr', "Slave address"],
        ['rport', "Slave port"],
        ['functions', "Activate Function code requests"],
        ['bursts', "Modbus requested function burst sequences"],
        ['help', "This help menu"],
        ['done', "Finish configuration edition"],
        ['show', "Resume configuration values"]
    ]

    ConfigurationPrompt = "MASTER > CONFIGURATION >> "

    def __init__(self):
        self.SlaveAddr = "127.0.0.1"
        self.SlavePort = 502

        # Contains field propierties of each functionCode packets
        self.Functions = []

        # Specifies how are made communication packet bursts.
        self.Bursts = []

    def show(self):
        # TODO: show prettyable
        body = ''' 
        Slave Address:          %s
        Slave Port:             %d
        Active Functions:       %s
                    
        ''' % (self.SlaveAddr, self.SlavePort, str([code[0] for code in self.Functions]))

        UserOutput.information_resume("configuration", body)

    def edit_configuration(self):
        finished = False
        while not finished:
            fun = ServerConfiguration.switcher(UserInput.command_input(ServerConfiguration.ConfigurationPrompt))
            finished = fun(self)

    def __raddr(self):
        self.SlaveAddr = UserInput.value_input("Slave Address", type=str)
        return False

    def __rport(self):
        self.SlavePort = UserInput.value_input("Slave Port", type=int)
        return False

    def __functions(self):
        # TODO: Dont delete after reentrying
        if self.Functions:
            self.Functions = FunctionOptions.define(self.Functions)
        else:
            self.Functions = FunctionOptions.define()
        return False

    def __bursts(self):
        try:
            if self.Bursts:
                self.Bursts = BurstsOptions.define(self.Functions, self.Bursts)
            else:
                self.Bursts = BurstsOptions.define(self.Functions)
        except MasterError as ex:
            UserOutput.response_output(ex.message, 'error')
        return False

    def __help(self):
        table = PrettyTable()
        table.field_names = ["COMMAND", "DESCRIPTION"]
        for i in self.helpOptions:
            table.add_row(i)
        table.align['COMMAND'] = "l"
        table.align['DESCRIPTION'] = "l"
        print(table)
        return False

    def __invalid(self):
        pass

    def __exit(self):
        return True


    @staticmethod
    def switcher(value):
        switcher = {
            'raddr': ServerConfiguration.__raddr,
            'rport': ServerConfiguration.__rport,
            'functions': ServerConfiguration.__functions,
            'bursts': ServerConfiguration.__bursts,
            'done': ServerConfiguration.__exit,
            'help': ServerConfiguration.__help,
            'show': ServerConfiguration.show
        }
        return switcher.get(value, ServerConfiguration.__invalid)


class BurstsOptions:

    Prompt = "MASTER > CONFIGURATION > BURSTS >> "

    HelpCommand = [
        ['help', 'Help Menu'],
        ['add', 'Add new packets to current burst'],
        ['done', 'Save created functions'],
        ['del', 'Remove one packet from current burst'],
        ['show', 'Show current burst properties']
    ]

    # Burst packet propierties
    # ["burstIndex", "fcodeIndex", "delay", "Variance"]

    @staticmethod
    def define(functions, editing_burst=None):
        if not functions:
            raise MasterError("Function codes must be defined before burst creation.")
        if not editing_burst:
            editing_burst = []
        op = None
        while True:
            if op == "add":
                item = BurstsOptions.__add_to_burst(functions)
                if item:
                    # TODO: Problem!
                    item.insert(0, len(editing_burst))
                    editing_burst.append(item)
            elif op == "done":
                break
            elif op == "del":
                BurstsOptions.__del_from_burst(editing_burst, functions)
            elif op == "show":
                BurstsOptions.show_packets(editing_burst, functions)
            elif op == "help":
                BurstsOptions.__show_help()
            else:
                pass

            op = UserInput.command_input(BurstsOptions.Prompt)

        return editing_burst

    @staticmethod
    def __add_to_burst(functions):
        # print functions
        FunctionOptions.show_functions(functions)

        # Input parameters
        fcode_index = UserInput.value_input("Packet index", type=int, default=None, required=True)
        delay = UserInput.value_input("Transmission Delay", type=float, default=0.05987, required=False)
        variance = UserInput.value_input("Delay variance", type=float, default=0.003, required=False)
        return [fcode_index, delay, variance]

    @staticmethod
    def __del_from_burst(burst, functions):
        BurstsOptions.show_packets(burst, functions)
        while True:
            indx = UserInput.value_input("Packet index", type=int, default=None, required=True)
            if indx > len(burst):
                UserOutput.response_output("Enter a valid index", 'warning')
            else:
                burst.pop(indx)
                break


    @staticmethod
    def show_packets(burst, functions):
        table = PrettyTable()
        table.field_names = ["Function Code", "Delay", "Variance"]
        for index, i in enumerate(burst):
            if i:
                # fcode = functions[i[0]][1]
                row = [functions[i[0]][1]] + i[2:]
                print(row)
                table.add_row(row)
        table.align = "l"
        print(table)

    @staticmethod
    def __show_help():
        table = PrettyTable()
        table.field_names = ["COMMAND", "DESCRIPTION"]
        for i in BurstsOptions.HelpCommand:
            table.add_row(i)
        table.align['COMMAND'] = "l"
        table.align['DESCRIPTION'] = "l"
        print(table)


class FunctionOptions:

    Prompt = "MASTER > CONFIGURATION > FUNCTIONS >> "
    HelpCommand = [
        ['help', 'Help Menu'],
        ['add', 'Add new function code'],
        ['done', 'Save created functions'],
        ['show', 'Show current active function codes']
    ]

    @staticmethod
    def define(functions=None):
        """
        Creates functions options requesting to user.
        :return: Array of arrays containing parameters of each function
        """
        # Array that contains arrays of parameters
        # functions = [func_item1, func_item2, ...]
        # func_item ['funcCode', 'latency', 'variance', 'fieldsValues[]']
        if not functions:
            functions = []
        op = None
        while True:
            if op == "add":
                item = FunctionOptions.__create_func_item()
                if item:
                    item.insert(0, len(functions))
                    functions.append(item)
            elif op == "show":
                FunctionOptions.show_functions(functions)
            elif op == "help":
                FunctionOptions.__show_help()
                pass
            elif op == "done":
                break
            elif op == "exit":
                if functions:
                    a = UserInput.value_input("Exit without saving changes? (Y/N)", type=str)
                    if a == "y":
                        functions = []
                        break
                    else:
                        op = None
            elif op == "del":
                # TODO: corregir
                functions = [i for i in functions if UserInput.value_input("Function Code", type=int) not in i[0]]
            else:
                pass
            op = UserInput.command_input(FunctionOptions.Prompt)
        return functions


    @staticmethod
    def __create_func_item():
        # TODO: Validate values
        fcode = UserInput.value_input("Function Code", type=int, required=True)
        latency = UserInput.value_input("Latency", type=float, default=1.526167)
        variance = UserInput.value_input("Variance", type=float, default=0.004589)
        fields_array = FunctionOptions.__get_fields(fcode)
        return [fcode, latency, variance, fields_array]

    @staticmethod
    def show_functions(functions):
        table = PrettyTable()
        table.field_names = ["Index", "Function Code", "Latency", "Variance", "Fields Values"]
        for key, i in enumerate(functions):
            if i:
                table.add_row(i)
        table.align = "l"
        print(table)

    @staticmethod
    def __show_help():
        table = PrettyTable()
        table.field_names = ["COMMAND", "DESCRIPTION"]
        for i in FunctionOptions.HelpCommand:
            table.add_row(i)
        table.align['COMMAND'] = "l"
        table.align['DESCRIPTION'] = "l"
        print(table)

    @staticmethod
    def __get_fields(fcode):
        if fcode == 1:
            fields = ReadCoilFunction.get_parameters()
        elif fcode == 2:
            fields = ReadDiscreteInputsFunction.get_parameters()
        elif fcode == 15:
            fields = WriteMultipleCoilsFunction.get_parameters()
        elif fcode == 4:
            fields = ReadInputRegistersFunction.get_parameters()
        else:
            raise MasterError("Invalid function code selected.")
        return fields


class GenericFunction:

    ItemParameters = {
        'function_code': 0
    }


    @staticmethod
    def get_parameters():
        # TODO: esto esta mal
        for key, value in GenericFunction.ItemParameters.items():
            n_values = {key: 1}
            GenericFunction.ItemParameters.update(n_values)


class WriteMultipleCoilsFunction(GenericFunction):

    @staticmethod
    def get_parameters():
        start_addr = UserInput.value_input('Starting Address', type=int, default=0, required=False)
        quantity = UserInput.value_input('Quantity of Outputs', type=int, default=1, required=False)
        values = []
        for x in range(quantity):
            values.append(UserInput.value_input('Value %d' % x, type=bool, default=False, required=False))

        return [start_addr, quantity, values]


class ReadCoilFunction(GenericFunction):

    @staticmethod
    def get_parameters():
        start_addr = UserInput.value_input('Starting Address', type=int, default=0, required=False)
        quantity = UserInput.value_input('Quantity of Outputs', type=int, default=1, required=False)
        return [start_addr, quantity]


class ReadDiscreteInputsFunction(GenericFunction):

    @staticmethod
    def get_parameters():
        start_addr = UserInput.value_input('Starting Address', type=int, default=0, required=False)
        quantity = UserInput.value_input('Quantity of Outputs', type=int, default=1, required=False)
        return [start_addr, quantity]

class ReadInputRegistersFunction(GenericFunction):

    @staticmethod
    def get_parameters():
        start_addr = UserInput.value_input('Starting Address', type=int, default=0, required=False)
        quantity = UserInput.value_input('Quantity of Outputs', type=int, default=1, required=False)
        return [start_addr, quantity]

class SlaveConfiguration:

    DefaultFile = "default.cnf"
    MenuPrompt = "SLAVE > CONFIGURATION >>"

    def __init__(self):
        # Create data tables for each data type
        self.coils_table = BitTable(10000)
        self.discrete_inputs_table = BitTable(10000)
        self.holding_registers_table = RegisterTable(10000)
        self.input_registers_table = RegisterTable(10000)

        # Create access masks
        self.CoilsMask = CoilsMask(10000)
        self.InputRegistersMask = InputRegistersMask(10000)
        self.HoldingRegistersMask = HoldingRegistersMask(10000)
        self.DiscreteInputsMask = DiscreteInputsMask(10000)

        # Supported function codes
        self.SupportedFunctionCodes = []

        # Network information
        self.Address = "0.0.0.0"
        self.Port = 502

        # User defined parameters
        #self.edit_configuration()

    def edit_configuration(self):
        self.Address, self.Port = GenericInterace.get_general_configuration()
        option = GenericInterace.adding_blocks()
        while option != "Done":
            if option == "Add Coils":
                start, end = ConfigurationInterface().input("Coils")
                self.SupportedFunctionCodes.append(1)
                self.SupportedFunctionCodes.append(5)
                self.CoilsMask.add_block(start, end)
                self.coils_table.add_block(start, end)


            elif option == "Add InputRegister":
                start, end = ConfigurationInterface().input("InputRegisters")
                self.SupportedFunctionCodes.append(4)
                self.InputRegistersMask.add_block(start, end)
                self.input_registers_table.add_block(start, end)

            elif option == "Add HoldingRegisters":
                start, end = ConfigurationInterface().input("HoldingRegisters")
                self.SupportedFunctionCodes.append(3)
                self.SupportedFunctionCodes.append(6)
                self.HoldingRegistersMask.add_block(start, end)
                self.holding_registers_table.add_block(start, end)

            elif option == "Add DiscreteInputs":
                start, end = ConfigurationInterface().input("DiscreteInputs")
                self.SupportedFunctionCodes.append(2)
                self.DiscreteInputsMask.add_block(start, end)
                self.discrete_inputs_table.add_block(start, end)

            option = GenericInterace.adding_blocks()

    def main_config_interface(self):

        op = None
        while op != "done":
            if op == "laddr":
                #type, default = None, required = False
                self.Address = UserInput.value_input("Listening Address", type=str, default="127.0.0.1", required=False)
            elif op == "lport":
                print("TODO.")
            else:
                print("TODO")
            op = UserInput.command_input(SlaveConfiguration.MenuPrompt)
