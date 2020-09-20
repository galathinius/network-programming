import json
import yaml

import queue
import xml.etree.ElementTree as ET
ma_data = {}

q = queue.Queue()

def send_to_file(data):
    print('opening file')
    f2 = open('parsed.json', "w")
    f2.write(json.dumps(data))
    print('sending to file')

    f2.close()

def parse_person_data():
    print('entering q')
    while not q.empty():
        person = q.get()
        integrate_data(person)
        q.task_done()
    print('exiting q')
    send_to_file(ma_data)

def integrate_data(data):

    print('integrating')
    # print(data)
    for person in data:
        if person in ma_data:
            for info in data[person]:
                ma_data[person][info] = data[person][info]
        else:
            ma_data[person] = data[person]
    
def look_at_names(data):
    print('looking at names')
    new_data = {}
    for person in data:    
        if 'full_name' in data[person]:
            names = data[person]['full_name'].split(' ')
            data[person]['first_name'] = names[0]
            data[person]['last_name'] = names[1]
        else :
            data[person]['full_name'] = f'{data[person]["first_name"]} {data[person]["last_name"]}' 
        new_data[data[person]['full_name']] = data[person]
    q.put(new_data)
    # integrate_data(new_data)
        

def parse_json(data):
    print('parsing json')
    parsed_json = (json.loads(data))
    dict_data = {}
    for i in range (0, len(parsed_json)):
        dict_data[i] = parsed_json[i]
    look_at_names(dict_data)

def parse_xml(data):
    print('parsing xml')
    root = ET.fromstring(data)
    dict_data = {}
    for i in range (0, len(root)):
        to_add = {}
        for j in range(0, len(root[i])):
            to_add[root[i][j].tag] = root[i][j].text
        dict_data[i] = to_add
    # print(dict_data)
    look_at_names(dict_data)


def parse_csv(data):
    print('parsing csv')
    rows = data.split('\n')[0:-1]
    rows = [i.split(',') for i in rows]
    dict_data = {}
    for i in range (1, len(rows)):
        to_add = {}
        for j in range(0, len(rows[0])):
            to_add[rows[0][j]] = rows[i][j]
        dict_data[i-1] = to_add
    # print(dict_data)
    look_at_names(dict_data)

def parse_yml(data):
    print('parsing yml')
    # print(data)
    yaml_data = yaml.safe_load(data)
    # print(yaml_data)
    dict_data = {}
    for i in range (0, len(yaml_data)):
        dict_data[i] = yaml_data[i]
    # print(dict_data)
    look_at_names(dict_data)
    # pass

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



