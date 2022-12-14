from flask import Blueprint, request, jsonify
# from album_exchange.models import db, Album, album_schema, albums_schema
import discogs_client
import requests

search = Blueprint('search', __name__, url_prefix='/search')

consumer_key="SGnbdzOSBlQguorCeWZL"
consumer_secret="ZIYtXJaFCdFapSeXCcdXNnFqPeFOlCRz"
current_token="ZKEGTYUlqOaaEVUSbitxAEfpBNdatdaCjEyKPSgG"

# Request Token URL	https://api.discogs.com/oauth/request_token
# Authorize URL	https://www.discogs.com/oauth/authorize
# Access Token URL	https://api.discogs.com/oauth/access_token

# Testing discogs api calls

d = discogs_client.Client(
    'album_exchange/0.1',
    # consumer_key="SGnbdzOSBlQguorCeWZL",
    # consumer_secret="ZIYtXJaFCdFapSeXCcdXNnFqPeFOlCRz",
    user_token=current_token
    )
# print(d.get_authorize_url())
# print(d.get_access_token('GDznYgaaZQ'))
# print(d.identity())
# results = d.search('Can I borrow a feeling?')
# print(results.page(1))
# print(d.release(20017387).images[0])

# print(d.search('Lonesome Crowded West', type='release').page(1))
# print(dir(d.release(22460452)))

# Search by album title
@search.route('/album_title', methods=['GET'])
def search_album():
    """Searching the Deezer API for the album title"""
    title = request.json['album_title']
    r = requests.get(f'https://api.deezer.com/search/album?q={title}')
    data = r.json()