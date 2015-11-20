from flask import Flask, render_template
from flask_restful import reqparse, Resource, Api
from flask.ext.cors import CORS
import requests
import config
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
            result['type'] = hit['_type']
            results.append(result)
        return results


class HotelAvailability(ESResource):

    url = config.es_base_url+ '/hotel/_search'

    def parse_args(self):
        parser.add_argument('cityId')
        parser.add_argument('enterDate')
        parser.add_argument('exitDate')
        parser.add_argument('undefinedDates')
        self.args = parser.parse_args()

    def get_date_range(self):
        enter_date = self.args['enterDate']
        exit_date = self.args['exitDate']
        return ['26/05/2015', '27/05/2015', '30/05/2015']

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
        # GET desafiohu1/disp/_search
        # {
        # "query": {
        #     "filtered": {
        #     "filter": {
        #         "bool": {
        #         "must": [
        #             {
        #                 "term": {
        #                 "city_id": ["AVEjnt8sJTFSUzSrG34f"]
        #                 }
        #             },
        #             {
        #                 "term": {
        #                 "dates": ["3/5/2015", "4/5/2015", "5/5/2015", "6/5/2015", "7/5/2015", "8/5/2015"]
        #                 }
        #             }
        #         ]
        #         }
        #     }
        #     }
        # }
        # }
        resp = requests.post(self.url, data=json.dumps(query))
        return self.handle_result(resp.json())
api.add_resource(HotelAvailability, config.base_url+'hotel')


class Places(ESResource):

    url = config.es_base_url + '/city,hotel/_search'

    def parse_args(self):
        parser.add_argument('searchString', default='')
        self.args = parser.parse_args()

    def get(self):
        self.parse_args()
        query = {
            "sort" : [
                { "_type" : "asc" }, "_score"
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
        print json.dumps(query)
        resp = requests.post(self.url, data=json.dumps(query))
        return self.handle_result(resp.json())
api.add_resource(Places, config.base_url+'places')
