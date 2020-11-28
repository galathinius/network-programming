import session as ses
import sys

if __name__ == "__main__":
    
    # while True:

        server = ses.start_sever("0.0.0.0", int(sys.argv[1]))
        mess = ses.recv(server)
        print(mess)

        ses.send('ello too', server)

        # f = open("../message.txt", "r")
        # file_text = f.read()
        # mess = ses.recv(server)
        # print(mess)

        # ses.send(file_text, server)
