from api.common import routes

def action(test_client):
    return test_client.post(routes.USER_LOGOUT)

def test_with_logged_in(test_by_superuser):
    res = action(test_by_superuser)
    assert res.status_code == 200

def test_without_logged_in(test_without_login):
    res = action(test_without_login)
    assert res.status_code == 401