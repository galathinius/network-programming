import json
import queue
from specific_parse import parse_json, parse_csv, parse_xml, parse_yml

q = queue.Queue()

def send_to_file(data):
    with open('parsed.json', "w") as f2:
        f2.write(json.dumps(data))
        f2.close()

def make_it_sring(data):
    for person in data:
        if 'id' in person:
            person['id'] = str(person['id'])
        if 'card_currency' in person:
            person['card_currency'] = str(person['card_currency'])
        if 'card_balance' in person:
            person['card_balance'] = str(person['card_balance'])
    return data

def parse_person_data():
    le_all = []
    while not q.empty():
        person = q.get()
        le_all = integrate_data(person, le_all)
        q.task_done()
    send_to_file(make_it_sring(le_all))

def same(person1, person2):
    uniq_keys = [
        'first_name', 
        'last_name', 
        'full_name',
        'email'
    ]
    comm  = person1.items() & person2.items()
        # mai putin dens
    if [True for key in uniq_keys
            for touple in comm 
            if key in touple]:
        return True
    return False
    
def anti_clone(pers1, pers2):
    return {**pers1, **pers2}

def integrate_data(data, everyone):
    for person1 in data:
        index_to_merge = [everyone.index(person2) 
                            for person2 in everyone 
                            if same(person1, person2)
                            ]
        if index_to_merge:
            everyone[index_to_merge[0]] = anti_clone(person1, everyone[index_to_merge[0]])
        else:
            everyone.append(person1)  
    return everyone  

def parse_response(req):
    if 'mime_type' in req:
        if req['mime_type'] == 'text/csv':
            q.put(parse_csv(req['data']))

        elif req['mime_type'] == 'application/xml':
            q.put(parse_xml(req['data']))
        else:
            q.put(parse_yml(req['data']))
    else:
        q.put(parse_json(req['data']))

