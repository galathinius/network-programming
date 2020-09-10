
def parse_json(data):
    print('parsing json')
    pass

def parse_xml(data):
    print('parsing xml')
    pass

def parse_csv(data):
    print('parsing csv')
    pass

def parse_yml(data):
    print('parsing yml')
    pass

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



