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
import pickle
# Local modules


# The path to the file (CSV format) containing the sample data
DB_PATH='song_info.csv'
recommendation_model=pickle.load (open('model.pkl','rb'))
# The unique exercise code
# The EXER environment variable has a value specific to this exercise
ucode = 's3'

# The application

app = Flask(__name__)

bp = Blueprint('app', __name__)

database = {}


def load_db():
    global database
    with open(DB_PATH, 'r') as inp:
        rdr = csv.reader(inp)
        next(rdr)  # Skip header line
        for Song_name, Length_of_the_music, Artist, Producers, Language, Rating_of_the_song, Released_Year, Id, genre in rdr:
            database[Id] = (Song_name, Length_of_the_music, Artist, Producers, Language, Rating_of_the_song, Released_Year, genre)
            
            
@bp.route('/deleteall', methods=['DELETE'])
def deleteall_songs():
    global database
    id_list=[]
    for Id, value in database.items():
        id_list.append(Id)
    for i in id_list:
        del database[i]
    return {}

@bp.route('/update/<Id1>', methods=['PUT'])
def update_song(Id1):
    global database
    if Id1 in database:
        try:
            content = request.get_json()
            Artist = content['Artist']
            Song_name= content['Song_name']
            Length_of_the_music= content['Length_of_the_music']
            Producers= content['Producers']
            Language= content['Language']
            Rating_of_the_song= content['Rating_of_the_song']
            Released_Year= content['Released_Year']
            genre= content['genre']
        except Exception:
            return app.make_response(
            ({"Message": "Error reading arguments"}, 400)
            )
        Id = Id1
        database[Id] = (Song_name, Length_of_the_music, Artist, Producers, Language, Rating_of_the_song, Released_Year,genre)
        response = {
            "Id": Id
        }
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return response


@bp.route('/health')
def health():
    return ""


@bp.route('/readiness')
def readiness():
    return ""


@bp.route('/obtainall', methods=['GET'])
def list_all():
    global database
    response = {
        "Count": len(database),
        "Items":
            [{'Song_name': value[0], 'Length_of_the_music': value[1],'Artist': value[2], 'Producers': value[3], 'Language': value[4], 'Rating_of_the_song': value[5], 'Released_Year': value[6],'Id': Id,'genre': value[7]}
             for Id, value in database.items()]
    }
    return response

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
    output_list=[]


    for Id, value in database.items():
        print(value[7], recommendation[0])
        if value[7]==recommendation[0]:
            output_list.append([{'Song_name': value[0], 'Length_of_the_music': value[1],'Artist': value[2], 'Producers': value[3], 'Language': value[4], 'Rating_of_the_song': value[5], 'Released_Year': value[6],'Id': Id,'genre': value[7]}])
    response = {
            "output": output_list
            }
    return response

    

@bp.route('/obtain/<Id>', methods=['GET'])
def get_song(Id):
    global database
    if Id in database:
        value = database[Id]
        response = {
            "Count": 1,
            "Items":
                [{'Song_name': value[0], 'Length_of_the_music': value[1],'Artist': value[2], 'Producers': value[3], 'Language': value[4], 'Rating_of_the_song': value[5], 'Released_Year': value[6],'Id': Id,'genre': value[7]}]
        }
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return response


@bp.route('/create', methods=['POST'])
def create_song():
    global database
    try:
        content = request.get_json()
        Artist = content['Artist']
        Song_name= content['Song_name']
        Length_of_the_music= content['Length_of_the_music']
        Producers= content['Producers']
        Language= content['Language']
        Rating_of_the_song= content['Rating_of_the_song']
        Released_Year= content['Released_Year'],
        genre= content['genre']
    except Exception:
        return app.make_response(
            ({"Message": "Error reading arguments"}, 400)
            )
    Id = len(database.items())+1
    database[Id] = (Song_name, Length_of_the_music, Artist, Producers, Language, Rating_of_the_song, Released_Year,genre)
    response = {
        "Id": Id
    }
    return response



@bp.route('/delete/<Id>', methods=['DELETE'])
def delete_song(Id):
    global database
    if Id in database:
        del database[Id]
    else:
        response = {
            "Count": 0,
            "Items": []
        }
        return app.make_response((response, 404))
    return {}



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

app.register_blueprint(bp, url_prefix='')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(-1)

    load_db()
    app.logger.error("Unique code: {}".format(ucode))
    p = int(sys.argv[1])
    app.run(host='0.0.0.0', port=p, threaded=True)
