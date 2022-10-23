from flask import json
from api.common import routes
from .conftest import TEST_WRONG_EMAIL_FORMAT, TEST_EMAIL, TEST_PASSWORD, t_delete_user, t_get_user_by_email


def teardown_function():
    try:
        user = t_get_user_by_email(TEST_EMAIL)
        t_delete_user(user["uid"])
    except Exception as e:
        print(e)


def action(test_without_login, email, password, **kwargs):
    data = {
        **kwargs,
        "email": email,
        "password": password
    }
    json_dict = json.dumps(obj=data)
    return test_without_login.post(routes.USER_CREATE_SUPERUSER, data=json_dict, content_type='application/json')

def test_with_correct_format_and_exists_eamil(test_without_login):
    res = action(test_without_login, TEST_EMAIL, TEST_PASSWORD)
    assert res.status_code == 201
    res = action(test_without_login, TEST_EMAIL, TEST_PASSWORD)
    assert res.status_code == 400

def test_with_wrong_format(test_without_login):
    res = action(test_without_login, TEST_WRONG_EMAIL_FORMAT, TEST_PASSWORD)
    assert res.status_code == 400
        
def test_with_wrong_attributes(test_without_login):
    res = action(test_without_login, TEST_EMAIL, TEST_PASSWORD, TEST_WRONG_FILED=True)
    assert res.status_code == 400
        
