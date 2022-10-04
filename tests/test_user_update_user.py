from flask import json
from api import routes
from api.constants import Role
from .utils import CLIENT_0,  PASSWORD_0, PASSWORD_2, SUPERUSER_0, ADMIN_0,  PASSWORD_1, SUPERUSER_1, WRONG_EMAIL_FORMAT, f_login_user, f_logout_user, f_create_user, f_delete_user


def setup_module():
    f_create_user(Role.SUPERUSER, SUPERUSER_1, PASSWORD_1)

def teardown_module():
    f_delete_user(SUPERUSER_1)

def update_user(test_client, uid, obj):
    data = {
        **obj,
        "uid": uid,
    }
    json_dict = json.dumps(obj=data)
    return test_client.post(routes.USER_UPDATE_USER, data=json_dict, content_type='application/json')


def update_by_user(test_client, email, password, uid, obj):
    f_login_user(test_client, email, password)
    res = update_user(test_client, uid, obj)
    print(res.data)
    f_logout_user(test_client)
    return res

def test_without_login(test_client):
    res = update_user(test_client, SUPERUSER_1, obj={"password": PASSWORD_2})
    assert res.status_code == 401
    
def test_by_client(test_client):
    res = update_by_user(test_client, CLIENT_0, PASSWORD_0, SUPERUSER_1, obj={"password": PASSWORD_2})
    assert res.status_code == 403
    
def test_by_admin(test_client):
    res = update_by_user(test_client, ADMIN_0, PASSWORD_0, SUPERUSER_1, obj={"password": PASSWORD_2})
    assert res.status_code == 403

def test_by_superuser_with_wrong_attribute(test_client):
    res = update_by_user(test_client, SUPERUSER_0, PASSWORD_0, SUPERUSER_1, obj={"password": PASSWORD_2, WRONG_EMAIL_FORMAT: True})
    assert res.status_code == 400
  
def test_by_superuser(test_client):
    res = update_by_user(test_client, SUPERUSER_0, PASSWORD_0, SUPERUSER_1, obj={"password": PASSWORD_2, "disabled": True})
    assert res.status_code == 200
