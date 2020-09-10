import requests
from base import base_link
from parsing import parse_response

def get_links(req):
    global to_follow
    to_follow = []
    links = req['link']
    for key in links:
        to_follow.append(links[key])

def follow():
    for link in to_follow:
        new_link = f"{base_link}{link}"
        followed = requests.get(new_link, headers=headers).json()
        print(f"\nfollowed {link}\n")
        print(followed)
        parse_response(followed)

def the_beginning():
    # first
    first_link = f"{base_link}/register"
    first = requests.get(first_link).json()

    # second
    global headers
    headers = {
            'X-Access-Token': first['access_token']
            }
    second_link = f"{base_link}{first['link']}"
    second = requests.get(second_link, headers=headers).json()

    print(second)

    get_links(second)
