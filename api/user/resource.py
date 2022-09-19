import datetime
import base64
import os
from api import firebase_client

from flask import Blueprint, request, jsonify, make_response, Response, redirect
from marshmallow.exceptions import ValidationError

from firebase_admin import auth
from firebase_admin._user_mgt import UserRecord
from api import firebase_client

from .schema import UserBaseRequiredSchma, UserResetPasswordSchma, UserDeleteSchma
from ..utils import parse_request_form, handle_errors_response, successful_format, error_format
from ..decoration import login_required, admin_required, SESSION_ID_NAME
SUPERUSER = os.getenv('SUPERUSER')
ADMIN = os.getenv('ADMIN')
CLIENT = os.getenv('CLIENT')


user_api = Blueprint('user_api', __name__, url_prefix='/user')
client_auth = firebase_client.auth()


def create_user(email,
                password,
                uid=None,
                display_name=None,
                email_verified=False,
                phone_number=None,
                photo_url=None,
                disabled=False) -> UserRecord:

    return auth.create_user(
        uid=uid,
        display_name=display_name,
        email=email,
        email_verified=email_verified,
        phone_number=phone_number,
        photo_url=photo_url,
        password=password,
        disabled=disabled
    )


def login_user(email, password) -> Response:
    user = client_auth.sign_in_with_email_and_password(email, password)
    id_token = user['idToken']
    user['uid'] = user['localId']

    expires_in = datetime.timedelta(days=5)
    session_cookie = auth.create_session_cookie(
        id_token, expires_in=expires_in)

    response = make_response(jsonify(successful_format(data=user)))
    response.status_code = 200
    expires = datetime.datetime.now() + expires_in
    response.set_cookie(SESSION_ID_NAME, session_cookie,
                        expires=expires, httponly=True, secure=False)
    return response


@user_api.post('/login')
def login():
    try:
        auth = request.headers.get('Authorization')
        if not auth:
            raise ValidationError("")

        tmp = auth.rsplit(' ', 1)
        print('tmp', tmp)

        if tmp[0] != 'Basic':
            raise ValidationError("")

        decode = base64.b64decode(tmp[1]).decode("utf-8")
        print('decode', decode)

        email, password = decode.rsplit(':', 1)
        print('emai, passwor', email, password)
        return login_user(email, password)
    except Exception as e:
        return handle_errors_response(e)


@user_api.post('/sign_up_as_admin')
def register_as_admin():
    try:
        form = parse_request_form(UserBaseRequiredSchma(), request)
        user = create_user(**form, email_verified=True)
        auth.set_custom_user_claims(user.uid, {'role': SUPERUSER})
        return login_user(form['email'], form['password'])
    except Exception as e:
        return handle_errors_response(e)


@user_api.post('/sign_up_as_client')
def register_as_clien():
    try:
        form = parse_request_form(UserBaseRequiredSchma(), request)
        user = create_user(**form)
        auth.set_custom_user_claims(user.uid, {'role': CLIENT})
        return login_user(form['email'], form['password'])
    except Exception as e:
        return handle_errors_response(e)


@user_api.get('/profile')
@login_required
def profile(*args, **kwargs): 
    pass

@user_api.post('/update_user')
def update():
    pass


@user_api.post('/reset_password')
def reset_password():
    try:
        form = parse_request_form(UserResetPasswordSchma(), request)
        url = auth.generate_password_reset_link(email=form['email'])
        return redirect(url)
    except Exception as e:
        return handle_errors_response(e)


@user_api.post('/delete_user')
@admin_required
def delete_user(*args, **kwargs):
    try:
        form = parse_request_form(UserDeleteSchma(), request)
        auth.delete_user(form['uid'])
        return jsonify(successful_format(data=form))
    except Exception as e:
        return handle_errors_response(e)


@user_api.get('/list_admins')
@admin_required
def list_admins(*args, **kwargs):
    try:
        users = [{'email': user.email, 'uid': user.uid}
                 for user in auth.list_users().iterate_all()]
        return jsonify(successful_format(data={'users': users}))
    except Exception as e:
        return handle_errors_response(e)
