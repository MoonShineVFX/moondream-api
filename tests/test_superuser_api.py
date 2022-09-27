from .conftest import BaseTestClass
from .constants import SUPERUSER_EMAIL, ADMIN_1_EMAIL, PASSWORD, PASSWORD1


class TestSuperuser(BaseTestClass):
        
    def test_create_superuser_201(self, test_client):
        res = self.user_create_superuser(test_client, SUPERUSER_EMAIL, PASSWORD)
        assert res.status_code == 201

    def test_create_superuser_400(self, test_client):
        res = self.user_create_superuser(test_client, SUPERUSER_EMAIL, PASSWORD)
        assert res.status_code == 400
        
    def test_login_200(self, test_client):
        res = self.user_login(test_client, SUPERUSER_EMAIL, PASSWORD)
        assert res.status_code == 200
        
    def test_create_admin_201(self, test_client):
        res = self.user_create_admin(test_client, ADMIN_1_EMAIL, PASSWORD)
        assert res.status_code == 201
     
    def test_create_admin_400(self, test_client):
        res = self.user_create_admin(test_client, ADMIN_1_EMAIL, PASSWORD)
        assert res.status_code == 400
    
    def test_list_users_200(self, test_client):
        res = self.user_list_users(test_client)
        assert res.status_code == 200

    def test_update_user_200(self, test_client):
        uid = self.get_user_uid(ADMIN_1_EMAIL)
        res = self.user_update_user(test_client, uid, PASSWORD1)
        assert res.status_code == 200
        
    def test_reset_current_user_password_302(self, test_client):
        res = self.user_reset_current_user_password(test_client)
        return res.status_code == 302

    def test_delete_admin_200(self, test_client):
        uid = self.get_user_uid(ADMIN_1_EMAIL)
        res = self.user_delete_user(test_client, uid)
        return res.status_code == 200

    def test_delete_superuser_200(self, test_client):
        uid = self.get_user_uid(SUPERUSER_EMAIL)
        res = self.user_delete_user(test_client, uid)
        return res.status_code == 200

   
        