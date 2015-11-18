from flask import Flask, render_template
from flask_restful import reqparse, Resource, Api
from flask.ext.cors import CORS
import requests
from . import config
import json

app = Flask(__name__)
CORS(app)
api = Api(app)

parser = reqparse.RequestParser()


class ESResource(Resource):

    def handle_result(self, data):
        results = []
        for hit in data['hits']['hits']:
            result = hit['_source']
            result['id'] = hit['_id']
            results.append(result)
        return results


class HotelAvailability(ESResource):

    url = config.es_base_url['hotel']

    def parse_args(self):
        parser.add_argument('cityId')
        parser.add_argument('enterDate')
        parser.add_argument('exitDate')
        parser.add_argument('undefinedDates')
        self.args = parser.parse_args()

    def get_date_range(self):
        enter_date = self.args['enterDate']
        exit_date = self.args['exitDate']
        return ['2011-11-10']

    def get(self):
        self.parse_args()
        query = {
            "query": {
                "match": {
                    "available_days": {
                        "query": self.get_date_range(),
                        "operator": "and"
                    }
                }
            }
        }
        resp = requests.post(self.url, data=json.dumps(query))
        return self.handle_result(resp.json())


class Places(ESResource):

    url = config.es_base_url['places']

    def parse_args(self):
        parser.add_argument('searchString')
        self.args = parser.parse_args()

    def get(self):
        self.parse_args()
        query = {
            "query": {
                "multi_match": {
                    "fields": ["name", "city"],
                    "query": self.args['searchString'],
                    "type": "cross_fields",
                    "use_dis_max": False
                }
            },
            "size": 100
        }
        resp = requests.post(self.url, data=json.dumps(query))
        return self.handle_result(resp.json())


api.add_resource(HotelAvailability, config.api_base_url+'/hotel')
api.add_resource(Places, config.api_base_url+'/places')
