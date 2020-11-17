import protocol as pv
import sys

if __name__ == "__main__":
    server_handler = pv.server_socket("localhost", int(sys.argv[1]))

    pv.recv(server_handler)


    val = 'do the lab'
    print(val)

    pv.send(server_handler, val)
    val = pv.recv(server_handler)
    print(val)

    val += 'no, you!'
    pv.send(server_handler, val)
    val_new = pv.recv(server_handler)
    print(val_new)