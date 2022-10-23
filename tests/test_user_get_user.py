from api.common import routes
    
def test_without_logged_in(test_without_login):
    res = test_without_login.post(routes.USER_GET_USER)
    assert res.status_code == 401
    
def test_with_logged_in(test_by_superuser):
    res = test_by_superuser.post(routes.USER_GET_USER)
    assert res.status_code == 200    
