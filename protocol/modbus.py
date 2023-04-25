from scapy.all import *
import binascii
from system.exceptions import *
from bitarray import bitarray
from threading import Lock

# own constant definitions
transId = 1
connection = None
timeout = 5
modport = 502

function_code_name = {
    1: "Read Coils",
    2: "Read Discrete Inputs",
    3: "Read Multiple Holding Registers",
    4: "Read Input Registers",
    5: "Write Single Coil",
    6: "Write Single Holding Register",
    7: "Read Exception Status",
    8: "Diagnostic",
    11: "Get Com Event Counter",
    12: "Get Com Event Log",
    15: "Write Multiple Coils",
    16: "Write Multiple Holding Registers",
    17: "Report Slave ID",
    20: "Read File Record",
    21: "Write File Record",
    22: "Mask Write Register",
    23: "Read/Write Multiple Registers",
    24: "Read FIFO Queue",
    43: "Read Device Identification"}

_modbus_exceptions = {
    1: "Illegal function",
    2: "Illegal data address",
    3: "Illegal data value",
    4: "Slave device failure",
    5: "Acknowledge",
    6: "Slave device busy",
    8: "Memory parity error",
    10: "Gateway path unavailable",
    11: "Gateway target device failed to respond"}

class Transaction:

    RegisterTypes = ['bit', 'register']
    Locker = Lock()

    @staticmethod
    def validate_function_code(supported_functions, requested_function):
        if requested_function in supported_functions:
            return True
        else:
            return False

    @staticmethod
    def validate_data_address(data_mask, start_addr, quantity):
        # Validatione permissions of the request
        # Exception 02
        return data_mask.can_access(start_addr, quantity)

    @staticmethod
    def validate_data_value(quantity):
        # validate quantity of outputs
        # Exception 03
        if quantity < 1 or quantity > 2000:
            return False
        else:
            return True

    @staticmethod
    def read_block(datablock, start_addr, quantity, register_type='bit'):
        if register_type not in Transaction.RegisterTypes:
            raise TypeError("Register type must be one of " + str(Transaction.RegisterTypes))

        # response array
        data = []

        # bits internal array
        bits = []
        counter = 1

        if register_type == 'bit':
            n_bits = quantity
            max_counter = 8
        else:
            n_bits = quantity * 16
            max_counter = 16
        # Read all requested bits and storage in internal array 'bits'
        Transaction.Locker.acquire()
        for i in range(start_addr, start_addr + n_bits):
            bits.append(datablock.read(i))
            if counter is max_counter:  # When got 8 bits, create an integer and append to response
                data.append(int(bitarray(bits).to01(), 2))
                # Restart internal variables
                bits = []
                counter = 1
            counter += 1
        Transaction.Locker.release()
        if register_type == 'bit':
            data = Transaction.add_padding(data, bits)
        return data

    @staticmethod
    def read(datablock, start_addr, quantity):
        response = []
        remaining_bits = quantity
        offset = start_addr

        Transaction.Locker.acquire()
        while remaining_bits != 0:
            if remaining_bits // 8 > 0:
                read_from_data = datablock.read_uint8(offset)
                response.append(read_from_data)
                remaining_bits -= 8
                offset += 8
            else:
                response.append(datablock.read_x(offset, remaining_bits))
                remaining_bits = 0
        Transaction.Locker.release()
        return response

    @staticmethod
    def write_handler_int(datablock, addr, value):
        Transaction.Locker.acquire()
        datablock.write(addr, value)
        Transaction.Locker.release()


    @staticmethod
    def add_padding(data, bits):
        """
        Adds to data 'bits' containing values with '0' padding
        :param data:
        :param bits:
        :return:
        """
        # 0 Padding to 8 multiple
        while len(bits) % 8 != 0:
            bits.append(False)

        # Append padding byte
        data.append(int(bitarray(bits).to01(), 2))
        return data

    @staticmethod
    def write_register(datablock, addr, value):
        """
        :param datablock: bitarray of data to be overwritten
        :param value: 16 bit integer
        :return: Nothing
        """
        Transaction.Locker.acquire()
        datablock.write(addr, value)
        Transaction.Locker.release()
        pass

    @staticmethod
    def write_bit(datablock, address, value):
        if value not in [0, 65280]:
            raise ValueError("Writting values must be 0x0000 or 0xFF00 for coils.")
        Transaction.Locker.acquire()
        datablock.write(address, value == 65280)
        Transaction.Locker.release()

    @staticmethod
    def write_multiple_bits(datablock, start_addr, quantity, values):
        written_bits = 0
        offset = start_addr
        Transaction.Locker.acquire()
        for indx, value in enumerate(values):
            # Swap output value byte
            in_little = bitarray(endian='little')
            in_little.frombytes(value.to_bytes(1, byteorder='little'))
            for bit in range(8):
                datablock.write(offset, int(in_little[bit]))
                offset += 1
                written_bits += 1
                if written_bits == quantity:
                    Transaction.Locker.release()
                    return
        Transaction.Locker.release()

