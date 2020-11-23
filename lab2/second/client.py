# import transfer as pv
import session as ses
import sys

if __name__ == "__main__":

    client = ses.connect_to("0.0.0.0", int(sys.argv[1]))

    mess = 'hello there'

    ses.send(mess, client)

    mess = ses.recv(client)
    print(mess)

    # proto_handler = pv.socket()
    # pv.connect_to(proto_handler, '0.0.0.0', int(sys.argv[1]))

    # val = pv.recv(proto_handler)
    # val += ' - no, you!'
    # pv.send(proto_handler, val)

    # val_new = pv.recv(proto_handler)
    # pv.send(proto_handler, val_new + ' - nope')

    # pv.close(proto_handler)