from flask import Flask
from flask_redis import Redis

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
redis = Redis(app)

from app import routes
