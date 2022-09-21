import datetime
from flask import redirect, json
from firebase_admin import auth
from api.constants import SESSION_ID_NAME, ROLE

from api.models.user import FirebaseUser

from .base import BaseResource
from ..schemas.user import CreateUserSechma, UidRequiredSechma, UserBaseSechma
from ..decoration import login_required, admin_required, superuser_required
from ..firebase import firebase_client
client_auth = firebase_client.auth()




class ResetPassword(BaseResource):
    @login_required
    def post(self, user_id, email):
        try:
            url = auth.generate_password_reset_link(email=email)
            return redirect(url)
        except Exception as e:
            return self.handle_errors_response(e)

        
class LoginUser(BaseResource):
    def post(self):
        try:
            email, password = self.parse_request_authorization()
            user = client_auth.sign_in_with_email_and_password(email, password)
            id_token = user['idToken']
            user['uid'] = user['localId']

            expires_in = datetime.timedelta(days=5)
            session_cookie = auth.create_session_cookie(
                id_token, expires_in=expires_in)

            response = self.handle_success_response(data=user)
            response.status_code = 200
            expires = datetime.datetime.now() + expires_in
            response.set_cookie(SESSION_ID_NAME, session_cookie,
                                expires=expires, httponly=True, secure=False)
            return response
        except Exception as e:
            return self.handle_errors_response(e)
      
        
class UpdateUser(BaseResource):
    @superuser_required
    def post(self, user_id, email):
        try:
            user: FirebaseUser = self.parse_request_form(UidRequiredSechma())
            user.update_user()
            return self.handle_success_response(data=UidRequiredSechma().dump(user.__dict__))
        except Exception as e:
            return self.handle_errors_response(e)

        
        
class CreateAdmin(BaseResource):
    @superuser_required
    def post(self, user_id, email):
        try:
            user: FirebaseUser = self.parse_request_form(CreateUserSechma())
            user.custom_claims = {"role": ROLE['admin']}
            user.email_verified = True
            user.create_user()
            return self.handle_success_response(data=CreateUserSechma().dump(user.__dict__))
        except Exception as e:
            return self.handle_errors_response(e)
            

class CreateSuperuser(BaseResource):
    def post(self):
        try:
            user: FirebaseUser = self.parse_request_form(CreateUserSechma())
            user.custom_claims = {"role": ROLE['superuser']}
            user.email_verified = True
            user.create_user()
            return self.handle_success_response(data=CreateUserSechma().dump(user.__dict__))
        except Exception as e:
            return self.handle_errors_response(e)

class ListUsers(BaseResource):
    @admin_required
    def post(self, user_id, email):
        
        try:
            user = FirebaseUser(uid=user_id, email=email)
            users = user.get_users()
            return self.handle_success_response(data={"list": UserBaseSechma(many=True).dump(users)})
        except Exception as e:
            return self.handle_errors_response(e)

class DeleteAllUsers(BaseResource):
    @superuser_required
    def post(self, *args, **kwargs):
        try:
            users = self.get_users()
            uids = []
            for user in users:
                uids.append(user.uid)
            auth.delete_users(uids=uids)
            return self.handle_success_response()
        except Exception as e:
            return self.handle_errors_response(e)
        
    
class DeleteUser(BaseResource):
    @superuser_required
    def post(self, *args, **kwargs):
        try:
            user = self.parse_request_form(UidRequiredSechma())
            user.delete_user()
            return self.handle_success_response()
        except Exception as e:
            return self.handle_errors_response(e)
        