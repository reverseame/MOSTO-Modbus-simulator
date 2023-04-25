# READ COILS (0x01):

_READ_COILS = 0x01
READ_COILS_Q = b'\x00\x00\x00\x00\x00\x06\x00\x01\x00\x00\x00\x06'
READ_COILS_R = b'\x00\x00\x00\x00\x00\x04\x00\x01\x01'

# READ DISCRETE INPUTS  (0x02)
_READ_DISCRETE_INPUTS  = 0x02
READ_DISCRETE_INPUTS_Q = b'\x00\x00\x00\x00\x00\x06\x00\x02\x00\x00\x00\x06'
READ_DISCRETE_INPUTS_R = b'\x00\x00\x00\x00\x00\x04\x00\x02\x01\x01'

# READ MULTIPLE HOLDING REGISTERS  (0x03)
_READ_MULTIPLE_HOLDING_REGISTERS = 0x03
READ_HOLDING_REGISTERS_Q = b'\x00\x00\x00\x00\x00\x06\x00\x03\x00\x6B\x00\x03'
READ_HOLDING_REGISTERS_R = b'\x00\x00\x00\x00\x00\x08\x00\x03\x06\x02\x2B\x00\x00\x00\x64'

# READ INPUT REGISTERS (0x04)
_READ_INPUT_REGISTERS = 0x04
READ_INPUT_REGISTERS_Q = b'\x00\x00\x00\x00\x00\x06\x00\x04\x00\x08\x00\x01'
READ_INPUT_REGISTERS_R = b'\x00\x00\x00\x00\x00\x05\x00\x04\x02\x00\x0A'

# WRITE SINGLE COIL (0x05)
_WRITE_SINGLE_COIL = 0x05
WRITE_SINGLE_COIL_Q = b'\x00\x00\x00\x00\x00\x06\x00\x05\x00\xAC\xFF\x00'
WRITE_SINGLE_COIL_R = b'\x00\x00\x00\x00\x00\x06\x00\x05\x00\xAC\xFF\x00'

# WRITE SINGLE HOLDING REGISTER  (0x06)
_WRITE_SINGLE_HOLDING_REGISTER = 0x06
WRITE_SINGLE_REGISTER_Q = b'\x00\x00\x00\x00\x00\x06\x00\x06\x00\x01\x00\x03'
WRITE_SINGLE_REGISTER_R = b'\x00\x00\x00\x00\x00\x06\x00\x06\x00\x01\x00\x03'

# READ EXCEPTION STATUS (0x07)
_READ_EXCEPTION_STATUS = 0x07
READ_EXCEPTION_STATUS_Q = b'\x00\x00\x00\x00\x00\x02\x00\x07'
READ_EXCEPTION_STATUS_R = b'\x00\x00\x00\x00\x00\x02\x00\x07\x6D'

# DIAGNOSTICS (0x08) - Return Query data (00) "echo"
_DIAGNOSTICS = 0x08
DIAGNOSTICS_Q = b'\x00\x00\x00\x00\x00\x06\x00\x08\x00\x00\x0A\x06'
DIAGNOSTICS_R = b'\x00\x00\x00\x00\x00\x06\x00\x08\x00\x00\x0A\x06'
# ...

# ...
# GET COMM EVENT COUNTER (0x0B)
_GET_COMM_EVENT_COUNTER  = 0x0B
GET_COMM_EVENT_COUNTER_Q = b'\x00\x00\x00\x00\x00\x02\x00\x0B'
GET_COMM_EVENT_COUNTER_R = b'\x00\x00\x00\x00\x00\x06\x00\x0B\xFF\xFF\x01\x08'

# GET COMM EVENT LOG (0x0C)
_GET_COMM_EVENT_LOG  = 0x0C
GET_COMM_EVENT_LOG_Q = b'\x00\x00\x00\x00\x00\x02\x00\x0C'
GET_COMM_EVENT_LOG_R = b'\x00\x00\x00\x00\x00\x0B\x00\x0C\x08\x00\x00\x01\x08\x01\x21\x20\x00'

# WRITE MULTIPLE COILS (0x0F)
_WRITE_MULTIPLE_COILS = 0x0F
WRITE_MULTIPLE_COILS_Q = b'\x00\x00\x00\x00\x00\x08\x00\x0F\x00\x00\x00\x06\x01\x00\x01'  # DONE
WRITE_MULTIPLE_COILS_R = b'\x00\x00\x00\x00\x00\x06\x00\x0F\x00\x00\x00\x06'  # DONE


# WRITE MULTIPLE REGISTERS  (0x10)
_WRITE_MULTIPLE_REGISTERS  = 0x10
WRITE_MULTIPLE_REGISTERS_Q = b'\x00\x00\x00\x00\x00\x0B\x00\x10\x00\x01\x00\x02\x04\x00\x0A\x01\x02'
WRITE_MULTIPLE_REGISTERS_R = b'\x00\x00\x00\x00\x00\x06\x00\x10\x00\x01\x00\x02'

