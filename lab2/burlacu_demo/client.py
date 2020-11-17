import protocol as pv
import sys

if __name__ == "__main__":
    proto_handler = pv.socket()
    pv.connect_to(proto_handler, 'localhost', int(sys.argv[1]))

    # pv.send(proto_handler, 'connect')

    val = pv.recv(proto_handler)
    print(val)

    val += ' - no, you!'
    pv.send(proto_handler, val)
    val_new = pv.recv(proto_handler)
    pv.send(proto_handler, val_new + ' - nope')
    print(val_new)