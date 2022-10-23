from api.common import routes
from api.common.utils import base64_encode_url
from .conftest import TEST_SUPERUSER_EMAIL, TEST_PASSWORD, TEST_WRONG_EMAIL_FORMAT, TEST_PASSWORD, TEST_WRONG_PASSWORD


def login_user(test_client, email, password):
    token = base64_encode_url(email, password)
    headers = {"Authorization": f"Basic {token}"}
    return test_client.post(routes.USER_LOGIN, headers=headers)

def test_exists_email(test_by_superuser):
    res = login_user(test_by_superuser, TEST_SUPERUSER_EMAIL, TEST_PASSWORD)
    assert res.status_code == 200
    
def test_not_exists_email(test_by_superuser):
    res = login_user(test_by_superuser, TEST_WRONG_EMAIL_FORMAT, TEST_PASSWORD)
    assert res.status_code == 400
    
def test_exists_email_with_wrong_password(test_by_superuser):
    res = login_user(test_by_superuser, TEST_SUPERUSER_EMAIL, TEST_WRONG_PASSWORD)
    assert res.status_code == 400