from flask import json
from api import routes
from .utils import SUPERUSER_2, WRONG_EMAIL_FORMAT, SUPERUSER_0, SUPERUSER_1, PASSWORD_1, f_delete_user


def create_user(test_client, email, password, **kwargs):
    data = {
        **kwargs,
        "email": email,
        "password": password
    }
    json_dict = json.dumps(obj=data)
    return test_client.post(routes.USER_CREATE_SUPERUSER, data=json_dict, content_type='application/json')

def test_create_with_exists_eamil(test_client):
    res = create_user(test_client, SUPERUSER_0, PASSWORD_1)
    assert res.status_code == 400

def test_create_with_correct_format(test_client):
    res = create_user(test_client, SUPERUSER_1, PASSWORD_1)
    res_data = json.loads(res.data)
    uid = res_data["data"]["uid"]
    assert res.status_code == 201
    f_delete_user(uid)

def test_create_with_wrong_format(test_client):
    res = create_user(test_client, WRONG_EMAIL_FORMAT, PASSWORD_1)
    assert res.status_code == 400
        
def test_create_with_wrong_attributes(test_client):
    res = create_user(test_client, SUPERUSER_2, PASSWORD_1, wrongAttribute=True)
    assert res.status_code == 400
        
