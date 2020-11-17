import socket as skt

BUFF_SIZE = 1024

class Socket:
    def __init__(self, sock):
        self.sock = sock
        self.to_addr = None

def socket():
    return Socket(skt.socket(skt.AF_INET, skt.SOCK_DGRAM))

def server_socket(host, port):
    sock = socket()
    sock.sock.bind((host, port))
    return sock

def connect_to(sock, host, port):
    sock.to_addr = (host, port)
    return sock

def send(sock, val):
    sock.sock.sendto(val.encode('utf-8'), sock.to_addr)

def recv(sock):
    data, addr = sock.sock.recvfrom(BUFF_SIZE)
    # connect_to(sock, addr[0], addr[1])
    sock.to_addr = addr
    return data.decode('utf-8')