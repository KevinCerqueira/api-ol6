import os
import time
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import bcrypt
from core import Core
import json
import certifi
from flask_cors import CORS

utils = Core(origin=__name__)

api = Flask(__name__)
CORS(api)

secret_key = os.urandom(24).hex()
api.config['SECRET_KEY'] = secret_key

api.config["MONGO_URI"] = os.getenv('DB_URI')
mongo = PyMongo(api, tlsCAFile=certifi.where())
db = mongo.db.users


@api.route('/', methods=['GET'])
def index():
    return success_response([], 'Hello World!')


@api.route('/api/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    user = db.find_one({'email': email})

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return success_response({"id": str(user['_id'])}, 'Login successful')
    else:
        return error_response('Invalid username or password')


@api.route('/api/users', methods=['POST'])
def create_user():
    user_data = request.json

    # Verificando se 'email' e 'password' estão presentes
    if 'email' not in user_data or 'password' not in user_data:
        return error_response('Missing email or password')

    # Hash da senha
    hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt())
    user_data['password'] = hashed_password

    # Inserindo no banco de dados
    result = db.insert_one(user_data)

    return success_response({"id": str(result.inserted_id)}, 'User created successfully')


@api.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = db.find_one({'_id': ObjectId(user_id)})
    if user:
        user['id'] = str(user["_id"])
        del user["_id"]
        del user["password"]

        response = json_util.dumps(user)
        return success_response(json.loads(response), 'User fetched successfully')
    else:
        return error_response('User not found')


@api.route('/api/users', methods=['GET'])
def get_users():
    users = db.find()
    if users:
        response = list()
        for user in users:
            user["id"] = str(user["_id"])
            del user['_id']
            del user['password']
            response.append(user)

        response = json_util.dumps(response)
        return success_response(json.loads(response), 'Users fetched successfully')
    else:
        return error_response('Some error has occurred')


@api.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    update_data = request.json
    user = db.find_one({'_id': ObjectId(user_id)})

    # Verificando se o usuário existe
    if not user:
        return error_response('User not found')

    # Verificando se todos os campos a serem atualizados existem no usuário
    missing_fields = [field for field in update_data if field not in user]
    if missing_fields:
        return error_response(f'Missing fields in the user: {", ".join(missing_fields)}')

    # Se a senha estiver presente, ela precisa ser hashada
    if 'password' in update_data:
        hashed_password = bcrypt.hashpw(update_data['password'].encode('utf-8'), bcrypt.gensalt())
        update_data['password'] = hashed_password

    # Atualizando no banco de dados
    db.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
    return success_response({}, 'User updated successfully')


@api.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    db.delete_one({'_id': ObjectId(user_id)})
    return success_response({}, 'User deleted successfully')


def success_response(data, message: str):
    return jsonify({
        "success": True,
        "data": data,
        "message": message,
        "time": time.time(),
        "timestamp": int(time.time())
    })


def error_response(message: str, trace: list = None):
    return jsonify({
        "success": False,
        "error": {
            "message": message,
            "trace": trace
        }
    }), 400


if __name__ == "__main__":
    api.run(debug=True)
