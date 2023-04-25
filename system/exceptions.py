
class MasterError(Exception):

    def __init__(self, msg="Internal Error"):
        Exception.__init__(self)
        self.message = msg


class SendingDataError(MasterError):

    def __init__(self):
        MasterError.__init__(self, "No data to send")


class ModbusException(Exception):

    def __init__(self, message, exception_code=1):
        # Call the base class constructor with the parameters it needs
        super().__init__(message + ". ExceptionCode " + str(exception_code))
        self.exception_code = exception_code
        self.message = "Modbus Generic Exception"


class InvalidFunctionCode01(ModbusException):

    def __init__(self, function_code):
        super().__init__("Invalid Function Code", function_code)
        self.exception_code = 1
        self.message = "Invalid Function Code %d" % function_code


class InvalidDataAddress02(ModbusException):

    def __init__(self):
        super().__init__("Invalid Function Code", 2)
        self.exception_code = 2
        self.message = "Invalid Data Code"


class InvalidDataValue03(ModbusException):

    def __init__(self):
        super().__init__("Invalid Data Value", 3)
        self.exception_code = 3
        self.message = "Invalid Data Value"


class SlaveDeviceFailure(ModbusException):

    def __init__(self, msg=' '):
        super().__init__("Invalid Data Value", 4)
        self.exception_code = 4
        self.message = "Internal Error: %s" % msg


class SlaveException(Exception):

    def __init__(self, message):
        super().__init__(self, 'SlaveException: %s' % message)
