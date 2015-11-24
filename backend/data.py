import requests
import config
import json
from datetime import datetime
from server import app, mongo

def get_disps():
    disps = {}
    with open('artefatos/disp.txt', 'r') as f:
        f_disp = (x.split(',') for x in f.read().split('\n') if x)
        for disp in f_disp:
            _id, date, available = disp
            if _id in disps:
                disps[_id].append((date, available))
            else:
                disps[_id] = [(date, available)]
    return disps

def get_places(disps):
    places = {}
    with open('artefatos/hoteis.txt', 'r') as f:
        f_places = (x.split(',') for x in f.read().split('\n'))
        for place in f_places:
            _id, city, hotel = place
            hotel = dict(name=hotel, disp=disps[_id])
            if city not in places:
                places[city] = [hotel]
            elif hotel not in places[city]:
                places[city].append(hotel)
    return places

def add_city(name):
    url = config.es_base_url + '/city'
    resp = requests.post(url, data=json.dumps(dict(
        name=name
    )))
    return resp.json()['_id']

def add_hotel(name, city):
    url = config.es_base_url + '/hotel'
    json_data = json.dumps(dict(
        name=name,
        city=city,
    ))
    resp = requests.post(url, data=json_data)
    return resp.json()['_id']

def add_disp(hotel_id, hotel_name, city_id, city_name, disps):
    with app.app_context():
        results =  mongo.db.disp.insert_many([
            {
                'hotel_id': hotel_id,
                'hotel_name': hotel_name,
                'city_id': city_id,
                'city_name': city_name,
                'date': datetime.strptime(disp[0], '%d/%m/%Y'),
                'available': disp[1] == '1'
            } for disp in disps
        ])
        print 'Inserted %d disponibilities on %s - %s' % (
            len(results.inserted_ids), hotel_name, city_name
        )

def main():
    import_data = get_places(get_disps())
    for city in import_data:
        city_id = add_city(city)
        for hotel in import_data[city]:
            hotel_id = add_hotel(hotel['name'], city)
            add_disp(hotel_id, hotel['name'], city_id, city, hotel['disp'])

if __name__ == '__main__':
    main()
