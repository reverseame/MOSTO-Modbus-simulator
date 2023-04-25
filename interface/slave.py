from easygui import *
import sys, pickle


class MainMenu:

    @staticmethod
    def start_menu():
        from ModbusSlave.core.utils import Configuration

        option = GenericInterace.get_load_option()
        if option is "Default":  # Default Configuration
            configuration = GenericInterace.reload_configuration("./default.cnf")
            return configuration

        elif not option:  # Create Configuration
            configuration = Configuration()
            selected_dir = GenericInterace.ask_save()
            if selected_dir:
                GenericInterace.save_configuration(configuration, selected_dir)
            return configuration

        else:  # Load from file
            # option = selected_file
            configuration = GenericInterace.reload_configuration(option)
            return configuration


class GenericInterace:

    @staticmethod
    def get_load_option():
        msg = "Select a configuration for Slave"
        choices = ["New Configuration", "Default", "Choose", "Cancel"]
        reply = buttonbox(msg, title="Configuration", choices=choices)
        if reply is "Cancel":
            sys.exit(1)
        if reply is "New Configuration":
            reply = False
        if reply is "Choose":
            reply = fileopenbox(msg="Select saving directory", title="Save Configuration", default="./conf/",
                                filetypes=["*.cnf", "CNF files"])
            if not reply:
                sys.exit(1)
        return reply

    @staticmethod
    def get_general_configuration():
        fieldNames = ["Host Address", "Port"]
        addr, port = multenterbox("Enter Slave general configuration", "Configuration", fieldNames)
        return addr, int(port)

    @staticmethod
    def adding_blocks():
        choices = ["Add Coils", "Add HoldingRegisters", "Add DiscreteInputs", "Add InputRegister", "Done"]
        reply = buttonbox("Select option", title="Configuration", choices=choices)
        return reply

    @staticmethod
    def ask_save():
        msg = "Do you want to save configuration?"
        title = "Please Confirm"
        choices = ["Save", "Set as default", "Cancel"]
        selected = buttonbox(msg, title=title, choices=choices)
        if selected == "Save":  # show a Continue/Cancel dialog
            # user chose Save to file
            selected_dir = filesavebox(msg="Select saving directory", title="Save Configuration", default="./save.slave")
        elif selected == "Set as default":
            selected_dir = "./default.cnf"
        else:
            selected_dir = None
        return selected_dir

    @staticmethod
    def save_configuration(configuration, filename):
        with open(filename, 'wb') as handle:
            pickle.dump(configuration, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def reload_configuration(file_name):
        with open(file_name, 'rb') as handle:
            configuration = pickle.load(handle)
        return configuration


class ConfigurationInterface:

    ConfigItems = ['DiscreteInputs', 'Coils', 'InputRegisters', 'HoldingRegisters']
    Ranges = ['[0-65535]', '0-4095']

    def input(self, config_item):
        if config_item not in self.ConfigItems:
            raise ValueError("Config item must be one of next values: " + str(self.ConfigItems))
        interval = '[0-65535]'
        self.msg = "Enter a range for " + config_item + " values. " + interval
        title = "Slave Configuration"
        field_name = ["Range"]
        field_values = multenterbox(self.msg, title, field_name)

        if not field_values:  # Cancelled
            sys.exit(0)

        [start, end] = self.__validate_values(field_values[0])
        return start, end


    @staticmethod
    def __validate_values(range):
        range = range.strip()
        range = range.split('-')
        start = int(range[0])
        end = int(range[1])
        if start >= end:
            # Invalid range
            pass
        elif start < 0:
            # Invalid range
            pass
        elif end > 65535:
            # Invalid range
            pass
        else:
            # Data Ok
            pass
        return start, end






