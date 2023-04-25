
import protocol as pt
from protocol.codes import *

class Modbus(object):

    def __init__(self, fn_code):
        self.fn_code = fn_code
        self._code = pt.codes._RAW_QUERIES[fn_code]
        self.raw = bytes(bytearray(self._code))

    def raw(self):
        return self.raw
