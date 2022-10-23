from flask import json
from api.common import routes


def action(test_client, **kwargs):
    json_dict = json.dumps(obj=kwargs)
    return test_client.post(routes.FILE_LIST_FILES, data=json_dict, content_type='application/json')


def test_without_login(test_without_login):
    res = action(test_without_login)
    assert res.status_code == 401
    
def test_by_client(test_by_client):
    res = action(test_by_client)
    assert res.status_code == 200
    
def test_by_admin(test_by_admin):
    res = action(test_by_admin)
    assert res.status_code == 200

def test_by_superuser_with_wrong_attribute(test_by_superuser):
    res = action(test_by_superuser, TEST_WRONG_FILED=True)
    assert res.status_code == 400
  
def test_by_superuser(test_by_superuser):
    res = action(test_by_superuser, begin=1)
    assert res.status_code == 200
