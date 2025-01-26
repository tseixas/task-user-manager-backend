from flask import Flask
from app.config import Config
from flask_pymongo import PyMongo
from redis import Redis

mongo = PyMongo()
redis_client = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    global redis_client
    
    redis_client = Redis(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        decode_responses=True
    )

    return app
