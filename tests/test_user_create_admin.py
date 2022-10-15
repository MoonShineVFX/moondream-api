from flask import json
from api.common import routes

from .utils import CLIENT_0, PASSWORD_0, SUPERUSER_0, ADMIN_0, CLIENT_1, PASSWORD_1, f_delete_user, f_login_user, f_logout_user


def create_user(test_client, email, password, **kwargs):
    data = {
        **kwargs,
        "email": email,
        "password": password
    }
    json_dict = json.dumps(obj=data)
    return test_client.post(routes.USER_CREATE_ADMIN, data=json_dict, content_type='application/json')


def create_by_role(test_client, email, password, admin_email, admin_password, **kwargs):
    f_login_user(test_client, email, password)
    res = create_user(test_client, admin_email, admin_password, **kwargs)
    print(res.data)
    f_logout_user(test_client)
    return res

def test_without_login(test_client):
    res = create_user(test_client, CLIENT_1, PASSWORD_1)
    assert res.status_code == 401
    
def test_by_client(test_client):
    res = create_by_role(test_client, CLIENT_0, PASSWORD_0, CLIENT_1, PASSWORD_1)
    assert res.status_code == 403
    
def test_by_admin(test_client):
    res = create_by_role(test_client, ADMIN_0, PASSWORD_0, CLIENT_1, PASSWORD_1)
    assert res.status_code == 403

def test_by_superuser_with_wrong_attribute(test_client):
    res = create_by_role(test_client, SUPERUSER_0, PASSWORD_0, CLIENT_1, PASSWORD_1, WRONG_EMAIL_FORMAT=True)
    assert res.status_code == 400
  
def test_by_superuser(test_client):
    res = create_by_role(test_client, SUPERUSER_0, PASSWORD_0, CLIENT_1, PASSWORD_1)
    json_dict = json.loads(res.data)
    uid = json_dict["data"]["uid"]
    assert res.status_code == 201
    f_delete_user(uid)
    
