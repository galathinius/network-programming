import json
import yaml

import queue
import xml.etree.ElementTree as ET
ma_data = []

q = queue.Queue()

def send_to_file(data):
    # print('opening file')
    # print(f'ma_data len: {len(data)}')
    f2 = open('parsed.json', "w")
    f2.write(json.dumps(data))
    # print('sending to file')

    f2.close()

def parse_person_data():
    # print('entering q')
    # print(q.qsize())
    while not q.empty():
        person = q.get()
        integrate_data(person)
        q.task_done()
    # print('exiting q')
    send_to_file(ma_data)

uniq_keys = [
    'first_name', 
    'last_name', 
    'full_name',
    'email'
]

def same(person1, person2):
    comm  = person1.items() & person2.items()
    # if comm: 
    #     print(comm)
        
    if [True for key in uniq_keys for touple in comm if key in touple]:
        return True
    return False
    

def anti_clone(pers1, pers2):
    return {**pers1, **pers2}


def integrate_data(data):
    
    for person1 in data:

        index_to_merge = [ma_data.index(person2) 
                            for person2 in ma_data 
                            if same(person1, person2)
                            ]

        if index_to_merge:
            ma_data[index_to_merge[0]] = anti_clone(person1, ma_data[index_to_merge[0]])

        else:
            ma_data.append(person1)
    # print(len(ma_data))      

def parse_json(data):
    # print('parsing json')
    parsed_json = (json.loads(data))
    dict_data = []
    for i in range (0, len(parsed_json)):
        dict_data.append( parsed_json[i])
    
    q.put(dict_data)

def parse_xml(data):
    # print('parsing xml')
    root = ET.fromstring(data)
    dict_data = []
    for i in range (0, len(root)):
        to_add = {}
        for j in range(0, len(root[i])):
            to_add[root[i][j].tag] = root[i][j].text
        dict_data.append( to_add)
    
    q.put(dict_data)


def parse_csv(data):
    # print('parsing csv')
    rows = data.split('\n')[0:-1]
    rows = [i.split(',') for i in rows]
    dict_data = []
    for i in range (1, len(rows)):
        to_add = {}
        for j in range(0, len(rows[0])):
            to_add[rows[0][j]] = rows[i][j]
        dict_data.append( to_add)

    q.put(dict_data)

def parse_yml(data):
    # print('parsing yml')
    yaml_data = yaml.safe_load(data)
    dict_data = []
    for i in range (0, len(yaml_data)):
        dict_data.append( yaml_data[i])
    
    q.put(dict_data)

def parse_response(req):
    if 'mime_type' in req:

        if req['mime_type'] == 'text/csv':
            parse_csv(req['data'])

        elif req['mime_type'] == 'application/xml':
            parse_xml(req['data'])
        else:
            parse_yml(req['data'])
    else:
        parse_json(req['data'])



