from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @staticmethod
    def create_user(email, password):
        mongo = current_app.mongo

        password_hash = generate_password_hash(password)
        mongo.db.users.insert_one({"email": email, "password": password_hash})

        return {"email": email, "password": password_hash}

    @staticmethod
    def find_user_by_email(email):
        mongo = current_app.mongo

        user_data = mongo.db.users.find_one({"email": email})

        if user_data:
            return User(user_data['email'], user_data['password'])

        return None

    def verify_password(self, password):
        return check_password_hash(self.password, password)
