import socket
from protocol.pkt import Modbus
from datetime import datetime
import protocol as pt
import argparse
import time
import sys

## Default values

# Delay between sent packets in seconds
DELAY = 1/7.0
# Default type of burst
DEFAULT_BURST = 3
# Socket receiver buffer size in bytes
BUFFER_SIZE = 560
# Number of packets per burst (ppb)
N_PPB = 1000

def receive_data(_socket):
    tic = datetime.now()
    _data = _socket.recv(BUFFER_SIZE)
    toc = datetime.now()
    w8(tic, toc)
    return _data

def continuous(_socket, _modbus_pkt):
    for i in range(N_PPB):
        _socket.sendall(_modbus_pkt.raw)
        _data = receive_data(_socket)

def send_packet(_socket, _code, _n_ppb):
    # Create the corresponding Modbus packet
    _modbus_pkt = Modbus(_code)
        
    for i in range(_n_ppb):
        _socket.sendall(_modbus_pkt.raw)
        _data = receive_data(_socket)
        print(f"> (fn_code: {_code}) {i + 1}/{N_PPB} ...")


def bursts_of_main(_socket):
    for idx, _query in enumerate(pt.codes._RAW_QUERIES):
        if _query is None:
            continue

        send_packet(_socket, idx, N_PPB)
        # Only functions up to _WRITE_MULTIPLE_REGISTERS
        if idx == pt.codes._WRITE_MULTIPLE_REGISTERS:
            return

def one_of_each(_socket):

    _list = [pt.codes._READ_COILS, pt.codes._READ_DISCRETE_INPUTS, pt.codes._READ_MULTIPLE_HOLDING_REGISTERS, 
                 pt.codes._READ_INPUT_REGISTERS, pt.codes._WRITE_SINGLE_COIL, pt.codes._WRITE_MULTIPLE_REGISTERS
            ]

    for _code in _list:
        send_packet(_socket, _code, 1)

def w8(tic, toc):
    tdelta = (toc - tic).total_seconds()
    if tdelta < DELAY:
        time.sleep(DELAY - tdelta)


def interleaved(_socket, _codes):
    for i in range(N_PPB):
        for _code in _codes:
            _modbus_pkt = Modbus(_code)
            print(f"> (fn_code: {_code}) {i + 1}/{N_PPB} ...")
            _socket.sendall(_modbus_pkt.raw)
            _data = receive_data(_socket)
            if not _data:
                print("wait for response!!!!")

def connect_socket(_ip, _port):
    # TODO This can raise some exceptions, we need to check it 
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.connect((_ip, _port))
    print(f"Connection to {_ip}:{_port} successful  ...")
    return _socket

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MOSTO: generate a ModbusTCP traffic to specified host (addr:port)"
                                                 """
                                                 It builds Modbus packets with specified function codes and it
                                                 waits until the slave answers.
                                                 """
                                                 "The delay between sent packets can be set by -d option.")
    parser.add_argument("addr", help="Slave IP address", type=str)
    parser.add_argument("port", type=int, help="Slave TCP port", default=502)
    parser.add_argument("--burst", help=f"Specifies the type of burst (default {DEFAULT_BURST}): ", type=int, choices=[1, 2, 3, 4], default=DEFAULT_BURST)
    parser.add_argument("-d", "--delay", help=f"Specifies the delay between sent packets (default {DELAY}): ", type=float, default=0.15)
    parser.add_argument("-ppb", "--ppb", help=f"Specifies the number of packets per burst (ppb) (default {N_PPB}): ", type=int, default=1000)
    parser.add_argument("--code", help="Specifies Modbus function code (in decimal) of the burst: ", type=int,
                        choices=[idx for idx, c in enumerate(pt.codes._RAW_QUERIES) if c is not None], action="append")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true", default=False)

    args = parser.parse_args()
    if (args.burst == 1) and (args.code is None):
        parser.error("Continuous traffic requires a Modbus function code (--code)")
    if args.burst == 4 and args.code is not None and len(args.code) < 2:
        parser.error("Interleaved traffic requires more than one code (--code CODE_1 --code CODE_2 [--code CODE_3] ...)")

    _socket = connect_socket(args.addr, args.port)
   
    # XXX We should try/catch exceptions here...
    if args.burst == 1:
        print("Starting continuous traffic ...")
        _modbus_pkt =  Modbus(args.code[0])
        continuous(_socket, _modbus_pkt)
    elif args.burst == 2:
        print("Starting bursts of Modbus packets ...")
        bursts_of_main(_socket)
    elif args.burst == 3:
        print("Sending one packet of some Modbus function codes ...")
        one_of_each(_socket)
    elif args.burst == 4:
        print("Starting Interleaved burst with function codes", args.code)
        interleaved(_socket, args.code)

    _socket.close();
    print("Done!")
