from flask import request
from functools import wraps
from .constants import DOGE_AUTHORIZATION

def doge_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        s = request.headers.get("Authorization")
        if not s or s != DOGE_AUTHORIZATION:
            return "Unauthorized", 401
        return f(*args, **kwargs)
    return decorated_function