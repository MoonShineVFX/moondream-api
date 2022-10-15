from flask import json
from api.common import routes
from api.common.constants import Role
from .utils import CLIENT_0,  PASSWORD_0, SUPERUSER_0, ADMIN_0,  PASSWORD_1, SUPERUSER_1, WRONG_EMAIL_FORMAT, f_login_user, f_logout_user, f_create_user, f_delete_user


def setup_function():
    f_create_user(Role.SUPERUSER, SUPERUSER_1, PASSWORD_1)

def teardown_function():
    try:
        f_delete_user(SUPERUSER_1)
    except Exception as e:
        print(e)

def delete_user(test_client, uid, **kwargs):
    data = {
        **kwargs,
        "uid": uid,
    }
    json_dict = json.dumps(obj=data)
    print(data)
    return test_client.post(routes.USER_DELETE_USER, data=json_dict, content_type='application/json')


def delete_by_role(test_client, email, password, uid, **kwargs):
    f_login_user(test_client, email, password)
    res = delete_user(test_client, uid, **kwargs)
    print(res.data)
    f_logout_user(test_client)
    return res

def test_without_login(test_client):
    res = delete_user(test_client, SUPERUSER_1)
    assert res.status_code == 401
    
def test_by_client(test_client):
    res = delete_by_role(test_client, CLIENT_0, PASSWORD_0, SUPERUSER_1)
    assert res.status_code == 403
    
def test_by_admin(test_client):
    res = delete_by_role(test_client, ADMIN_0, PASSWORD_0, SUPERUSER_1)
    assert res.status_code == 403

def test_by_superuser_with_wrong_attribute(test_client):
    res = delete_by_role(test_client, SUPERUSER_0, PASSWORD_0, SUPERUSER_1, WRONG_EMAIL_FORMAT=True)
    assert res.status_code == 400
  
def test_by_superuser(test_client):
    res = delete_by_role(test_client, SUPERUSER_0, PASSWORD_0, SUPERUSER_1)
    assert res.status_code == 200
