import io
from PIL import Image
import pytest
from app import create_app
from api.common.constants import Role, SESSION_ID_NAME, IMAGE_TYPE
from api.model.user import UserModel
from api.model.file import FileModel
from api.schemas.file import FileSchema


TEST_WRONG_EMAIL_FORMAT = "test_wrong_email_format"
TEST_SUPERUSER_EMAIL = "test_superuser@gmail.com"
TEST_ADMIN_EMAIL = "test_admin@gamil.com"
TEST_CLIENT_EMAIL = "test_client@gmail.com"
TEST_EMAIL = "test_email@gmail.com"
TEST_PASSWORD = "test_password"
TEST_WRONG_PASSWORD = "test_wrong_password"
IMAGE_0 = "0.png"
IMAGE_1 = "1.png"


def t_create_user(role, email, password):
    return UserModel().create_user(
        role=role,
        uid=email, 
        email=email, 
        password=password,
        email_verified= Role.CLIENT != role)
    
def t_delete_user(uid):
    UserModel().delete_user(uid)
    
def t_get_user_by_email(email):
    return UserModel().get_user_by_email(email)
    
def t_login_user(client, email, password):
    user, id_token = UserModel().login_user(email, password)
    cookie = UserModel().create_session_cookie(SESSION_ID_NAME, id_token)
    client.set_cookie("localhost", cookie['key'], cookie['value'])
    return user
    
def t_logout_user(client):
    cookie = UserModel().disable_session_cookie(SESSION_ID_NAME)
    client.set_cookie("localhost", cookie['key'], cookie['value'])
    

def t_create_image(name):
    memory_file = io.BytesIO()
    pil_image = Image.new(mode="RGB", size=(400, 400), color="blue")
    pil_image.save(memory_file, format="PNG")
    memory_file.seek(0)
    memory_file.name = name
    return memory_file

def t_delete_files(names:list):
    paths = [FileModel().create_destination_path(type=IMAGE_TYPE, name=name) for name in names]
    FileModel().delete_files(paths)

def t_upload_images(names:list):
    create = FileModel().get_now_timestamp()
    
    for name in names:
        file = t_create_image(name)
        file_dict = FileModel().handle_image(file,
                                             filename=name, 
                                             content_type="image/png", 
                                             create=create, 
                                             user_id=TEST_SUPERUSER_EMAIL,
                                             session_id=TEST_SUPERUSER_EMAIL)
        
        json_dict = FileSchema().dump(file_dict)
        FileModel().set_doc(id=json_dict["id"], data_dict=json_dict)     
    
def t_get_file_path(name):
    return FileModel().create_destination_path(IMAGE_TYPE, name)



@pytest.fixture(scope="module")
def test_by_superuser():
    role = Role.SUPERUSER
    email = TEST_SUPERUSER_EMAIL
    password = TEST_PASSWORD
    flask_app = create_app()
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as testing_client:
        t_create_user(role, email, password)
        t_login_user(testing_client, email, password)
    
        with flask_app.app_context():
            yield testing_client
            
        t_logout_user(testing_client)
        t_delete_user(uid=email)
    
    
@pytest.fixture(scope="module")
def test_by_admin():
    role = Role.ADMIN
    email = TEST_ADMIN_EMAIL
    password = TEST_PASSWORD
    flask_app = create_app()
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as testing_client:
        t_create_user(role, email, password)
        t_login_user(testing_client, email, password)
    
        with flask_app.app_context():
            yield testing_client
            
        t_logout_user(testing_client)
        t_delete_user(uid=email)
        
        
@pytest.fixture(scope="module")
def test_by_client():
    role = Role.CLIENT
    email = TEST_CLIENT_EMAIL
    password = TEST_PASSWORD
    flask_app = create_app()
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as testing_client:
        t_create_user(role, email, password)
        t_login_user(testing_client, email, password)
    
        with flask_app.app_context():
            yield testing_client
            
        t_logout_user(testing_client)
        t_delete_user(uid=email)
        
        
@pytest.fixture(scope="module")
def test_without_login():
    flask_app = create_app()
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client