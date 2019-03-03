from ModbusSlave.core.interface import ConfigurationInterface, GenericInterace
from ModbusSlave.core.data import *
from ModbusSlave.core.data import BitTable, RegisterTable
from ModbusSlave.core.configuration.utils import UserInput


class Configuration:

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
        while option is not "Done":
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
            op = UserInput.command_input(Configuration.MenuPrompt)