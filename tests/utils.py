import base64
from flask import json
from api.firebase import FirebaseUser, FirebaseFile
from api.constants import SESSION_ID_NAME, Role


WRONG_EMAIL_FORMAT = "wrong_email_format"
SUPERUSER_0 = "superuser_0@gmail.com"
SUPERUSER_1 = "superuser_1@gmail.com"
SUPERUSER_2 = "superuser_2@gmail.com"
ADMIN_0 = "admin_0@gamil.com"
CLIENT_1 = "admin_1@gamil.com"
ADMIN_2 = "admin_2@gamil.com"
CLIENT_0 = "client_0@gmail.com"
CLIENT_1 = "client_1@gmail.com"
CLIENT_2 = "client_2@gmail.com" 
PASSWORD_0 = "000000"
PASSWORD_1 = "111111"
PASSWORD_2 = "222222"


def f_login_user(test_client, email, password):
    user, id_token = FirebaseUser().login_user(email, password)
    cookie = FirebaseUser().create_session_cookie(SESSION_ID_NAME, id_token)
    test_client.set_cookie("localhost", cookie['key'], cookie['value'])
    
def f_logout_user(test_client):
    cookie = FirebaseUser().disable_session_cookie(SESSION_ID_NAME)
    test_client.set_cookie("localhost", cookie['key'], cookie['value'])
    

def f_delete_user(uid):
    FirebaseUser().delete_user(uid)
        
def f_delete_users(uids=[]):
    FirebaseUser().delete_users(uids)
        
        
def f_create_user(role, email, password):
    return FirebaseUser().create_user(
        role=role,
        uid=email, 
        email=email, 
        password=password,
        email_verified= Role.CLIENT != role)


def create_auth_token(email, password):
    s = email + ":" + password
    b = s.encode()
    e = base64.b64encode(b)
    token = e.decode()
    return "Basic " + token


def load_data(json_data):
    return json.loads(json_data)

def f_list_file():
    return FirebaseFile().get_files(begin=1, end=9999999999999999)
