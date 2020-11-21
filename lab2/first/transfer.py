import socket as skt
import json
import hashlib

BUFF_SIZE = 1024

def make_packet(val):
    return json.dumps({
        'cksm' : hashlib.md5(val.encode('utf-8')).hexdigest(), 
        'payload' : val,
        }).encode('utf-8')

def is_valid(packet):
    val = packet['payload']
    return packet['cksm'] == hashlib.md5(val.encode('utf-8')).hexdigest()

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
    print('connecting')
    send(sock, 'connect')
    return sock

def send(sock, val):
    print('sending: ' + val)
    sock.sock.sendto(make_packet(val), sock.to_addr)
    data, addr = sock.sock.recvfrom(BUFF_SIZE)
    packet = json.loads(data.decode('utf-8'))
    while packet['payload'] == 'nack':
        sock.sock.sendto(make_packet(val), sock.to_addr)
        data, addr = sock.sock.recvfrom(BUFF_SIZE)

def close(sock):
    print('closing connection')
    sock.sock.close()

def recv(sock):
    while True:
        data, addr = sock.sock.recvfrom(BUFF_SIZE)
        packet = json.loads(data.decode('utf-8'))
        if is_valid(packet):
            sock.sock.sendto(make_packet('ack'), addr)
            if packet['payload'] == 'connect':
                sock.to_addr = addr
                print('connection established')
                return
            else:
                return packet['payload']
        else:
            sock.sock.sendto(make_packet('nack'), addr)
        