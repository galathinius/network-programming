import requests
import threading
import concurrent.futures as cf
from base import base_link
from parsing import parse_response

to_follow = []
executor = cf.ThreadPoolExecutor(max_workers=5)

def get_links(req):

    if 'link' in req:
        links = req['link']
        for key in links:
            to_follow.append(links[key])
            # executor.submit(follow, links[key])
    print(to_follow)

def follow(link_to_follow):
    new_link = f"{base_link}{link_to_follow}"
    followed = requests.get(new_link, headers=headers).json()
    print(f"\nfollowed {link_to_follow}\n")
    get_links(followed)
    parse_response(followed)

def get_a_link():
    return to_follow.pop(0)

def threads_distributor():
    with executor:
        while to_follow:
            link = to_follow.pop(0)
            executor.submit(follow, link)

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

    get_links(second)
