from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from datetime import timedelta
from app.models.user import User
# from app.utils import generate_reset_token, hash_password


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.find_user_by_email(email)

    if user and user.verify_password(password):
        redis_client = current_app.redis_client

        token = create_access_token(
            identity=email, expires_delta=timedelta(minutes=5))

        redis_client.setex(f"jwt:{email}", 300, token)

        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@auth.route('/register', methods=['POST'])
def register():
    data = request.json

    email = data["email"]
    password = data["password"]

    User.create_user(email, password)

    return jsonify({"message": "User registered successfully"}), 201


@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    redis_client = current_app.redis_client

    try:
        token = get_jwt()["jti"]

        if not token:
            return jsonify({"message": "Token não encontrado"}), 400

        redis_client.delete(token)

        return jsonify({"message": "Logout realizado com sucesso"}), 200
    except Exception as e:
        return jsonify({"error": "Erro ao realizar logout", "details": str(e)}), 500


# @auth.route('/reset-password', methods=['POST'])
# def reset_password():
#     data = request.get_json()
#     email = data.get('email')

#     user = User.find_user_by_email(email)

#     if not user:
#         return jsonify({'error': 'User not found'}), 404

#     reset_token = jwt.encode(
#         {'email': email, 'exp': datetime.datetime.utcnow(
#         ) + datetime.timedelta(hours=1)},  # Expira em 1 hora
#         current_app.config['SECRET_KEY'],
#         algorithm='HS256'
#     )

#     # Armazenando o token no Redis com um TTL de 1 hora
#     redis_client = current_app.redis_client
#     redis_client.setex(f"reset_token:{email}", 3600, reset_token)

#     # TODO: enviar email

#     return jsonify({'reset_token': reset_token}), 200


# @auth.route('/request_password_reset', methods=['POST'])
# def request_password_reset():
#     email = request.json.get("email")

#     if email:
#         token = generate_reset_token(email)

#         return jsonify({"message": "E-mail de redefinição enviado."}), 200
#     else:
#         return jsonify({"message": "E-mail não encontrado."}), 404


# @auth.route('/reset_password/<token>', methods=['POST'])
# def reset_password(token):
#     redis_client = current_app.redis_client
#     mongo = current_app.mongo

#     email = redis_client.get(token)

#     if email:
#         new_password = request.json.get("new_password")

#         mongo.db.users.update_one(
#             {"email": email}, {"$set": {"password": hash_password(new_password)}})

#         redis_client.delete(token)

#         return jsonify({"message": "Senha redefinida com sucesso."}), 200
#     else:
#         return jsonify({"message": "Token inválido ou expirado."}), 400
