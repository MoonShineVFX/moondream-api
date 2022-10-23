from flask import json
from api.common import routes
from api.common.constants import Role
from .conftest import TEST_EMAIL, TEST_PASSWORD, t_create_user, t_delete_user, t_get_user_by_email


def setup_module():
    t_create_user(Role.ADMIN, TEST_EMAIL, TEST_PASSWORD)

def teardown_module():
    t_delete_user(TEST_EMAIL)

def action(test_client, **kwargs):
    data = {
        **kwargs,
        "uid": TEST_EMAIL,
    }
    json_dict = json.dumps(obj=data)
    return test_client.post(routes.USER_UPDATE_USER, data=json_dict, content_type='application/json')


def test_without_login(test_without_login):
    res = action(test_without_login, disabled=True)
    assert res.status_code == 401
    
def test_by_client(test_by_client):
    res = action(test_by_client, disabled=True)
    assert res.status_code == 403
    
def test_by_admin(test_by_admin):
    res = action(test_by_admin, disabled=True)
    assert res.status_code == 403

def test_by_superuser_with_wrong_attribute(test_by_superuser):
    res = action(test_by_superuser, disabled=True, TEST_WRONG_FILED=True)
    assert res.status_code == 400
  
def test_by_superuser(test_by_superuser):
    res = action(test_by_superuser, disabled=True)
    assert res.status_code == 200
    user = t_get_user_by_email(TEST_EMAIL)
    assert user["disabled"] == True
