import socket
from threading import Thread 
import concurrent.futures as cf
import queue
import json, re

conn_q = queue.Queue(maxsize=20)

HOST = '0.0.0.0'
PORT = 5321

threads = [] 

ma_file = open('parsed.json', "r")
file_data = ma_file.read()
json_data = json.loads(file_data)

def get_column(column, pattern=None):
    to_return = ''
    for person in json_data:
        # print(person)
        if column in json_data[person]:
            if pattern is not None:
                if re.search(pattern, json_data[person][column]):
                    to_return = f'{to_return}\n{json_data[person][column]}'
            else:
                # print(json_data[person][column])
                to_return = f'{to_return}\n{json_data[person][column]}'
    # print(f'getting col \n{to_return}')
    return f'{to_return}\n\n'

def parse_query(query):
    
    query = query.replace('\n', '').replace('\r', '')
    words = query.split(' ')
    # print(words)
    if words[0] == 'getCol':
        return get_column(words[1])
    elif words[0] == 'getPat':
        return get_column(words[1], words[2])
    else:
        return 'sorry, we\'ve got no such command\n' 

def respond(con, adr):
    try:
        with con:
            print('Connected by', adr)
            while True:
                data = con.recv(1024)
                if not data:
                    break
                # con.sendall(data)
                print(data)
                # print(data.decode('utf-8'))
                response = parse_query(data.decode('utf-8'))
                # print(f'sending resp{response}')
                con.sendall(response.encode('utf-8'))
    except Exception:
        pass
    finally:
        con.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    s.bind((HOST, PORT))
    
    s.listen(5)
    
    while True:
        
        conn, addr = s.accept()
        
        x = Thread(target=respond, args=(conn, addr))
        print(f'thread 1')
        x.start()
        threads.append(x)
        
    for t in threads: 
        t.join() 
    s.close()
