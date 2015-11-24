from flask import Flask
from flask_restful import reqparse, Resource, Api
from flask.ext.cors import CORS
from flask.ext.pymongo import PyMongo
import requests
import config
import json

app = Flask(__name__)
app.config['MONGO_DBNAME'] = config.mongo_db_name
CORS(app)
api = Api(app)
mongo = PyMongo(app)
parser = reqparse.RequestParser()


class HotelAvailability(Resource):

    def parse_args(self):
        parser.add_argument('cityId')
        parser.add_argument('hotelId')
        parser.add_argument('enterDate')
        parser.add_argument('exitDate')
        parser.add_argument('undefinedDates')
        self.args = parser.parse_args()

    def get_data(self):
        if self.args.get('undefinedDates'):
            disps = mongo.db.disps.find(
                {'available': True}
            )

    def get(self):
        self.parse_args()
        return self.get_data()
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
