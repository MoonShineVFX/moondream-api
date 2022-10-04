import time
import pytest
from app import create_app
from .utils import f_create_user, f_delete_users, SUPERUSER_0, ADMIN_0, CLIENT_0, PASSWORD_0
from api.constants import Role

def init_users():
    f_create_user(
        role=Role.SUPERUSER,
        email=SUPERUSER_0, 
        password=PASSWORD_0
    )
    f_create_user(
        role=Role.ADMIN,
        email=ADMIN_0, 
        password=PASSWORD_0,
    )
    f_create_user(
        role=Role.CLIENT,
        email=CLIENT_0, 
        password=PASSWORD_0,
    )
    
        
@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()
    flask_app.config["TESTING"] = True

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        init_users()
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!
        f_delete_users(uids=[SUPERUSER_0, ADMIN_0, CLIENT_0])
    
   
@pytest.fixture(autouse=True)
def patch_sleep():
    yield
    print("sleep 1s")
    time.sleep(1)