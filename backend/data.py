import requests
import config


def do_the_magic(name):
    url = config.es_base_url + '/city'
    import ipdb; ipdb.set_trace()

def parse_places():
    with open('hoteis.txt', 'r') as f:
        f_hotels = f.read()
        for place in f_hotels.split('\n'):
            _id, city, hotel = place.split(',')
            do_the_magic(_id, city, hotel)
