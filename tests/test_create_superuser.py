from . import constants as c
from api import routes
from flask import json


class TestCreateSuperuser:
    def create_superuser(self, test_client, email, password):
        req_dict = {
            "email": email,
            "password": password
        }
        json_dict = json.dumps(obj=req_dict)
        
        return test_client.post(routes.USER_CREATE_SUPERUSER, data=json_dict or {}, content_type='application/json')
    
    def test_201(self, test_client):
        res = self.create_superuser(test_client, c.SUPERUSER_1, c.PASSWORD_1)
        assert res.status_code == 201
        
    def test_create_superuser_with_exists_eamil_400(self, test_client):
        res = self.create_superuser(test_client, c.SUPERUSER_1, c.PASSWORD_1)
        assert res.status_code == 400

    def test_wrong_email_format_400(self, test_client):
        res = self.create_superuser(test_client, "wrong_email_format", c.PASSWORD_1)
        assert res.status_code == 400
        
    
        
    
    
