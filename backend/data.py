import requests
import config
import json

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

def add_hotel(name, disp, city, city_id):
    url = config.es_base_url + '/hotel'
    json_data = json.dumps(dict(
        name=name,
        available_days=[x[0] for x in disp if x[1] == '1'],
        city=city,
        city_id=city_id
    ))
    resp = requests.post(url, data=json_data)
    return resp.json()['_id']

def main():
    import_data = get_places(get_disps())
    for city in import_data:
        city_id = add_city(city)
        for hotel in import_data[city]:
            add_hotel(hotel['name'], hotel['disp'], city, city_id)

if __name__ == '__main__':
    main()
