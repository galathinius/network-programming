# read the readme
from parsing import parse_person_data
from following import the_beginning, threads_distributor

from le_soket import start_soket

the_beginning()

threads_distributor()

parse_person_data()
print('fin de parcurgere')

# start_soket()
