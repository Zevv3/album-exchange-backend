from flask import Flask
from flask_migrate import Migrate
from .models import db as root_db, login_manager, ma
from config import Config
from .api.routes import api
from .helpers import JSONEncoder
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(api)

app.config.from_object(Config)

root_db.init_app(app)
migrate = Migrate(app, root_db)

ma.init_app(app)
app.json_encoder = JSONEncoder
CORS(app)