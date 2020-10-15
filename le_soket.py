import socket
from threading import Thread 
import concurrent.futures as cf
import queue
import json, re
import os  

# to make a separate function

HOST = '0.0.0.0'
PORT = 5321

def get_data():
    with open('parsed.json', "r") as ma_file:
        file_data = ma_file.read()
        data = json.loads(file_data)
        return data

def get_column(column, pattern=None):
    to_return = ''
    for person in json_data:
        if column in person:
            if pattern is not None:
                if re.search(pattern, person[column]):
                    to_return = f'{to_return}\n{person[column]}'
            else:
                to_return = f'{to_return}\n{person[column]}'
    if to_return == '':
        to_return = 'check your spelling, maybe there is no such column, or no data according to the pattern'
    return f'{to_return}\n\n'

def parse_query(query):
    help_string = """\nyou can use the following commands: 
    getCol column - so that you get a column
    getPat column pattern - so that you get a column filtered with the pattern\n\n"""
    
    query = query.replace('\n', '').replace('\r', '')
    words = query.split(' ')
    
    if words[0] == 'getCol':
        return get_column(words[1])
    elif words[0] == 'getPat':
        return get_column(words[1], words[2])
    elif words[0] == 'help':
        return help_string
    else:
        return '\nsorry, we\'ve got no such command\n' + help_string

def respond(con, adr):
    try:
        with con:
            print('Connected by', adr)
            while True:
                data = con.recv(1024)
                if not data:
                    break
                print(data)
                response = parse_query(data.decode('utf-8'))
                con.sendall(response.encode('utf-8'))
    except Exception:
        pass
    finally:
        con.close()

def print_info():
    print(f'soket started, you can connect on the ip:')
    cmd = "hostname -I |awk '{print $1}'"
    os.system(cmd) 
    print(f'using port {PORT} \n')

def start_soket():
    global json_data
    json_data = get_data()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        s.bind((HOST, PORT))
        s.listen()
        
        print_info()

        while True:
            conn, addr = s.accept()
            x = Thread(target=respond, args=(conn, addr))
            x.start()
        
# start_soket()