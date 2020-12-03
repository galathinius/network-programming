import p2_0_session as ses
import sys

if __name__ == "__main__":
    
    server = ses.start_sever("0.0.0.0", 1919)
    mess = ses.recv(server)
    print(mess)

    ses.send('ello too', server)

       
