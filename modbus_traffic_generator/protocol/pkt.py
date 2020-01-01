

class Modbus(object):

    def __init__(self, code):
        to_modify = bytearray(code)
        self.raw = bytes(to_modify)

    def raw(self):
        return self.raw
