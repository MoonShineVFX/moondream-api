from api.common import routes
from .utils import CLIENT_0, PASSWORD_0, SUPERUSER_0, ADMIN_0,  f_login_user, f_logout_user


def reset_password(test_client):
    return test_client.post(routes.USER_RESET_CURRENT_USER_PASSWORD)


def reset_password_by_user(test_client, email, password):
    f_login_user(test_client, email, password)
    res = reset_password(test_client)
    print(res.data)
    f_logout_user(test_client)
    return res

def test_without_login(test_client):
    res = reset_password(test_client)
    assert res.status_code == 401
    
def test_by_client(test_client):
    res = reset_password_by_user(test_client, CLIENT_0, PASSWORD_0)
    assert res.status_code == 302
    
def test_by_admin(test_client):
    res = reset_password_by_user(test_client, ADMIN_0, PASSWORD_0)
    assert res.status_code == 302

def test_by_superuser(test_client):
    res = reset_password_by_user(test_client, SUPERUSER_0, PASSWORD_0)
    assert res.status_code == 302