class ModbusADU(Packet):

    name = "ModbusADU"
    fields_desc = [

        # needs to be unique
        XShortField("transId", 0x0000),

        # needs to be zero (Modbus)
        XShortField("protoId", 0x0000),

        # is calculated with payload
        XShortField("len", None),

        # 0xFF or 0x00 should be used for Modbus over TCP/IP
        XByteField("unitId", 0x0)
    ]

    def guess_payload_class(self, payload):
        # First byte of the payload is Modbus function code (254 available function codes)
        data = binascii.hexlify(bytes(payload))
        function_code = int(data[0:2], 16)

        if function_code == 0x01:
            return ModbusPDU01ReadCoils

        elif function_code == 0x02:
            return ModbusPDU02ReadDiscreteInputs

        elif function_code == 0x03:
            return ModbusPDU03ReadHoldingRegisters

        elif function_code == 0x04:
            return ModbusPDU04ReadInputRegisters

        elif function_code == 0x05:
            return ModbusPDU05WriteSingleCoil

        elif function_code == 0x06:
            return ModbusPDU06WriteSingleRegister

        elif function_code == 0x07:
            return ModbusPDU07ReadExceptionStatus

        elif function_code == 0x0F:
            return ModbusPDU0FWriteMultipleCoils

        elif function_code == 0x10:
            return ModbusPDU10WriteMultipleRegisters

        elif function_code == 0x11:
            return ModbusPDU11ReportSlaveId
        else:
            return Packet.guess_payload_class(self, payload)


# Can be used to replace all Modbus read
class ModbusPDUReadGeneric(Packet):
    name = "Read Generic"
    fields_desc = [
        XByteField("funcCode", 0x01),
        XShortField("startAddr", 0x0000),
        XShortField("quantity", 0x0001)
    ]


# 0x01 - Read Coils
class ModbusPDU01ReadCoils(Packet):
    name = "Read Coils Request"
    fields_desc = [
        XByteField("funcCode", 0x01),
        # 0x0000 to 0xFFFF
        XShortField("startAddr", 0x0000),
        XShortField("quantity", 0x0001)
    ]

    def process(self, datablock, coilsmask):
        # Read Coils State Diagram:
        if not Transaction.validate_data_value(self.quantity):
            raise InvalidDataValue03()

        if not Transaction.validate_data_address(coilsmask, self.startAddr, self.quantity):
            raise InvalidDataAddress02()

        return self.execute(datablock)

    def execute(self, datablock):
        try:
            result = Transaction.read(datablock=datablock, start_addr=self.startAddr, quantity=self.quantity)
        except Exception as ex:
            raise SlaveDeviceFailure(str(ex))
        return result


# 0x02 - Read Discrete Inputs
class ModbusPDU02ReadDiscreteInputs(Packet):
    name = "Read Discrete Inputs"
    fields_desc = [
        XByteField("funcCode", 0x02),
        XShortField("startAddr", 0x0000),
        XShortField("quantity", 0x0001)]

    def process(self, datablock, discrete_inputs_mask):
        # TODO: define
        # Read DiscreteInputs Diagram:
        if not Transaction.validate_data_value(self.quantity):
            raise InvalidDataValue03()

        if not Transaction.validate_data_address(discrete_inputs_mask, self.startAddr, self.quantity):
            raise InvalidDataAddress02()

        return self.execute(datablock)

    def execute(self, datablock):
        try:
            result = Transaction.read(datablock=datablock, start_addr=self.startAddr, quantity=self.quantity)
        except Exception as ex:
            raise SlaveDeviceFailure(str(ex))
        return result


# 0x03 - Read Holding Registers
# TODO: Test
class ModbusPDU03ReadHoldingRegisters(Packet):
    name = "Read Holding Registers"
    fields_desc = [
        XByteField("funcCode", 0x03),
        XShortField("startAddr", 0x0001),
        XShortField("quantity", 0x0002)]

    def process(self, datablock, holding_registers_mask):
        if not Transaction.validate_data_value(self.quantity):
            raise InvalidDataValue03()

        if self.startAddr >= 16 and self.startAddr <= 27:
            print("Start Address: %s\nQuantity: %s\n")
        if not Transaction.validate_data_address(holding_registers_mask, self.startAddr, self.quantity):
            raise InvalidDataAddress02()

        return self.execute(datablock)

    def execute(self, datablock):
        return Transaction.read_block(datablock=datablock, start_addr=self.startAddr,
                                      quantity=self.quantity, register_type='register')


