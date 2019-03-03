from threading import Thread
import threading
from ModbusMaster.system.utils import Utilities, UserOutput
from ModbusMaster.system.exceptions import *
from time import sleep
from ModbusMaster.protocol.modbus import *
import random
from bitarray import bitarray

import datetime


class Master(Thread):

    def __init__(self, configuration):
        Thread.__init__(self)
        self.Configuration = configuration
        self.Active = True

        self.last_item = None
        self.bursts_handler = BurstHandler(configuration.Bursts, configuration.Functions)

    def run(self):
        # self.Configuration.show_from_master()
        log = Logger()
        tic = datetime.datetime.now()
        try:
            cnx = Utilities.create_connection(self.Configuration.SlaveAddr, self.Configuration.SlavePort, log)
            if not cnx:
                self.Active = False
            while self.Active:
                pkt = self.create_packet()
                toc = datetime.datetime.now()
                if not pkt:
                    self.Active = False
                else:
                    # TODO: user defined timeout
                    timeout = 2

                    self.bursts_handler.wait_delay(tic, toc)
                    tic = datetime.datetime.now()
                    ans = cnx.sr1(pkt, timeout=timeout, verbose=0)
                    if ans:
                        # Nothing to do with response
                        pass

        except SendingDataError as ex:
            log.write("Sending Data Error. %s. Closing the program." % str(ex.message))
            self.Active = False
        except Exception as ex:
            UserOutput.response_output("Exception ocurred: %s" %str(ex))
            if not log:
                log.write("Internal error. %s. Closing the program." % str(ex))
                self.Active = False
        log.close()

    def create_packet(self):
        func_item = self.bursts_handler.get_next_packet_props()
        pkt = None
        if func_item and func_item[3]:
            # TODO: Check funcCode to create specific packet
            # Read Coils
            if func_item[0] == 1:
                pkt = ModbusADU() / ModbusPDU01ReadCoils(funcCode=int(func_item[0]), startAddr=int(func_item[3][0]),
                                                         quantity=int(func_item[3][1]))
            # Read Discrete Inputs
            elif func_item[0] == 2:
                pkt = ModbusADU() / ModbusPDU02ReadDiscreteInputs(funcCode=int(func_item[0]),
                                                                  startAddr=int(func_item[3][0]),
                                                                  quantity=int(func_item[3][1]))

            # Read Holding Registers
            elif func_item[0] == 3:
                pkt = ModbusADU() / ModbusPDU03ReadHoldingRegisters(funcCode=int(func_item[0]),
                                                                    startAddr=int(func_item[3][0]),
                                                                    quantity=int(func_item[3][1]))

            # Write Multiple Coils
            elif func_item[0] == 15:
                pkt = ModbusADU() / ModbusPDU0FWriteMultipleCoils(funcCode=int(func_item[0]),
                                                                  startingAddr=int(func_item[3][0]),
                                                                  quantityOutput=int(func_item[3][1]),
                                                                  outputsValue=int(bitarray(func_item[3][2]).to01(), 2))

            elif func_item[0] == 4:
                pkt = ModbusADU() / ModbusPDU04ReadInputRegisters(funcCode=int(func_item[0]),
                                                                  startAddr=int(func_item[3][0]),
                                                                  quantity=int(func_item[3][1]))
            else:
                UserOutput.response_output("Bad packet", 'error')
                pkt = None

            pkt.len = len(pkt.payload) + 1
        return pkt

    def stop(self):
        # TODO: Make in mutual exclusion
        self.Active = False


class BurstHandler:

    def __init__(self, bursts, functions):
        if not bursts:
            UserOutput.response_output("No functions defined to send.", type='exception')
            raise SendingDataError()
        # Array of ['index', 'funcCode', 'latency', 'variance', 'fieldsValues[]']
        self.functions = functions

        # Array of ["burstIndex", "fcodeIndex", "delay", "Variance"]
        self.bursts = bursts

        self.last_burst_item = []

    def get_next_packet_props(self):
        if not self.last_burst_item:
            # first transmission. Don't need delay.
            next_burst_item = self.bursts[0]
            fcode_indx = next_burst_item[1]
            next_item = self.functions[fcode_indx][1:]
            # update for next iteration
            self.last_burst_item = next_burst_item

        else:
            n_index = self.bursts.index(self.last_burst_item)+1
            if n_index >= len(self.bursts):
                n_index = 0
            next_burst_item = self.bursts[n_index]
            fcode_indx = next_burst_item[1]
            next_item = self.functions[fcode_indx][1:]
            # update for next iteration
            self.last_burst_item = next_burst_item
        return next_item

    def wait_delay(self, tic, toc):
        rtt = (toc - tic).total_seconds()

        # ["burstIndex", "fcodeIndex", "delay", "Variance"]
        delay = self.last_burst_item[2]
        variance = self.last_burst_item[3]
        wait_time = delay + random.uniform(-variance, variance)
        if rtt < wait_time:
            sleep(wait_time - rtt)


class Logger:

    def __init__(self):
        self.__create_log_file()
        self.fp = Logger.__create_log_file()

    def write(self, msg):
        self.fp.write(msg + "\n")

    def close(self):
        self.fp.write("Finished at %s \n" % str(datetime.datetime.now()))
        self.fp.close()
        UserOutput.response_output("Master Stopped", type='info')

    @staticmethod
    def __add_header(fp):
        fp.write("Started at %s\n" % str(datetime.datetime.now()))
        fp.write("Thread ID: %s\n" % str(threading.current_thread().ident))

    @staticmethod
    def __create_log_file():
        filename = str(datetime.datetime.now()).lstrip("-").replace(":", "_").replace(" ", "-").split(".")[0] + ".log"
        file_path = "./log/" + filename
        fp = open(file_path, "w+")
        Logger.__add_header(fp)
        return fp
