import session as ses
import sys

if __name__ == "__main__":

    client = ses.connect_to("0.0.0.0", int(sys.argv[1]))

    mess = 'hello there'

    ses.send(mess, client)

    file_text = ses.recv(client)
    print(file_text)
    # f = open("received.txt", "w")
    # f.write(file_text)
    # f.close()
    ses.close(client)
