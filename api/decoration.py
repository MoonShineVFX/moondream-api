import os
from flask import request, jsonify
from functools import wraps
from firebase_admin import auth

from .utils import handle_errors_response, error_format

SESSION_ID_NAME = os.getenv('SESSION_ID_NAME')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_cookie = request.cookies.get(SESSION_ID_NAME)
        if not session_cookie:
            return jsonify(error_format(message='Unauthorized')), 401

        try:
            decoded_claims = auth.verify_session_cookie(
                session_cookie, check_revoked=True)
            print('decoded_claims', decoded_claims)
            return f(*args, **kwargs, user_id=decoded_claims['user_id'], email=decoded_claims['email'])
        except Exception as e:
            return handle_errors_response(e)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_cookie = request.cookies.get(SESSION_ID_NAME)
        if not session_cookie:
            return jsonify(error_format(message='Unauthorized')), 401
        # try:
        decoded_claims = auth.verify_session_cookie(
            session_cookie, check_revoked=True)
        print('decoded_claims', decoded_claims)
        if decoded_claims['is_admin'] == True:
            return f(*args, **kwargs, user_id=decoded_claims['user_id'], email=decoded_claims['email'])
        else:
            return jsonify(error_format(message='Unauthorized')), 401
        # except Exception as e:
        #     return handle_errors_response(e)
    return decorated_function
