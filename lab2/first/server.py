import transfer as pv
import sys

if __name__ == "__main__":
    server_handler = pv.server_socket("0.0.0.0", int(sys.argv[1]))

    # listening for connections
    pv.recv(server_handler) 

    val = 'do the lab'

    pv.send(server_handler, val)
    val = pv.recv(server_handler)
    
    val += ' - no, you!'
    pv.send(server_handler, val)
    val_new = pv.recv(server_handler)
    