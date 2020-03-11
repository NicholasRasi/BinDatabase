import argparse

from flask import Flask, request
from flask_cors import CORS
from tinydb import TinyDB, Query
import datetime
import logging

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)
db = TinyDB('db.json')

@app.route('/all')
def get_all():
    data_bins = db.all()
    return {'bins': data_bins}


@app.route('/new', methods=['POST'])
def create_new():
    request_data = request.get_json()
    data_bin = db.search(Query().id == request_data["id"])
    if len(data_bin) != 0 or str(request_data["id"]) == "new":
        return {'error': 'bin already created'}, 400
    else:
        db.insert({'id': str(request_data["id"]),
                   'desc': str(request_data["desc"]),
                   'values': [],
                   'updated': str(datetime.datetime.now())})
        return {'msg': 'bin created'}


@app.route('/<bin_id>', methods=['GET', 'POST'])
def read_write(bin_id):
    if request.method == 'GET':
        data_bin = db.search(Query().id == bin_id)
        if len(data_bin) != 0:
            return {'desc': data_bin[0]['updated'],
                    'updated': data_bin[0]['updated'],
                    'values': data_bin[0]['values']}
        else:
            return {'error': 'bin not valid'}, 400
    elif request.method == 'POST':
        data_bin = db.search(Query().id == bin_id)
        if len(data_bin) != 0:
            values = data_bin[0]['values']
            values.append(request.get_json())
            db.update({'values': values,
                       'updated': str(datetime.datetime.now())}, Query().id == bin_id)
            return {'msg': 'bin updated'}
        else:
            return {'error': 'bin not valid'}, 400


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    app.run(host='0.0.0.0', port=args.port)
