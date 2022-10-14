from flask import request
from functools import wraps
from firebase_admin import auth
from flask_restful.utils import http_status_message

from .constants import Role, SESSION_ID_NAME
from .utils import output_json

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_cookie = request.cookies.get(SESSION_ID_NAME)
        if not session_cookie:
            return output_json(data={"message": http_status_message(401)}, code=401)

        try:
            decoded_claims = auth.verify_session_cookie(
                session_cookie, check_revoked=True)
            return f(*args, **kwargs, user_id=decoded_claims["user_id"], email=decoded_claims["email"])
        except Exception as e:
            return output_json(data={"message": http_status_message(401)}, code=401)

    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        session_cookie = request.cookies.get(SESSION_ID_NAME)
        if not session_cookie:
            return output_json(data={"message": http_status_message(401)}, code=401)
        try:
            decoded_claims = auth.verify_session_cookie(
                session_cookie, check_revoked=True)
            role = decoded_claims["role"]
            if role in [Role.ADMIN, Role.SUPERUSER]:
                return f(*args, **kwargs, user_id=decoded_claims["user_id"], email=decoded_claims["email"])
            else:
                return output_json(data={"message": http_status_message(403)}, code=403)
        except Exception as e:
            return output_json(data={"message": http_status_message(400)}, code=400)
    return decorated_function


def superuser_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_cookie = request.cookies.get(SESSION_ID_NAME)
        if not session_cookie:
            return output_json(data={"message": http_status_message(401)}, code=401)
        try:
            decoded_claims = auth.verify_session_cookie(
                session_cookie, check_revoked=True)
            role = decoded_claims["role"]
            if role == Role.SUPERUSER:
                return f(*args, **kwargs, user_id=decoded_claims["user_id"], email=decoded_claims["email"])
            else:
                return output_json(data={"message": http_status_message(403)}, code=403)
        except Exception as e:
            return output_json(data={"message": http_status_message(400)}, code=400)
    return decorated_function