# 0x04 - Read Input Registers
# TODO: Test
class ModbusPDU04ReadInputRegisters(Packet):
    name = "Read Input Registers"
    fields_desc = [
        XByteField("funcCode", 0x04),
        XShortField("startAddr", 0x0000),
        XShortField("quantity", 0x0001)]

    def process(self, datablock, input_registers_mask):
        if not Transaction.validate_data_value(self.quantity):
            raise InvalidDataValue03()

        if not Transaction.validate_data_address(input_registers_mask, self.startAddr, self.quantity):
            raise InvalidDataAddress02()

        return self.execute(datablock)

    def execute(self, datablock):
        return Transaction.read_block(datablock=datablock, start_addr=self.startAddr,
                                      quantity=self.quantity, register_type='register')


# 0x05 - Write Single Coil
# TODO: Test
class ModbusPDU05WriteSingleCoil(Packet):

    ValidOutputValues = [0x0000, 0xFF00]

    name = "Write Single Coil"
    fields_desc = [
        XByteField("funcCode", 0x05),
        XShortField("outputAddr", 0x0000),   # from 0x0000 to 0xFFFF
        XShortField("outputValue", 0x0000)]  # 0x0000 == Off, 0xFF00 == On

    def process(self, datablock, coils_mask):
        """
        If proccesing is OK, nothing returns, else, an exception is raised
        :param datablock:
        :param coils_mask:
        :return:
        """
        # Validate OutputValue
        if self.outputValue not in ModbusPDU05WriteSingleCoil.ValidOutputValues:
            raise InvalidDataValue03()

        if not Transaction.validate_data_address(coils_mask, start_addr=self.outputAddr, quantity=1):
            raise InvalidDataAddress02()

        self.execute(datablock)

    def execute(self, datablock):
        try:
            Transaction.write_bit(datablock, address=self.outputAddr, value=self.outputValue)
        except Exception as ex:
            raise SlaveDeviceFailure(str(ex))


# 0x06 - Write Single Register
# TODO: Test
class ModbusPDU06WriteSingleRegister(Packet):
    name = "Write Single Register"
    fields_desc = [
        XByteField("funcCode", 0x06),
        XShortField("registerAddr", 0x0000),
        XShortField("registerValue", 0x0000)]

    def process(self, datablock, holding_registers_mask):
        # Validate registerValue
        if self.registerValue > 65535:
            raise InvalidDataValue03()
        if not Transaction.validate_data_address(data_mask=holding_registers_mask, start_addr=self.outputAddr,
                                                 quantity=1):
            raise InvalidDataAddress02()
        self.execute(datablock)

    def execute(self, datablock):
        try:
            Transaction.write_register(datablock, self.registerAddr, self.registerValue)
        except Exception as ex:
            raise SlaveDeviceFailure(str(ex))


# 0x0F - Write Multiple Coils
# TODO: test
class ModbusPDU0FWriteMultipleCoils(Packet):
    name = "Write Multiple Coils"
    fields_desc = [
        XByteField("funcCode", 0x0F),
        XShortField("startingAddr", 0x0000),
        XShortField("quantityOutput", 0x0001),
        BitFieldLenField("byteCount", None, 8, count_of="outputsValue", adjust=lambda pkt, x:x),
        FieldListField("outputsValue", [0x00], XByteField("", 0x00), count_from=lambda pkt: pkt.byteCount)]

    def process(self, datablock, coils_mask):
        if not Transaction.validate_data_value(self.quantityOutput) and (len(self.outputsValue) + 1 != self.byteCount):
            raise InvalidDataValue03()

        if not Transaction.validate_data_address(data_mask=coils_mask, start_addr=self.startingAddr,
                                                 quantity=self.quantityOutput):
            raise InvalidDataAddress02()
        self.execute(datablock)

    def execute(self, datablock):
        #try:
        Transaction.write_multiple_bits(datablock=datablock, start_addr=self.startingAddr, quantity=self.quantityOutput,
                                        values=self.outputsValue)
        """
                    for indx, value in enumerate(self.outputsValue):
            # Swap output value byte
            in_little = bitarray(endian='little')
            in_little.frombytes(value.to_bytes(1, byteorder='little'))
            for bit in range(8):
                Transaction.write_bit(datablock=datablock, address=self.startAddr + indx*8 + bit,
                                      value=int(in_little[bit]))
        """

        #except Exception as ex:
        #    raise SlaveDeviceFailure(str(ex))


# 0x10 - Write Multiple Registers
class ModbusPDU10WriteMultipleRegisters(Packet):
    name = "Write Multiple Registers"
    fields_desc = [
        XByteField("funcCode", 0x10),
        XShortField("startingAddr", 0x0000),
        XShortField("quantityRegisters", 0x0001),
        BitFieldLenField("byteCount", None, 8, count_of="outputsValue", adjust=lambda pkt, x:x),
        FieldListField("outputsValue", [0x00], XByteField("", 0x00), count_from=lambda pkt: pkt.byteCount)]

    def process(self, datablock, coils_mask):
        # TODO:
        pass

    def execute(self):
        # TODO:
        pass


