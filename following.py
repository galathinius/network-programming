import requests
import threading
import concurrent.futures as cf
from base import base_link
from parsing import parse_response

to_follow = []


def get_links(req):
    links_to_return = []
    if 'link' in req:
        links = req['link']
        for key in links:
            links_to_return.append(links[key])
            # executor.submit(follow, links[key])
    print(links_to_return)
    return links_to_return

def follow(link_to_follow):
    new_link = f"{base_link}{link_to_follow}"
    followed = requests.get(new_link, headers=headers).json()
    print(f"\nfollowed {link_to_follow}\n")
    new_links = get_links(followed)
    threads_distributor(new_links)
    parse_response(followed)

# def get_a_link():
#     return to_follow.pop(0)

def threads_distributor(links):
    # executor = 
    if links:
        with cf.ThreadPoolExecutor(max_workers=len(links)) as executor:
            response = executor.map(follow, links)
            

def the_beginning():
    print('the beginning')
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

    return get_links(second)
