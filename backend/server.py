from flask import Flask
from flask_restful import reqparse, Resource, Api
from flask.ext.cors import CORS
from flask.ext.pymongo import PyMongo
from bson import json_util
import requests
import config
import json
import dateutil.parser


app = Flask(__name__)
app.config['MONGO_DBNAME'] = config.mongo_db_name
mongo = PyMongo(app)
CORS(app)
api = Api(app)
parser = reqparse.RequestParser()


class HotelAvailability(Resource):

    def parse_args(self):
        parser.add_argument('placeId')
        parser.add_argument('placeType')
        parser.add_argument('enterDate')
        parser.add_argument('exitDate')
        parser.add_argument('undefinedDate')
        self.args = parser.parse_args()

    def get_query(self):
        query = dict(available=True)
        if self.args.get('placeType') == 'city':
            query.update(city_id=self.args.get('placeId'))
        else:
            query.update(hotel_id=self.args.get('placeId'))
        if not self.args.get('undefinedDate') == 'true':
            enterDate = dateutil.parser.parse(self.args['enterDate'])
            exitDate = dateutil.parser.parse(self.args['exitDate'])
            query.update(date={'$gte': enterDate, '$lt': exitDate})
        return query

    def get(self):
        self.parse_args()
        query = self.get_query()
        result = mongo.db.disp.find(query)
        return [{
            'name': r['hotel_name'],
            'city': r['city_name'],
            'date': r['date'].strftime('%d/%m/%Y')
        } for r in result]

api.add_resource(HotelAvailability, config.base_url+'disp')


class Places(Resource):

    url = config.es_base_url + '/city,hotel/_search'

    def handle_result(self, data):
        results = []
        for hit in data['hits']['hits']:
            result = hit['_source']
            result['id'] = hit['_id']
            result['type'] = hit['_type']
            results.append(result)
        return results

    def parse_args(self):
        parser.add_argument('searchString', default='')
        self.args = parser.parse_args()

    def get(self):
        self.parse_args()
        query = {
            "sort": [
                {"_type": "asc"}, "_score"
            ],
            "query": {
                "multi_match": {
                    "fields": ["name", "city"],
                    "query": self.args.get('searchString'),
                    "type": "cross_fields",
                    "use_dis_max": False,
                    "operator": "and"
                }
            },
            "size": 10
        }
        resp = requests.post(self.url, data=json.dumps(query))
        return self.handle_result(resp.json())
api.add_resource(Places, config.base_url+'places')