# ---------------- ANSWERS ---------------- #

class ModbusPDU01ReadCoilsAnswer(Packet):
    name = "Read Coils Answer"
    fields_desc = [
        XByteField("funcCode", 0x01),
        BitFieldLenField("byteCount", None, 8, count_of="coilStatus"),
        FieldListField("coilStatus", [0x00], ByteField("", 0x00), count_from=lambda pkt: pkt.byteCount)]


class ModbusPDU02ReadDiscreteInputsAnswer(Packet):
    name = "Read Discrete Inputs Answer"
    fields_desc = [
        XByteField("funcCode", 0x02),
        BitFieldLenField("byteCount", None, 8, count_of="inputStatus"),
        FieldListField("inputStatus", [0x00], ByteField("", 0x00), count_from=lambda pkt: pkt.byteCount)]


class ModbusPDU03ReadHoldingRegistersAnswer(Packet):
    name = "Read Holding Registers Answer"
    fields_desc = [
        XByteField("funcCode", 0x03),
        BitFieldLenField("byteCount", None, 8, count_of="registerVal"),
        FieldListField("registerVal", [0x00], ByteField("", 0x00), count_from=lambda pkt: pkt.byteCount)]


class ModbusPDU04ReadInputRegistersAnswer(Packet):
    name = "Read Input Registers Answer"
    fields_desc = [
        XByteField("funcCode", 0x04),
        BitFieldLenField("byteCount", None, 8, count_of="registerVal"),
        FieldListField("registerVal", [0x00], ByteField("", 0x00), count_from=lambda pkt: pkt.byteCount)]


class ModbusPDU05WriteSingleCoilAnswer(Packet):  # The answer is the same as the request if successful
    name = "Write Single Coil"
    fields_desc = [
        XByteField("funcCode", 0x05),
        XShortField("outputAddr", 0x0000),   # from 0x0000 to 0xFFFF
        XShortField("outputValue", 0x0000)]  # 0x0000 == Off, 0xFF00 == On


class ModbusPDU06WriteSingleRegisterAnswer(Packet):

    name = "Write Single Register Answer"
    fields_desc = [
        XByteField("funcCode", 0x06),
        XShortField("registerAddr", 0x0000),
        XShortField("registerValue", 0x0000)]


# 0x07 - Read Exception Status (Serial Line Only)
class ModbusPDU07ReadExceptionStatus(Packet):
    name = "Read Exception Status"
    fields_desc = [XByteField("funcCode", 0x07)]


class ModbusPDU07ReadExceptionStatusAnswer(Packet):
    name = "Read Exception Status Answer"
    fields_desc = [
        XByteField("funcCode", 0x07),
        XByteField("startingAddr", 0x00)]


class ModbusPDU0FWriteMultipleCoilsAnswer(Packet):
    name = "Write Multiple Coils Answer"
    fields_desc = [
        XByteField("funcCode", 0x0F),
        XShortField("startingAddr", 0x0000),
        XShortField("quantityOutput", 0x0001)]


class ModbusPDU10WriteMultipleRegistersAnswer(Packet):
    name = "Write Multiple Registers Answer"
    fields_desc = [
        XByteField("funcCode", 0x10),
        XShortField("startingAddr", 0x0000),
        XShortField("quantityRegisters", 0x0001)]


# 0x11 - Report Slave Id
class ModbusPDU11ReportSlaveId(Packet):
    name = "Report Slave Id"
    fields_desc = [XByteField("funcCode", 0x11)]


class ModbusPDU11ReportSlaveIdAnswer(Packet):
    name = "Report Slave Id Answer"
    fields_desc = [
        XByteField("funcCode", 0x11),
        BitFieldLenField("byteCount", None, 8, length_of="slaveId"),
        ConditionalField(StrLenField("slaveId", "", length_from=lambda pkt: pkt.byteCount),
                         lambda pkt: pkt.byteCount > 0),
        ConditionalField(XByteField("runIdicatorStatus", 0x00), lambda pkt: pkt.byteCount > 0)]


# ---------------- EXCEPTIONS ---------------- #


#class ModbusPDUIllegalFunctionException(Packet):
#    name = "Illegal Function Exception"
#    fields_desc = [
#        XByteField("funcCode", 0x80),
#       ByteEnumField("exceptCode", 1, _modbus_exceptions)
#    ]


class ModbusPDUGenericException(Packet):
    name = "Modbus Exception"
    fields_desc = [
        XByteField("funcCode", 0x80),
        XByteField("exceptCode", 0x00)
    ]