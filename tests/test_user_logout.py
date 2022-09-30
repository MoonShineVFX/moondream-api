from .utils import f_login_user, SUPERUSER_0, PASSWORD_0
from api import routes

def logout_user(test_client):
    return test_client.post(routes.USER_LOGOUT)

def test_with_logged_in(test_client):
    f_login_user(test_client, SUPERUSER_0, PASSWORD_0)
    res = logout_user(test_client)
    assert res.status_code == 200

def test_without_logged_in(test_client):
    res = logout_user(test_client)
    assert res.status_code == 401