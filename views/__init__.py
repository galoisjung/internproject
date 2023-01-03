from functools import wraps
from flask import g
from flask import Response
from flask import request
import jwt as jwt
from flask import jsonify, current_app
from flask.json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return JSONEncoder.default(self, obj)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token is not None:
            try:
                payload = jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], 'HS256')
            except jwt.InvalidTokenError:
                payload = None

            if payload is None:
                return Response(status=401)

            user_id = payload['user_id']
            g.user_id = user_id

        else:
            return Response(status=401)

        return f(*args, **kwargs)

    return decorated_function


def create_endpoints(app, service):
    app.json_encoder == CustomJSONEncoder

    user_service = service.user_service

    @app.route("/ping", methods=['GET'])
    def ping():
        return "pong"

    @app.route("/sign-up", methods=['POST'])
    def sign_up():
        new_user = request.json
        print(new_user)
        new_user_id = user_service.create_new_user(new_user)
        new_user = user_service.get_user(new_user_id)

        print(jsonify(new_user))

        return jsonify(new_user)
