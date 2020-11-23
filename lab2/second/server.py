import session as ses
# import transfer as pv
import sys

if __name__ == "__main__":

    server = ses.start_sever("0.0.0.0", int(sys.argv[1]))

    mess = ses.recv(server)
    print(mess)

    ses.send('ello too', server)


    # server_handler = ses.start_sever("0.0.0.0", int(sys.argv[1]))

    # # listening for connections
    # pv.recv(server_handler) 

    # val = 'do the lab'

    # pv.send(server_handler, val)
    # val = pv.recv(server_handler)
    
    # val += ' - no, you!'
    # pv.send(server_handler, val)
    # val_new = pv.recv(server_handler)