from flask import Flask
import json, re


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
    # print(to_return)
    return to_return


# get_column('email')

app = Flask(__name__)

@app.route('/<name>')
def hello_name(name):
   return f'hellooooo {name}'

@app.route('/<say>/<name>')
def say_name(say, name):
   return f'{say} {name}'

@app.route('/say/<column>')
def say_column(column):
   return f'here are the {column}(s)\n\r{get_column(column)}'

@app.route('/say/<column>/<pattern>')
def say_pattern(column, pattern):
   return f"here are the {column}(s) according to the pattern '{pattern}'\n\r{get_column(column, pattern=pattern)}"


@app.route('/json')
def say_json():
   return {'nem' : 'fe', 'gtre' : 'rtyu'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5050', debug=True)