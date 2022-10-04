from flask import json
from api import routes
from .utils import CLIENT_0,  PASSWORD_0,  SUPERUSER_0, ADMIN_0,  f_login_user, f_logout_user, f_list_file


def delete_files(test_client, **kwargs):
    list = f_list_file()[:2]
    paths = [item["path"] for item in list]
    print(paths)
    data = {
        **kwargs,
        "paths": paths
    }
    json_dict = json.dumps(obj=data)
    return test_client.post(routes.FILE_DELETE_FILES, data=json_dict, content_type='application/json')


def action_by_role(test_client, email, password, **kwargs):
    f_login_user(test_client, email, password)
    res = delete_files(test_client, **kwargs)
    f_logout_user(test_client)
    return res

def test_without_login(test_client):
    res = delete_files(test_client)
    assert res.status_code == 401
    
def test_by_client(test_client):
    res = action_by_role(test_client, CLIENT_0, PASSWORD_0)
    assert res.status_code == 403
    
def test_by_admin(test_client):
    res = action_by_role(test_client, ADMIN_0, PASSWORD_0)
    assert res.status_code == 200

def test_by_superuser_with_wrong_attribute(test_client):
    res = action_by_role(test_client, SUPERUSER_0, PASSWORD_0, WRONG_EMAIL_FORMAT=True)
    assert res.status_code == 400
  
def test_by_superuser(test_client):
    res = action_by_role(test_client, SUPERUSER_0, PASSWORD_0)
    assert res.status_code == 200
