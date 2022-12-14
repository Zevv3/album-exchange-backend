from flask import Blueprint, request, jsonify
from album_exchange.helpers import token_required
from album_exchange.models import db, Album, album_schema, albums_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata', methods = ['GET'])
def getdata():
    return {'some':'value'}

# Create Album
@api.route('/albums', methods=['POST'])
@token_required
def create_album(current_user_token):
    album_title = request.json['album_title']
    artist_name = request.json['artist_name']
    year = request.json['year']
    genre = request.json['genre']
    number_of_tracks = request.json['number_of_tracks']
    label = request.json['label']
    cover_url = request.json['cover_url']
    user_token = current_user_token.token

    print(f"User Token: {current_user_token.token}")

    album = Album(album_title, artist_name, year, genre, number_of_tracks, label, cover_url, user_token=user_token)

    db.session.add(album)
    db.session.commit()

    response = album_schema.dump(album)
    return jsonify(response)

# Get All Albums in user library
@api.route('/albums/<token>', methods=['GET'])
def get_user_albums(token):
    albums = Album.query.filter_by(user_token=token).all()
    response = albums_schema.dump(albums)
    return jsonify(response)

# Get ONE album in user library
@api.route('/albums/<token>/<id>', methods=['GET'])
def get_one_album(token, id):
    owner = token
    if owner == token:
        album = Album.query.get(id)
        response = album_schema.dump(album)
        return jsonify(response)
    else:
        return jsonify({"error message": "Valid Token Required!"}), 401

# Update ONE album in user library
@api.route('albums/<token>/<id>', methods=['POST','PUT'])
def update_album(token, id):
    album = Album.query.get(id)

    album.album_title = request.json['album_title']
    album.artist_name = request.json['artist_name']
    album.year = request.json['year']
    album.genre = request.json['genre']
    album.number_of_tracks = request.json['number_of_tracks']
    album.label = request.json['label']
    album.cover_url = request.json['cover_url']
    album.user_token = token

    db.session.commit()
    response = album_schema.dump(album)
    return jsonify(response)

@api.route('albums/<id>', methods=['DELETE'])
def delete_album(id):
    album = Album.query.get(id)

    db.session.delete(album)
    db.session.commit()
    response = album_schema.dump(album)
    return jsonify(response)