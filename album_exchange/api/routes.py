from flask import Blueprint, request, jsonify
# from album_exchange.helpers import token_required
from album_exchange.models import db, Album, ExchangeAlbum, album_schema, albums_schema, exchange_album_schema, exchange_albums_schema

import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

import random

admin_token = os.environ.get('ADMIN_TOKEN')

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata', methods = ['GET'])
def getdata():
    return {'some':'value'}

# Create Album
@api.route('/albums', methods=['POST', 'GET'])
# @token_required
def create_album():
    album_title = request.json['album_title']
    artist_name = request.json['artist_name']
    release_date = request.json['release_date']
    genre = request.json['genre']
    number_of_tracks = request.json['number_of_tracks']
    label = request.json['label']
    cover_url = request.json['cover_url']
    deezer_id = request.json['deezer_id']
    rating = ''
    review = ''
    user_token = request.json['user_token']
    # user_token = current_user_token.token

    # print(f"User Token: {current_user_token.token}")

    album = Album(album_title, artist_name, release_date, genre, number_of_tracks, label, cover_url, deezer_id, rating, review, user_token)

    db.session.add(album)
    db.session.commit()

    response = album_schema.dump(album)
    return jsonify(response)

# Get All Albums in user library
@api.route('/albums/<token>', methods=['GET'])
def get_user_albums(token):
    albums = Album.query.filter_by(user_token=token).all()
    response = albums_schema.dump(albums)
    print(response)
    return jsonify(response)

# Get ONE album in user library
# we can probably just get rid of token here
@api.route('/albums/<token>/<id>', methods=['GET'])
def get_one_album(token, id):
    owner = token
    if owner == token:
        album = Album.query.get(id)
        response = album_schema.dump(album)
        return jsonify(response)
    else:
        return jsonify({"error message": "Valid Token Required!"}), 401

# exchange calls this to get that 1 album, make a call to create in the new exchange database
# get all of exchange database is the exchange

@api.route('/exchange', methods=['GET'])
def get_exchange_albums():
    albums = ExchangeAlbum.query.all()
    response = exchange_albums_schema.dump(albums)
    print(response)
    return jsonify(response)

# Update ONE album in user library
@api.route('/albums/<token>/<id>', methods=['POST','PUT'])
def update_album(token, id):
    album = Album.query.get(id)

    album.album_title = request.json['album_title']
    album.artist_name = request.json['artist_name']
    album.release_date = request.json['release_date']
    album.genre = request.json['genre']
    album.number_of_tracks = request.json['number_of_tracks']
    album.label = request.json['label']
    # album.cover_url = request.json['cover_url']
    album.user_token = token

    db.session.commit()
    response = album_schema.dump(album)
    return jsonify(response)

# Delete ONE album in user library
@api.route('/albums/<id>', methods=['DELETE'])
def delete_album(id):
    album = Album.query.get(id)
    print(album)
    db.session.delete(album)
    db.session.commit()
    response = album_schema.dump(album)
    return jsonify(response)

# Review an Album
@api.route('/albums/review/<token>/<id>', methods=['POST', 'PUT'])
def review_album(token, id):
    album = Album.query.get(id)

    album.rating = request.json['rating']
    album.review = request.json['review']

    db.session.commit()
    response = album_schema.dump(album)
    return jsonify(response)

@api.route('/exchange/<token>', methods=['POST', 'GET'])
# @token_required
def send_exchange(token):
    album_title = request.json['album_title']
    artist_name = request.json['artist_name']
    release_date = request.json['release_date']
    genre = request.json['genre']
    number_of_tracks = request.json['number_of_tracks']
    label = request.json['label']
    cover_url = request.json['cover_url']
    deezer_id = request.json['deezer_id']
    rating = ''
    review = ''
    user_token = token
    # user_token = current_user_token.token

    # print(f"User Token: {current_user_token.token}")

    album = ExchangeAlbum(album_title, artist_name, release_date, genre, number_of_tracks, label, cover_url, deezer_id, rating, review, user_token)

    db.session.add(album)
    db.session.commit()

    response = exchange_album_schema.dump(album)
    return jsonify(response)

@api.route('/exchange/review/<token>/<id>', methods=['POST', 'PUT'])
# @token_required
def review_exchange(token, id):
    album = ExchangeAlbum.query.get(id)

    album.rating = request.json['rating']
    album.review = request.json['review']

    db.session.commit()
    response = exchange_album_schema.dump(album)
    return jsonify(response)

@api.route('/exchange/start/<token>', methods=['POST', 'PUT'])
# @token_required
def start_exchange(token):
    # I will set up an admin account and set the token of that account to admin_token 
    # so that not just anybody can start the exchange
    if token == admin_token:
        albums = ExchangeAlbum.query.all()
        users = [album.id for album in albums]
        random.shuffle(users)
        for album in albums:
            if album.id == users[0]:
                album.id = users[1]
                users.pop(1)
            else:
                album.id = users[0]
                users.pop(0)
        db.session.commit()
        response = exchange_album_schema.dump(albums)
        return jsonify(response)
    else:
        return jsonify({"error message": "You do not have permission to perform this action"}), 401
    
@api.route('/exchange/clear/<token>', methods=['DELETE'])
def clear_exchange(token):
    if token == admin_token:
        albums = ExchangeAlbum.query.all()
        db.session.delete(albums)
        db.session.commit()
        return jsonify({"message": "Exchange Cleared"})
    else:
        return jsonify({"error message": "You do not have permission to perform this action"}), 401