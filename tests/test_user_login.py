from api.common import routes
from .utils import create_auth_token, f_logout_user, SUPERUSER_0, PASSWORD_0, WRONG_EMAIL_FORMAT, PASSWORD_1

def login_user(test_client, email, password):
    token = create_auth_token(email, password)
    headers = {"Authorization": token}
    return test_client.post(routes.USER_LOGIN, headers=headers)

def test_exists_email(test_client):
    res = login_user(test_client, SUPERUSER_0, PASSWORD_0)
    assert res.status_code == 200
    f_logout_user(test_client)
    
def test_not_exists_email(test_client):
    res = login_user(test_client, WRONG_EMAIL_FORMAT, PASSWORD_1)
    assert res.status_code == 400
    
def test_exists_email_with_wrong_password(test_client):
    res = login_user(test_client, SUPERUSER_0, PASSWORD_1)
    assert res.status_code == 400