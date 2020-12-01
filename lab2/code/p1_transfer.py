import socket as skt
import pickle
import base64
import hashlib

BUFF_SIZE = 1024

class Socket:
    def __init__(self, sock):
        self.sock = sock
        self.to_addr = None

def make_packet(val):
    try:
        val_b = val.encode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        val_b = val

    return pickle.dumps({
        'cksm' : hashlib.md5(val_b).hexdigest(), 
        'payload' : val,
        })

def is_valid(packet):
    val = packet['payload']
    try:
        val_b = val.encode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        val_b = val

    return packet['cksm'] == hashlib.md5(val_b).hexdigest()

def socket():
    return Socket(skt.socket(skt.AF_INET, skt.SOCK_DGRAM))

def server_socket(host, port):
    sock = socket()
    sock.sock.setsockopt(skt.SOL_SOCKET, skt.SO_REUSEADDR, 1)
    sock.sock.bind((host, port))
    return sock

def connect_to(sock, host, port):
    sock.to_addr = (host, port)
    print('connecting')
    send(sock, 'connect')
    return sock

def send(sock, val):
    # print('sending: ' + val)
    sock.sock.sendto(make_packet(val), sock.to_addr)
    data, addr = sock.sock.recvfrom(BUFF_SIZE)
    packet = pickle.loads(data)
    while packet['payload'] == 'nack':
        sock.sock.sendto(make_packet(val), sock.to_addr)
        data, addr = sock.sock.recvfrom(BUFF_SIZE)

def close(sock):
    print('closing connection')
    sock.sock.close()

def recv(sock):
    # while True:
        data, addr = sock.sock.recvfrom(BUFF_SIZE)
        packet = pickle.loads(data)
        if is_valid(packet):
            sock.sock.sendto(make_packet('ack'), addr)
            if packet['payload'] == 'connect':
                # print(addr)
                sock.to_addr = addr
                print('connection established')
                return
            else:
                return packet['payload']
        else:
            sock.sock.sendto(make_packet('nack'), addr)
        