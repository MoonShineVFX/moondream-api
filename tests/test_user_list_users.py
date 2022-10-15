from flask import json
from api.common import routes
from .utils import CLIENT_0, PASSWORD_0, SUPERUSER_0, ADMIN_0, f_login_user, f_logout_user


def list_users(test_client, **kwargs):
    json_dict = json.dumps(obj=kwargs)
    return test_client.post(routes.USER_LIST_USERS, data=json_dict, content_type='application/json')
    

def create_by_role(test_client, email, password, **kwargs):
    f_login_user(test_client, email, password)
    res = list_users(test_client, **kwargs)
    print(res.data)
    f_logout_user(test_client)
    return res

def test_without_login(test_client):
    res = list_users(test_client)
    assert res.status_code == 401
    
def test_by_client(test_client):
    res = create_by_role(test_client, CLIENT_0, PASSWORD_0)
    assert res.status_code == 403
    
def test_by_admin(test_client):
    res = create_by_role(test_client, ADMIN_0, PASSWORD_0)
    assert res.status_code == 200

def test_by_superuser_with_wrong_attribute(test_client):
    res = create_by_role(test_client, SUPERUSER_0, PASSWORD_0, WRONG_EMAIL_FORMAT=True)
    assert res.status_code == 200
  
def test_by_superuser(test_client):
    res = create_by_role(test_client, SUPERUSER_0, PASSWORD_0)
    assert res.status_code == 200
    
