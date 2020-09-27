import requests
import concurrent.futures as cf
from base import base_link
from parsing import parse_response
import queue
 
link_q = queue.Queue(maxsize=20)

def get_links(req):
    if 'link' in req:
        links = req['link']
        for key in links:
            link_q.put(links[key])         

def follow(link_to_follow):
    new_link = f"{base_link}{link_to_follow}"
    followed = requests.get(new_link, headers=headers).json()
    print(f"\nfollowed {link_to_follow}\n")
    get_links(followed)
    parse_response(followed)


def threads_distributor():
    with cf.ThreadPoolExecutor(max_workers=7) as executor:
        while True:
            try:
                link = link_q.get(timeout=7)
                link_q.task_done()
                executor.submit(follow, link)
            except queue.Empty:
                break
                 

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

    get_links(second)
