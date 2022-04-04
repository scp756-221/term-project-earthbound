# Standard library modules
import csv
import logging
import os
import sys
import uuid
import glob
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response
import pickle
# Local modules
from prometheus_flask_exporter import PrometheusMetrics
import requests

import simplejson as json
from flask import jsonify, make_response

# The path to the file (CSV format) containing the sample data
DB_PATH='song_info.csv'
recommendation_model=pickle.load(open('model.pkl','rb'))
# The unique exercise code
# The EXER environment variable has a value specific to this exercise
ucode = 's3'
music = {
    "name": "http://cmpt756s2:30001/api/v1/music",
    "endpoint": [
        "list_all",
        "get_song",
        "create_song",
        "delete_song",
        
    ]
}
db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
    ]
}


# The application
app = Flask(__name__)
bp = Blueprint('app', __name__)


metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Song list process')
database = {}

@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")


@bp.route('/obtainall', methods=['GET'])
def list_all():
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    # list all songs here
    return {}

@bp.route('/recommendation', methods=['POST'])
def recommendation_fn():
    content = request.get_json()
    age=int(content['age'])
    if content['gender']=="M":
        gender=1
    else:
        gender=0
    recommendation = recommendation_model.predict([[age,gender]])
    recommendation=recommendation[0].split(" ")
    response = {
            "output": recommendation
            }
    return response

    

# @bp.route('/delete_in_music_service/<Id1>', methods=['DELETE'])
# def delete_in_music_service(Id1):
#     url = music['name'] + '/' + music['endpoint'][3]
#     response = requests.delete(
#         url,
#         params={"objtype": "music", "objkey": music_id},
#         headers={'Authorization': headers['Authorization']})
    
#     return {}
    

@bp.route('/obtain/<Id>', methods=['GET'])
def get_song(Id):
    headers = request.headers
    # check header here
    print("123")
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    payload = {"objtype": "music", "objkey": Id}
    print("45")
    url = music['name']+'/'+Id
    print("1")
    print("78")
    response=requests.get(
        url,
        headers={'Authorization': headers['Authorization']})
    return response.json()


@bp.route('/create', methods=['POST'])
def create_song():
    content = request.get_json()
    print(content)
    Artist = content['Artist']
    Song_name= content['SongTitle']
    url = music['name'] + '/'
    print("1")
    response =requests.post(
        url,
        json={"Artist": Artist, "SongTitle": Song_name},
        headers={'Authorization': 'Bearer A'})
    return response.json()

@bp.route('/delete/<Id>', methods=['DELETE'])
def delete_song(Id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    payload = {"objtype": "music", "objkey": Id}
    url = music['name'] + '/' + Id
    response = requests.delete(
        url,
        headers={'Authorization': headers['Authorization']})
    return (response.json())

@bp.route('/restore', methods=['GET'])
def restore_songs():
    global database
    id_list=[]
    for Id, value in database.items():
        id_list.append(Id)
    for i in id_list:
        del database[i]
    with open(DB_PATH, 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header line
        for Song_name, Length_of_the_music, Artist, Producers, Language, Rating_of_the_song, Released_Year, Id, genre in rdr:
            database[Id] = (Song_name, Length_of_the_music, Artist, Producers, Language, Rating_of_the_song, Released_Year, genre)
    return database

app.register_blueprint(bp, url_prefix='/api/v1/songs_list/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(-1)

    #load_db()
    #app.logger.error("Unique code: {}".format(ucode))
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)
