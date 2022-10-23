from flask import json
from api.common import routes
from api.common.constants import Role
from .conftest import t_create_user, t_delete_user, TEST_PASSWORD, TEST_EMAIL

def setup_function():
    t_create_user(Role.SUPERUSER, TEST_EMAIL, TEST_PASSWORD)

def teardown_function():
    try:
        t_delete_user(TEST_EMAIL)
    except Exception as e:
        print(e)

def action(test_client, **kwargs):
    data = {
        **kwargs,
        "uid": TEST_EMAIL,
    }
    json_dict = json.dumps(obj=data)
    print(data)
    return test_client.post(routes.USER_DELETE_USER, data=json_dict, content_type='application/json')


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
    assert res.status_code == 200
