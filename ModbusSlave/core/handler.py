from threading import Thread
import random
from time import sleep
from ModbusSlave.core.utils import *
from ModbusSlave.core.protocols import Transaction


class Handler(Thread):

    SleepDelay = 0.5214

    def __init__(self, bit_table1, bit_table2, register_table1, register_table2):
        Thread.__init__(self)
        # Data to be handled
        self.bit_table1 = bit_table1
        self.bit_table2 = bit_table2
        self.register_table1 = register_table1
        self.register_table2 = register_table2

    def run(self):
        random.seed()
        while True:
            # Select random table
            table = random.choice([self.bit_table1, self.bit_table2, self.register_table1, self.register_table2])

            # Select random block
            if not table.Blocks:
                continue
            block = random.choice(table.Blocks)

            # Select random address from block
            addr = random.randrange(block[0], block[1], 1)

            # Write random bit value in table
            if isinstance(table, RegisterTable):
                value = random.randrange(0, 65535, 1)
                Transaction.write_handler_int(table, addr, value)
            else:
                Transaction.write_bit(table, addr, random.choice([0, 65280]))

            sleep(self.SleepDelay)
