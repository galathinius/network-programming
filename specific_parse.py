import json
import yaml
import xml.etree.ElementTree as ET

def parse_json(data):
    parsed_json = (json.loads(data))
    return parsed_json

def parse_xml(data):
    root = ET.fromstring(data)
    list_data = []
    for person in root:
        to_add = {}
        for info in person:
            to_add[info.tag] = info.text
        list_data.append( to_add)
    return list_data

def parse_csv(data):
    rows = data.split('\n')[0:-1]
    rows = [i.split(',') for i in rows]
    list_data = []
    for row in rows[1:]:
        to_add = {}
        for column in rows[0]:
            to_add[column] = row[rows[0].index(column)]
        list_data.append( to_add)
    return list_data

def parse_yml(data):
    yaml_data = yaml.safe_load(data)
    return yaml_data
    