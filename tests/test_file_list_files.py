from flask import json
from api import routes
from .utils import CLIENT_0,  PASSWORD_0,  SUPERUSER_0, ADMIN_0,  f_login_user, f_logout_user


def get_files(test_client, **kwargs):
    json_dict = json.dumps(obj=kwargs)
    return test_client.post(routes.FILE_LIST_FILES, data=json_dict, content_type='application/json')


def query_by_user(test_client, email, password, **kwargs):
    f_login_user(test_client, email, password)
    res = get_files(test_client, **kwargs)
    print(res.data)
    f_logout_user(test_client)
    return res

def test_without_login(test_client):
    res = get_files(test_client)
    assert res.status_code == 401
    
def test_by_client(test_client):
    res = query_by_user(test_client, CLIENT_0, PASSWORD_0)
    assert res.status_code == 200
    
def test_by_admin(test_client):
    res = query_by_user(test_client, ADMIN_0, PASSWORD_0)
    assert res.status_code == 200

def test_by_superuser_with_wrong_attribute(test_client):
    res = query_by_user(test_client, SUPERUSER_0, PASSWORD_0, WRONG_EMAIL_FORMAT=True)
    assert res.status_code == 400
  
def test_by_superuser(test_client):
    res = query_by_user(test_client, SUPERUSER_0, PASSWORD_0, begin=1)
    assert res.status_code == 200
