import socket
from protocol.codes import *

WRITE_MULTIPLE_COILS_RESPONSE = b'\x00\x00\x00\x00\x00\x06\x00\x0F\x00\x00\x00\x06'


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 502))
    s.listen(10)
    cnx, addr = s.accept()
    print("Connection donde by " + str(addr))
    try:
        while True:
            # data = cnx.recv(1024).decode()
            data = cnx.recv(1024)     # OPTIMIZE: lower buffer = faster
            if not data:
                cnx.close()
                s.close()
                exit(0)
            else:
                print(data)
                if data == b'\x00\x00\x00\x00\x00\x06\x00\x01\x00\x00\x00\x06':
                    print("recived READ COILS (0x01)")
                    cnx.sendto(READ_COILS_R, (addr[0], addr[1]))

                elif data == b'\x00\x00\x00\x00\x00\x06\x00\x02\x00\x00\x00\x06':
                    print("recived READ DISCRETE INPUTS (0x02)")
                    cnx.sendto(READ_DISCRETE_INPUTS_R, (addr[0], addr[1]))

                elif data == b'\x00\x00\x00\x00\x00\x06\x00\x03\x00k\x00\x03':
                    print("recived READ HOLDING REGISTERS (0x01)")
                    cnx.sendto(READ_HOLDING_REGISTERS_R, (addr[0], addr[1]))

                elif data == b'\x00\x00\x00\x00\x00\t\x00\x10\x00\x01\x02\x04\x00\n\x01\x02':
                    print("recived WRITE MULTIPLE REGISTERS (0x01)")
                    cnx.sendto(WRITE_MULTIPLE_REGISTERS_R, (addr[0], addr[1]))

                else:
                    print("UNKNOWN PACKET")
                    print(data)
                    cnx.sendto(data, (addr[0], addr[1]))
    finally:
        cnx.close()
        s.close()


if __name__ == "__main__":
    main()
