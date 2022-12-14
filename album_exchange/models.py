from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import uuid
from werkzeug.security import generate_password_hash
import secrets
from datetime import datetime
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



# We might not need this, google firebase will give each user a token already so I can just get that from the database. 
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    display_name = db.Column(db.String(150), nullable = False, default = '')
    password = db.Column(db.String, nullable = True)
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, display_name='', first_name='', last_name='', id='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.display_name = display_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User {self.display_name} has been added to the database!"

class Album(db.Model):
    id = db.Column(db.String, primary_key = True)
    album_title = db.Column(db.String(150), nullable = False)
    artist_name = db.Column(db.String(100), nullable = False)
    year = db.Column(db.Integer, nullable = True)
    genre = db.Column(db.String(200), nullable = True)
    number_of_tracks = db.Column(db.Integer, nullable = True)
    label = db.Column(db.String(100), nullable = True)
    cover_url = db.Column(db.String(9999), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, album_title, artist_name, year, genre, number_of_tracks, label, user_token, cover_url, id = ''):
        self.id = self.set_id()
        self.album_title = album_title
        self.artist_name = artist_name
        self.year = year
        self.genre = genre
        self.number_of_tracks = number_of_tracks
        self.label = label
        self.cover_url = cover_url
        self.user_token = user_token

        def set_id(self):
            return secrets.token_urlsafe()

        def __repr__(self):
            return f"{self.album_title} has been added to your library!"

class AlbumSchema(ma.Schema):
    class Meta:
        fields = ['id', 'album_title', 'artist_name', 'year', 'genre', 'number_of_tracks', 'cover_url', 'label']

album_schema = AlbumSchema()
albums_schema = AlbumSchema(many = True)