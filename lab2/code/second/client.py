import p2_0_session as ses
import sys

if __name__ == "__main__":

    client = ses.connect_to("0.0.0.0", 1919)

    mess = 'hello there'

    ses.send(mess, client)

    file_text = ses.recv(client)
    print(file_text)
    
