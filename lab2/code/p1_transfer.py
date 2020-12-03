import socket as skt
import pickle
import base64
import hashlib

BUFF_SIZE = 1024

class Socket:
    def __init__(self, sock):
        self.sock = sock
        self.to_addr = None

def get_cksm(val):
    try:
        val_b = val.encode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        val_b = val
    return hashlib.md5(val_b).hexdigest()
    
def make_packet(val):
    return pickle.dumps({
        'cksm' : get_cksm(val), 
        'payload' : val,
        })

def is_valid(packet):
    return packet['cksm'] == get_cksm(packet['payload'])

def socket():
    return Socket(skt.socket(skt.AF_INET, skt.SOCK_DGRAM))

def server_socket(host, port):
    sock = socket()
    sock.sock.setsockopt(skt.SOL_SOCKET, skt.SO_REUSEADDR, 1)
    sock.sock.bind((host, port))
    return sock

def connect_to(sock, host, port):
    sock.to_addr = (host, port)
    get_ack(sock, make_packet('connect'))
    return sock

def get_ack(sock, mess, fin = False):
    sock.sock.sendto(mess, sock.to_addr)
    data, addr = sock.sock.recvfrom(BUFF_SIZE)
    packet = pickle.loads(data)
    for _ in range(5):
        if packet['payload'] == 'ack':
            break
        sock.sock.sendto(mess, sock.to_addr)
        data, addr = sock.sock.recvfrom(BUFF_SIZE)

    if fin:
        data, addr = sock.sock.recvfrom(BUFF_SIZE)
        packet = pickle.loads(data)
        return packet['payload'] == 'ack'

def chunks(lst, n):
    # Yield successive n-sized chunks from lst
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def make_header(val):
    # the header has the checksum of the message as a whole
    return pickle.dumps({
        'cksm' : get_cksm(get_cksm(val)), 
        'payload' : get_cksm(val),
        })

def send(sock, val):
    for _ in range(5):
        # make header
        # send header
        get_ack(sock, make_header(val))
        
        # send parts and get aks
        for part in chunks(val, 10):
            get_ack(sock, make_packet(part))

        # get general ak
        if get_ack(sock, make_packet('fin'), True):
            break
        
def wait_for_connections(sock):
    for _ in range(5):
        data, addr = sock.sock.recvfrom(BUFF_SIZE)
        packet = pickle.loads(data)
        if packet['payload'] == 'connect':
            sock.to_addr = addr
            sock.sock.sendto(make_packet('ack'), addr)
            print('connection established')
            return sock

def get_part(sock):
    while True:
        data, addr = sock.sock.recvfrom(BUFF_SIZE)
        packet = pickle.loads(data)
        if is_valid(packet):
            sock.sock.sendto(make_packet('ack'), addr)
            return packet['payload']
        else:
            sock.sock.sendto(make_packet('nack'), addr)

def recv(sock):
    # get header info
    header = get_part(sock)
    # get pakets
    first = get_part(sock)
    while True:
        part = get_part(sock)
        if part == 'fin':
            break
        # merge pakets
        first += part
    
    # chek merged to header cksm
    paket = {
        'cksm' : header, 
        'payload' : first,
    }

    if is_valid(paket):
    # send general ak
        sock.sock.sendto(make_packet('ack'), sock.to_addr)
        return paket['payload']
    else:
        sock.sock.sendto(make_packet('nack'), sock.to_addr)
    
