from api.common import routes
from .conftest import IMAGE_0, IMAGE_1, t_create_image, t_delete_files



def teardown_function():
    try:
        t_delete_files(names=[IMAGE_0, IMAGE_1])
    except Exception as e:
        print(e)


def action(test_client, **kwargs):
    data = {
        **kwargs,
        "files": [(t_create_image(IMAGE_0)), (t_create_image(IMAGE_1))]
    }
    
    return test_client.post(
        routes.FILE_UPLOAD_FILES, 
        content_type='multipart/form-data',
        data=data
        )


def test_without_login(test_without_login):
    res = action(test_without_login)
    assert res.status_code == 401
    
def test_by_client(test_by_client):
    res = action(test_by_client)
    assert res.status_code == 403
    
def test_by_admin(test_by_admin):
    res = action(test_by_admin)
    assert res.status_code == 201
        
def test_by_superuser_with_wrong_attribute(test_by_superuser):
    res = action(test_by_superuser, TEST_WRONG_FILED=True)
    assert res.status_code == 400
  
def test_by_superuser(test_by_superuser):
    res = action(test_by_superuser)
    assert res.status_code == 201
    