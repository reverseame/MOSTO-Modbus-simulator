# READ COILS (0x01):

READ_COILS_Q = b'\x00\x00\x00\x00\x00\x06\x00\x01\x00\x00\x00\x06'
READ_COILS_R = b'\x00\x00\x00\x00\x00\x04\x00\x01\x01'

# READ DISCRETE INPUTS  (0x02)
READ_DISCRETE_INPUTS_Q = b'\x00\x00\x00\x00\x00\x06\x00\x02\x00\x00\x00\x06'
READ_DISCRETE_INPUTS_R = b'\x00\x00\x00\x00\x00\x04\x00\x02\x01\x01'

# RESQUEST  (0x03)
READ_HOLDING_REGISTERS_Q = b'\x00\x00\x00\x00\x00\x06\x00\x03\x00\x6B\x00\x03'
READ_HOLDING_REGISTERS_R = b'\x00\x00\x00\x00\x00\x08\x00\x03\x06\x02\x2B\x00\x00\x00\x64'

# (0x04)
READ_INPUT_REGISTERS_Q = b'\x00\x00\x00\x00\x00\x06\x00\x04\x00\x08\x00\x01'
READ_INPUT_REGISTERS_R = b'\x00\x00\x00\x00\x00\x05\x00\x04\x02\x00\x0A'

# (0x05)
WRITE_SINGLE_COIL_Q = b'\x00\x00\x00\x00\x00\x06\x00\x05\x00\xAC\xFF\x00'
WRITE_SINGLE_COIL_R = b'\x00\x00\x00\x00\x00\x06\x00\x05\x00\xAC\xFF\x00'

# (0x06)
WRITE_SINGLE_REGISTER_Q = b'\x00\x00\x00\x00\x00\x06\x00\x06\x00\x01\x00\x03'
WRITE_SINGLE_REGISTER_R = b'\x00\x00\x00\x00\x00\x06\x00\x06\x00\x01\x00\x03'

# (0x07)
READ_EXCEPTION_STATUS_Q = b'\x00\x00\x00\x00\x00\x02\x00\x07'
READ_EXCEPTION_STATUS_R = b'\x00\x00\x00\x00\x00\x02\x00\x07\x6D'

# (0x08) - Return Query data (00) "echo"
DIAGNOSTICS_Q = b'\x00\x00\x00\x00\x00\x06\x00\x08\x00\x00\x0A\x06'
DIAGNOSTICS_R = b'\x00\x00\x00\x00\x00\x06\x00\x08\x00\x00\x0A\x06'
# ...


# (0x0B)
GET_COMM_EVENT_COUNTER_Q = b'\x00\x00\x00\x00\x00\x02\x00\x0B'
GET_COMM_EVENT_COUNTER_R = b'\x00\x00\x00\x00\x00\x06\x00\x0B\xFF\xFF\x01\x08'

# (0x0C)
GET_COMM_EVENT_LOG_Q = b'\x00\x00\x00\x00\x00\x02\x00\x0C'
GET_COMM_EVENT_LOG_R = b'\x00\x00\x00\x00\x00\x0B\x00\x0C\x08\x00\x00\x01\x08\x01\x21\x20\x00'

# (0x0F)
WRITE_MULTIPLE_COILS_Q = b'\x00\x00\x00\x00\x00\x08\x00\x0F\x00\x00\x00\x06\x01\x00\x01'  # DONE
WRITE_MULTIPLE_COILS_R = b'\x00\x00\x00\x00\x00\x06\x00\x0F\x00\x00\x00\x06'  # DONE


# WRITE MULTIPLE REGISTERS  (0x10)
WRITE_MULTIPLE_REGISTERS_Q = b'\x00\x00\x00\x00\x00\x0B\x00\x10\x00\x01\x00\x02\x04\x00\x0A\x01\x02'
WRITE_MULTIPLE_REGISTERS_R = b'\x00\x00\x00\x00\x00\x06\x00\x10\x00\x01\x00\x02'

# (0x11)
REPORT_SERVER_ID_Q = b'\x00\x00\x00\x00\x00\x02\x00\x11'
# ?

# (0x14)
READ_FILE_RECORD_Q = b'\x00\x00\x00\x00\x00\x0A\x00\x14\x06\x06\x00\x04\x00\x01\x00\x02'

# (0x15)
WRITE_FILE_RECORD_Q = b'\x00\x00\x00\x00\x00\x08\x00\x15\x05\x06\x00\x04\x00\x07'

# (0x16)
MASK_WRITE_REGISTER_Q = b'\x00\x00\x00\x00\x00\x08\x00\x16\x00\x04\x00\xF2\x00\x25'

# (0x17)
# READ_WRITE_MULTIPLE_REGISTERS_Q = b'\x00\x00\x00\x00\x00\x17\x00\x01\x00\x00\x00\x06'

# (0x18)
READ_FIFO_QUEUE_Q = b'\x00\x00\x00\x00\x00\x04\x00\x18\x04\xDE'

# (0x2B)
ENCAPSULATED_INTERFACE_TRANSPORT_Q = b'\x00\x00\x00\x00\x00\x05\x00\x2B\x0E\x01\x00'
# READ_DEVICE_IDENTIFICATION_Q = b'\x00\x00\x00\x00\x00\x06\x00\x0E\x00\x00\x00\x06'


def code(dec):
    if dec == 1:
        return READ_COILS_Q
    elif dec == 2:
        return READ_DISCRETE_INPUTS_Q
    elif dec == 3:
        return READ_HOLDING_REGISTERS_Q
    elif dec == 4:
        return READ_INPUT_REGISTERS_Q
    elif dec == 5:
        return WRITE_SINGLE_COIL_Q
    elif dec == 6:
        return WRITE_SINGLE_REGISTER_Q
    elif dec == 7:
        return READ_EXCEPTION_STATUS_Q
    elif dec == 8:
        return DIAGNOSTICS_Q
    elif dec == 11:
        return GET_COMM_EVENT_COUNTER_Q
    elif dec == 12:
        return GET_COMM_EVENT_LOG_Q
    elif dec == 15:
        return WRITE_MULTIPLE_COILS_Q
    elif dec == 16:
        return WRITE_MULTIPLE_REGISTERS_Q
    elif dec == 17:
        return REPORT_SERVER_ID_Q
    elif dec == 20:
        return READ_FILE_RECORD_Q
    elif dec == 21:
        return WRITE_FILE_RECORD_Q
    elif dec == 22:
        return MASK_WRITE_REGISTER_Q
    elif dec == 43:
        return ENCAPSULATED_INTERFACE_TRANSPORT_Q

    else:
        raise Exception("CodeError: invalid Modbus function code. Doesn't exist or it is not implemented.")
