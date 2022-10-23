from api.common import routes


def action(test_client):
    return test_client.post(routes.USER_RESET_CURRENT_USER_PASSWORD)


def test_without_login(test_without_login):
    res = action(test_without_login)
    assert res.status_code == 401
    
def test_by_client(test_by_client):
    res = action(test_by_client)
    assert res.status_code == 302
    
def test_by_admin(test_by_admin):
    res = action(test_by_admin)
    assert res.status_code == 302

def test_by_superuser(test_by_superuser):
    res = action(test_by_superuser)
    assert res.status_code == 302
