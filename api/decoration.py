from flask import request
from functools import wraps
from firebase_admin import auth

from .constants import Role, SESSION_ID_NAME
from .utils import base_response


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # print("login_required")
        session_cookie = request.cookies.get(SESSION_ID_NAME)
        # print("session_cookie", session_cookie)
        if not session_cookie:
            return base_response(401, message="Unauthorized")

        try:
            decoded_claims = auth.verify_session_cookie(
                session_cookie, check_revoked=True)
            return f(*args, **kwargs, user_id=decoded_claims["user_id"], email=decoded_claims["email"])
        except Exception as e:
            return base_response(401, message="Unauthorized")
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # print("admin_required")
        
        session_cookie = request.cookies.get(SESSION_ID_NAME)
        # print("session_cookie", session_cookie)
        if not session_cookie:
            return base_response(401, message="Unauthorized")
        try:
            decoded_claims = auth.verify_session_cookie(
                session_cookie, check_revoked=True)
            role = decoded_claims["role"]
            if role in [Role.ADMIN, Role.SUPERUSER]:
                return f(*args, **kwargs, user_id=decoded_claims["user_id"], email=decoded_claims["email"])
            else:
                return base_response(403, message="Forbidden")
        except Exception as e:
            return base_response(400, message=str(e))
    return decorated_function


def superuser_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # print("superuser_required")
        session_cookie = request.cookies.get(SESSION_ID_NAME)
        # print("session_cookie", session_cookie)
        if not session_cookie:
            return base_response(401, message="Unauthorized")
        try:
            decoded_claims = auth.verify_session_cookie(
                session_cookie, check_revoked=True)
            role = decoded_claims["role"]
            if role == Role.SUPERUSER:
                return f(*args, **kwargs, user_id=decoded_claims["user_id"], email=decoded_claims["email"])
            else:
                return base_response(403, message="Forbidden")
        except Exception as e:
            return base_response(400, message=str(e))
    return decorated_function
