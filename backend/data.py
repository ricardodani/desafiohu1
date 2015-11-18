import requests
from . import config

def add_place(_id, city, hotel):
    city = get_or_add_city(city)

def parse_places():
    url = config.es_base_url['places']+'/_search'
    with open('hoteis.txt', 'r') as f:
        f_hotels = f.read()
        for place in f_hotels.split('\n'):
            _id, city, hotel = place.split(',')
            add_place(_id, city, hotel)
