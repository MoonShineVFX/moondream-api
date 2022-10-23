from flask import json
from api.common import routes
from .conftest import IMAGE_0, IMAGE_1, t_upload_images, t_delete_files, t_get_file_path

IMAGE_NAMES=[IMAGE_0, IMAGE_1]


def setup_function():
    t_upload_images(names=IMAGE_NAMES)

def teardown_function():
    t_delete_files(names=IMAGE_NAMES)


def action(test_client, **kwargs):
    paths = [t_get_file_path(name) for name in IMAGE_NAMES]
    data = {
        **kwargs,
        "paths": paths
    }
    json_dict = json.dumps(obj=data)
    return test_client.post(routes.FILE_DOWNLOAD_ZIP, data=json_dict, content_type='application/json')


def test_without_login(test_without_login):
    res = action(test_without_login)
    assert res.status_code == 200
    
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
    res = action(test_by_superuser)
    assert res.status_code == 200
