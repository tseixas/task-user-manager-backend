import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import timedelta
from flask import request, jsonify, current_app
from flask_mail import Message


def generate_task_id():
    return str(uuid.uuid4())


def is_valid_due_date(due_date):
    try:
        due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d %H:%M:%S')
        return due_date > datetime.datetime.utcnow()
    except ValueError:
        return False


def validate_password(password):
    if len(password) < 8:
        return False
    return True


def hash_password(password):
    return generate_password_hash(password)


def verify_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)


def generate_reset_token(email):
    redis_client = current_app.redis_client

    token = secrets.token_hex(16)

    redis_client.setex(token, timedelta(hours=1), email)

    send_reset_email(email, token)

    return token


def send_reset_email(email, token):
    mail = current_app.mail

    reset_url = f"http://localhost:5000/reset_password/{token}"

    msg = Message("Redefinição de Senha", recipients=[email])
    msg.body = f"Para redefinir sua senha, acesse o seguinte link: {reset_url}"
    
    mail.send(msg)