# REPORT SERVER ID (0x11)
_REPORT_SERVER_ID  = 0x11
REPORT_SERVER_ID_Q = b'\x00\x00\x00\x00\x00\x02\x00\x11'
# REPORT_SERVER_ID_R XXX TBD

# READ FILE RECORD (0x14)
_READ_FILE_RECORD  = 0x14
READ_FILE_RECORD_Q = b'\x00\x00\x00\x00\x00\x0A\x00\x14\x06\x06\x00\x04\x00\x01\x00\x02'
# READ_FILE_RECORD_Q XXX TBD

# WRITE FILE (0x15)
_WRITE_FILE_RECORD  = 0x15
WRITE_FILE_RECORD_Q = b'\x00\x00\x00\x00\x00\x08\x00\x15\x05\x06\x00\x04\x00\x07'
# WRITE_FILE_RECORD_Q XXX TBD

# MASK WRITE REGISTER (0x16)
_MASK_WRITE_REGISTER  = 0x16
MASK_WRITE_REGISTER_Q = b'\x00\x00\x00\x00\x00\x08\x00\x16\x00\x04\x00\xF2\x00\x25'
# MASK_WRITE_REGISTER_Q XXX TBD

# READ WRITE MULTIPLE REGISTERS (0x17)
_READ_WRITE_MULTIPLE_REGISTERS = 0x17
# READ_WRITE_MULTIPLE_REGISTERS_Q = b'\x00\x00\x00\x00\x00\x17\x00\x01\x00\x00\x00\x06'
# READ_WRITE_MULTIPLE_REGISTERS_R XXX TBD

# READ FIFO QUEUE (0x18)
_READ_FIFO_QUEUE  = 0x18
READ_FIFO_QUEUE_Q = b'\x00\x00\x00\x00\x00\x04\x00\x18\x04\xDE'
# READ_FIFO_QUEUE_R XXX TBD

# ENCAPSULATED INTERFACE TRANSPORT (0x2B)
_ENCAPSULATED_INTERFACE_TRANSPORT  = 0x2B
ENCAPSULATED_INTERFACE_TRANSPORT_Q = b'\x00\x00\x00\x00\x00\x05\x00\x2B\x0E\x01\x00'
# ENCAPSULATED_INTERFACE_TRANSPORT_R XXX TBD

_RAW_QUERIES = [None, # Leave this in line 100, more comfortable
READ_COILS_Q,
READ_DISCRETE_INPUTS_Q,
READ_HOLDING_REGISTERS_Q,
READ_INPUT_REGISTERS_Q,
WRITE_SINGLE_COIL_Q,
WRITE_SINGLE_REGISTER_Q,
READ_EXCEPTION_STATUS_Q,
DIAGNOSTICS_Q,
None,
None,
GET_COMM_EVENT_COUNTER_Q,
GET_COMM_EVENT_LOG_Q,
None,
None,
WRITE_MULTIPLE_COILS_Q,
WRITE_MULTIPLE_REGISTERS_Q,
REPORT_SERVER_ID_Q,
None,
None,
READ_FILE_RECORD_Q,
WRITE_FILE_RECORD_Q,
MASK_WRITE_REGISTER_Q,
None,
None,
None,
None,
None,
None,
None,
None,
None,
None,
None,
None,
None,
None,
None,
None,
None,
None,
None,
None,
ENCAPSULATED_INTERFACE_TRANSPORT_Q
]

FUNCTION_CODE_NAMES = {
    _READ_COILS: "Read Coils",
    _READ_DISCRETE_INPUTS: "Read Discrete Inputs",
    _READ_MULTIPLE_HOLDING_REGISTERS: "Read Multiple Holding Registers",
    _READ_INPUT_REGISTERS: "Read Input Registers",
    _WRITE_SINGLE_COIL: "Write Single Coil",
    _WRITE_SINGLE_HOLDING_REGISTER: "Write Single Holding Register",
    _READ_EXCEPTION_STATUS: "Read Exception Status",
    _DIAGNOSTICS: "Diagnostic",
    _GET_COMM_EVENT_COUNTER: "Get Comm Event Counter",
    _GET_COMM_EVENT_LOG: "Get Comm Event Log",
    _WRITE_MULTIPLE_COILS: "Write Multiple Coils",
    _WRITE_MULTIPLE_REGISTERS: "Write Multiple Holding Registers",
    _REPORT_SERVER_ID: "Report Slave ID",
    _READ_FILE_RECORD: "Read File Record",
    _WRITE_FILE_RECORD: "Write File Record",
    _MASK_WRITE_REGISTER: "Mask Write Register",
    _READ_WRITE_MULTIPLE_REGISTERS: "Read/Write Multiple Registers",
    _READ_FIFO_QUEUE: "Read FIFO Queue",
    _RAW_QUERIES: "Read Device Identification"
}

_MODBUS_EXCEPTIONS = {
    1: "Illegal function",
    2: "Illegal data address",
    3: "Illegal data value",
    4: "Slave device failure",
    5: "Acknowledge",
    6: "Slave device busy",
    8: "Memory parity error",
    10: "Gateway path unavailable",
    11: "Gateway target device failed to respond"
}
