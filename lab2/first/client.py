import transfer as pv
import sys

if __name__ == "__main__":
    proto_handler = pv.socket()
    pv.connect_to(proto_handler, '0.0.0.0', int(sys.argv[1]))

    val = pv.recv(proto_handler)
    val += ' - no, you!'
    pv.send(proto_handler, val)

    val_new = pv.recv(proto_handler)
    pv.send(proto_handler, val_new + ' - nope')

    pv.close(proto_handler)