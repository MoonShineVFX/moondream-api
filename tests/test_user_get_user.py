from api.common import routes
from .utils import f_login_user, f_logout_user, SUPERUSER_0, PASSWORD_0

    
def test_without_logged_in(test_client):
    res = test_client.post(routes.USER_GET_USER)
    assert res.status_code == 401
    
def test_with_logged_in(test_client):
    f_login_user(test_client, SUPERUSER_0, PASSWORD_0)
    res = test_client.post(routes.USER_GET_USER)
    assert res.status_code == 200    
    f_logout_user(test_client)
