import argparse
from flask import Flask, request
from flask_cors import CORS
from tinydb import TinyDB, Query
import datetime
import logging
from threading import Lock

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)
db = TinyDB('db.json')
mutex = Lock()


def create_new(bin_id):
    db.insert({'id': bin_id,
               'values': [],
               'updated': str(datetime.datetime.now())})


def get_bin_data(data_bin):
    if len(data_bin) != 0:
        return {'updated': data_bin[0]['updated'],
                'values': data_bin[0]['values']}
    else:
        return {'error': 'bin not valid'}, 400


def add_data(bin_id, data_bin):
    values = data_bin[0]['values']
    values.append(request.get_json())
    db.update({'values': values, 'updated': str(datetime.datetime.now())}, Query().id == bin_id)
    return {'msg': 'bin updated'}


@app.route('/all')
def get_all():
    data_bins = db.all()
    return {'bins': data_bins}


@app.route('/<bin_id>', methods=['GET', 'POST'])
def read_write(bin_id):
    bin_id = str(bin_id)
    if request.method == 'GET':
        mutex.acquire()
        data_bin = db.search(Query().id == bin_id)
        # return bin data if exists
        ret = get_bin_data(data_bin)
        mutex.release()
        return ret
    elif request.method == 'POST':
        mutex.acquire()
        data_bin = db.search(Query().id == bin_id)
        if len(data_bin) == 0:
            # bin not present -> create bin -> add value
            create_new(bin_id)
            data_bin = db.search(Query().id == bin_id)
        ret = add_data(bin_id, data_bin)
        mutex.release()
        return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=int, default="0.0.0.0")
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port)
