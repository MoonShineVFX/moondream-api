import pytest
import base64
from flask import json
from firebase_admin import auth
from app import create_app, routes

@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()
    flask_app.config["TESTING"] = True

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!
            



class BaseTestClass:
    def get_json(self, res):
        return json.loads(res.data)
    
    def get_response(self, test_client, route, req_dict={}):
        json_dict = json.dumps(obj=req_dict)
        return test_client.post(route, data=json_dict or {}, content_type='application/json')
    
    def get_user_uid(self, email):
        user = auth.get_user_by_email(email)
        return user.uid

    def user_create_superuser(self, test_client, email, password):
        req_dict = {
            "email": email,
            "password": password
        }
        return self.get_response(test_client, routes.USER_CREATE_SUPERUSER, req_dict)
    
    def user_delete_all_users(self, test_client):
        return self.get_response(test_client, routes.USER_DELETE_ALL_USERS)
    
    def user_login(self, test_client, email, password):
        s = email + ":" + password
        b = s.encode()
        e = base64.b64encode(b)
        token = e.decode()
        headers = {"Authorization": f"Basic {token}"}
        return test_client.post(routes.USER_LOGIN, headers=headers)
    
    def user_logout(self, test_client):
        return self.get_response(test_client, routes.USER_LOGOUT)

    def user_create_admin(self, test_client, email, password):
        req_dict = {
            "email": email,
            "password": password
        }
        return self.get_response(test_client, routes.USER_CREATE_ADMIN, req_dict)
        
    def user_list_users(self, test_client):
        return self.get_response(test_client, routes.USER_LIST_USERS)

    def user_update_user(self, test_client, uid, password):
        req_dict = {
            "uid": uid,
            "password": password
        }
        return self.get_response(test_client, routes.USER_UPDATE_USER, req_dict)
    

    def user_reset_current_user_password(self, test_client):
        return self.get_response(test_client, routes.USER_RESET_CURRENT_USER_PASSWORD)

    def user_delete_user(self, test_client, uid):
        req_dict = {
            "uid": uid
        }
        return self.get_response(test_client, routes.USER_DELETE_USER, req_dict)
    
    
    def file_list_files(self, test_client, begin, end):
        req_dict = {
            "begin": begin,
            "end": end
        }
        return self.get_response(test_client, routes.FILE_LIST_FILES, req_dict)
    
    
    def file_download_zip(self, test_client, paths = []):
        req_dict = {
            "paths": paths
        }
        return self.get_response(test_client, routes.FILE_DOWNLOAD_ZIP, req_dict)
        
    
    def file_delete_files(self, test_client, paths):
        req_dict = {
            "paths": paths
        }
        return self.get_response(test_client, routes.FILE_DELETE_FILES, req_dict)
    
    def file_upload_files(self, test_client, files, session_id):
        pass
