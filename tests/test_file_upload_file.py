from api.common import routes
from .utils import CLIENT_0, IMAGE_0, IMAGE_1,  PASSWORD_0,  SUPERUSER_0, ADMIN_0,  f_login_user, f_logout_user, f_create_image, f_delete_files



def upload_files(test_client, **kwargs):
    data = {
        **kwargs,
        "file": (f_create_image(), IMAGE_0)
    }
    
    return test_client.post(
        routes.FILE_UPLOAD_FILE, 
        content_type='multipart/form-data',
        data=data
        )


def upload_by_user(test_client, email, password, **kwargs):
    f_login_user(test_client, email, password)
    res = upload_files(test_client, **kwargs)
    print(res.data)
    f_logout_user(test_client)
    return res

def test_without_login(test_client):
    res = upload_files(test_client)
    assert res.status_code == 401
    
def test_by_client(test_client):
    res = upload_by_user(test_client, CLIENT_0, PASSWORD_0)
    assert res.status_code == 403
    
def test_by_admin(test_client):
    res = upload_by_user(test_client, ADMIN_0, PASSWORD_0)
    assert res.status_code == 201
    f_delete_files(names=[IMAGE_0])
    

def test_by_superuser_with_wrong_attribute(test_client):
    res = upload_by_user(test_client, SUPERUSER_0, PASSWORD_0, WRONG_EMAIL_FORMAT=True)
    assert res.status_code == 400
  
def test_by_superuser(test_client):
    res = upload_by_user(test_client, SUPERUSER_0, PASSWORD_0)
    assert res.status_code == 201
    f_delete_files(names=[IMAGE_0])
    