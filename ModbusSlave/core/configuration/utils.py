import socket
from scapy.all import StreamSocket, Raw
from datetime import datetime
from core.logging import colors


class UserOutput:
    eol = '\n' + colors.reset
    warning = '\t\t[' + colors.bold + colors.fg.yellow + '*' + colors.reset + '] '
    information = '\t\t[' + colors.bold + colors.fg.cyan + '*' + colors.reset + '] '
    confirmation = '\t\t[' + colors.bold + colors.fg.green + '*' + colors.reset + '] '
    standard = '\t\t[' + colors.bold + colors.fg.lightgrey + '*' + colors.reset + '] '
    error = '\t\t[' + colors.bold + colors.fg.red + 'x' + colors.reset + '] '
    exception = '\t\t[' + colors.bold + colors.fg.red + '!' + colors.reset + '] ' + colors.fg.red

    Types = {
        'standard': standard,
        'warning': warning,
        'info': information,
        'confirm': confirmation,
        'error': error,
        'exception': exception
    }

    @staticmethod
    def response_output(message, type='standard'):
        t = UserOutput.Types.get(type)
        print(t + message + UserOutput.eol)

    @staticmethod
    def information_resume(title, body):
        title = "\n\n\t\t\t\t" + colors.bold + colors.fg.cyan + title.upper() + colors.reset + '\n'
        body = '\t' + colors.fg.cyan + body + colors.reset
        print(title + body)

    @staticmethod
    def banner():
        title = "\n\n\t\t\t" + colors.bold + colors.UNDERLINE + colors.fg.lightblue + "WELCOME TO MODBUS MASTER SIMULATOR" + colors.reset
        banner = '''

                    Version: 0.1 
                    Author: @ibaimc24 
                    Last updated: 09-08-2018

                    ''' + colors.reset
        print(title + colors.fg.lightblue + banner)


class UserInput:
    warning = '\t\t[' + colors.bold + colors.fg.yellow + '*' + colors.reset + '] '
    intro = '\t\t[' + colors.bold + colors.fg.green + '*' + colors.reset + '] '

    type = {

    }

    @staticmethod
    def command_input(propmt):
        return input(propmt).lower()

    @staticmethod
    def value_input(value_name, type, default=None, required=False):
        # TODO: show default value between parenthesis.
        if default or default == 0:
            value_name = value_name + ' (%s):' % str(default)
        else:
            value_name = value_name + ': '
        while True:
            try:
                inp = input(UserInput.warning + value_name)
                if not inp and not required:
                    return default
                elif not inp and required:
                    print(colors.fg.red + "\t\tThis value is mandatory." + colors.reset)
                else:
                    if type is bool and (inp != '1' and inp != '0'):
                        print(colors.fg.red + "\t\tMust be boolean (0/1)" + colors.reset)
                    elif type is bool:
                        return type(int(inp))
                    else:
                        return type(inp)

            except ValueError:
                print(colors.fg.red + "\t\tMust be integer." + colors.reset)
