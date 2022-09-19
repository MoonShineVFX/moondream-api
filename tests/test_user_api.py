import base64
import os
from flask import Response


class TestGroup:
    TEST_EMAIL = os.getenv('TEST_EMAIL')
    TEST_PASSWORD = os.getenv('TEST_PASSWORD')
    USER_UID = ''
    COOKIE = ''

    def test_sign_up_as_admin(self, test_client):
        data = {"email": self.TEST_EMAIL, "password": self.TEST_PASSWORD}
        res: Response = test_client.post('/user/sign_up_as_admin', data=data)
        self.COOKIE = res.headers['Set-Cookie']
        self.USER_UID = res.data['uid']
        print(res)
        assert res.status_code == 200

    def test_sign_up_as_admin_with_exist_email(self, test_client):
        data = {"email": self.TEST_EMAIL, "password": self.TEST_PASSWORD}
        res: Response = test_client.post('/user/sign_up_as_admin', data=data)
        assert res.status_code == 400

    def test_login(self, test_client):
        s = self.TEST_EMAIL + ":" + self.TEST_PASSWORD
        token = base64.b64encode(s.encode())
        print(token)
        Headers = {"Authorization": f"Basic {token}"}
        res: Response = test_client.post(
            '/user/sign_up_as_admin', headers=Headers)
        self.COOKIE = res.headers['Set-Cookie']

        assert res.status_code == 200
        assert self.USER_UID == res.data['uid']

    def test_reset_password(self, test_client):
        res: Response = test_client.post(
            '/user/reset_password', data={'email': self.TEST_EMAIL})
        assert res.status_code == 302

    def test_list_admins(self, test_client):
        header = {"cookie": self.COOKIE}
        res = test_client.get('/user/list_admins', header=header)
        assert res.status_code == 200

    def test_delete_user(self, test_client):
        header = {"cookie": self.COOKIE}
        res = test_client.post('/user/delete_user',
                               data={'uid': self.USER_UID}, header=header)
        assert res.status_code == 200
