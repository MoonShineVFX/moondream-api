import base64
from flask import json
from api import routes

class BaseTestClass:
    def get_response(self, test_client, route, data=""):
        res = test_client.post(route, data=data)
        data = json.loads(res.data)
        print(res.status_code, data)
        return res, data
    

    def user_create_superuser(self, test_client, email, password):
        data = json.dumps(obj={
            "email": email,
            "password": password
        })
        return self.get_response(test_client, routes.USER_CREATE_SUPERUSER, data)
    
    def user_delete_all_users(self, test_client):
        return self.get_response(test_client, routes.USER_DELETE_ALL_USERS)
    
    def user_login(self, test_client, email, password):
        s = email + ":" + password
        b = s.encode()
        e = base64.b64encode(b)
        token = e.decode()
        Headers = {"Authorization": f"Basic {token}"}
        return test_client.post(routes.USER_LOGIN, headers=Headers)
    
    def user_logout(self, test_client):
        return self.get_response(test_client, routes.USER_LOGOUT)

    def user_create_admin(self, test_client, email, password):
        data = json.dumps(obj={
            "email": email,
            "password": password
        })
        return self.get_response(test_client, routes.USER_CREATE_ADMIN, data)
        
    def user_list_users(self, test_client):
        return self.get_response(test_client, routes.USER_LIST_USERS)

    def user_update_user(self, test_client, password):
        data = json.dumps(obj = {
            "password": password
        })
        return self.get_response(test_client, routes.USER_UPDATE_USER, data)
    

    def user_reset_current_user_password(self, test_client):
        return self.get_response(test_client, routes.USER_RESET_CURRENT_USER_PASSWORD)

    def user_delete_user(self, test_client, uid):
        data = json.dumps(obj = {
            "uid": uid
        })
        return self.get_response(test_client, routes.USER_DELETE_USER, data)
    
    
    def file_list_files(self, test_client, begin, end):
        data = json.dumps(obj={
            "begin": begin,
            "end": end
        })
        return self.get_response(test_client, routes.FILE_LIST_FILES, data)
    
    
    def file_download_zip(self, test_client, paths = []):
        data = json.dumps(obj={
            "paths": paths
        })
        return self.get_response(test_client, routes.FILE_DOWNLOAD_ZIP, data)
        
    
    def file_delete_files(self, test_client, paths):
        data = json.dumps(obj={
            "paths": paths
        })
        return self.get_response(test_client, routes.FILE_DELETE_FILES, data)
    
    def file_upload_files(self, test_client, files, session_id):
        pass





SUPERUSER_EMAIL="superuser@gmail.com"
ADMIN_EMAIL="admin@gamil.com"
PASSWORD="000000"
PASSWORD1="111111"


class TestSuperuser(BaseTestClass):
    email = SUPERUSER_EMAIL
    password = PASSWORD
    superuser_uid = ""
    admin_uid = ""
        
    def test_create_superuser_201(self, test_client):
        res, data = self.user_create_superuser(test_client, self.email, self.password)
        assert res.status_code == 201

    def test_create_superuser_400(self, test_client):
        res, data = self.user_create_superuser(test_client, self.email, self.password)
        assert res.status_code == 400
        
    def test_login_200(self, test_client):
        res, data = self.user_login(test_client, self.email, self.password)
        assert res.status_code == 200
        
    def test_create_admin_201(self, test_client):
        res, data = self.user_create_admin(test_client, ADMIN_EMAIL, self.password)
        self.admin_uid = data["uid"]
        assert res.status_code == 201
     
    def test_create_admin_400(self, test_client):
        res, data = self.user_create_admin(test_client, ADMIN_EMAIL, self.password)
        assert res.status_code == 400
    
    def test_list_users_200(self, test_client):
        res, data = self.user_list_users(test_client, ADMIN_EMAIL, self.password)
        assert res.status_code == 200

    def test_update_user_200(self, test_client):
        res, data = self.user_update_user(test_client, PASSWORD1)
        assert res.status_code == 200
        
    def test_reset_current_user_password_302(self, test_client):
        res, data = self.user_reset_current_user_password(test_client)
        return res.status_code == 302

    def test_delete_user_200(self, test_client):
        res, data = self.user_delete_user(test_client, self.admin_uid)
        return res.status_code == 200

    def test_delete_user_400(self, test_client):
        res, data = self.user_delete_user(test_client, self.admin_uid)
        return res.status_code == 400
        

    
        
    

# class TestSuperuser:
#     email = "test@gmail.com"
#     password = "123456"
    
#     def get_test_data(self):
#         return json.dumps(obj={
#             "email": self.email,
#             "password": self.password
#         })
    
#     def test_create_superuser_201(self, test_client):
#         res = test_client.post(routes.USER_CREATE_SUPERUSER, data=self.get_test_data())
#         print(res.data)
#         assert res.status_code == 201

#     def test_create_superuser_400(self, test_client):
#         res = test_client.post(routes.USER_CREATE_SUPERUSER, data=self.get_test_data())
#         print(res.data)
#         assert res.status_code == 400
        
    
#     def test_login_200(self, test_client):
#         s = self.email + ":" + self.password
#         b = s.encode()
#         e = base64.b64encode(b)
#         token = e.decode()
#         Headers = {"Authorization": f"Basic {token}"}
#         res = test_client.post(routes.USER_LOGIN, headers=Headers)

#         assert res.status_code == 200
        
    
        
#     def test_list_users(test_client):
#         res = test_client.post(routes.USER_LIST_USERS)
#         print(res.data)
#         assert res.status_code == 200
        
        
#     def test_delete_all_users_200(self,test_client):
#         res = test_client.post(routes.USER_DELETE_ALL_USERS)
        
#         assert res.status_code == 200
        