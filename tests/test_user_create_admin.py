from flask import json
from api.common import routes

from .conftest import TEST_EMAIL, TEST_PASSWORD, t_delete_user, t_get_user_by_email


def teardown_function():
    try:
        user = t_get_user_by_email(TEST_EMAIL)
        t_delete_user(user["uid"])
    except Exception as e:
        print(e)


def action(test_client, **kwargs):
    data = {
        **kwargs,
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    json_dict = json.dumps(obj=data)
    return test_client.post(routes.USER_CREATE_ADMIN, data=json_dict, content_type='application/json')


def test_without_login(test_without_login):
    res = action(test_without_login)
    assert res.status_code == 401
    
def test_by_client(test_by_client):
    res = action(test_by_client)
    assert res.status_code == 403
    
def test_by_admin(test_by_admin):
    res = action(test_by_admin)
    assert res.status_code == 403

def test_by_superuser_with_wrong_attribute(test_by_superuser):
    res = action(test_by_superuser, TEST_WRONG_FILED=True)
    assert res.status_code == 400
  
def test_by_superuser(test_by_superuser):
    res = action(test_by_superuser)
    assert res.status_code == 201
    
    
    
    
