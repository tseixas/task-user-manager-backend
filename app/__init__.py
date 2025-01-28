from flask import Flask
from flask_pymongo import PyMongo
from flask_mail import Mail
from redis import Redis
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config
from app.routes.auth import auth
from app.routes.tasks import tasks
from app.models.user import User


mongo = PyMongo()
redis_client = None
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # app.config["JWT_SECRET_KEY"] = app.config["JWT_SECRET_KEY"]
    jwt = JWTManager(app)

    CORS(app)

    mongo.init_app(app)
    mail.init_app(app)

    global redis_client

    redis_client = Redis(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        decode_responses=True
    )

    app.redis_client = redis_client
    app.mongo = mongo
    app.mail = mail

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(tasks, url_prefix='/tasks')

    with app.app_context():
        create_default_user(app.config["DEFAULT_ADMIN_EMAIL"], app.config["DEFAULT_ADMIN_PASSWORD"])

    return app


def create_default_user(email, password):
    User.create_user(email, password)
    print(f'Usuário padrão criado, {email} - {password}')
