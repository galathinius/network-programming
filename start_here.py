# read the readme
from parsing import parse_person_data
from following import the_beginning, threads_distributor

links = the_beginning()

threads_distributor(links)

parse_person_data()
