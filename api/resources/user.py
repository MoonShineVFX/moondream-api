import datetime
from flask import redirect
from firebase_admin import auth
from firebase_admin.auth import UserRecord

from .base import BaseResource
from ..constants import SESSION_ID_NAME, Role
from ..schemas.user import CreateUserSechma, UidRequiredSechma, UserBaseSechma
from ..decoration import login_required, admin_required, superuser_required
from ..firebase import firebase_client
client_auth = firebase_client.auth()


class UserBaseResource(BaseResource):
    def get_user_record_dict(self, user: UserRecord):
        return {
            "custom_claims": user.custom_claims,
            "disabled": user.disabled,
            "email": user.email,
            "uid": user.uid
        }
    
    def create_user(self, role):
        json_dict = self.parse_request_json(CreateUserSechma())
        email_verified = role != Role.CLIENT
        custom_claims = {"role": role}
        user: UserRecord = auth.create_user(email=json_dict["email"], password=json_dict["password"], email_verified=email_verified)
        auth.set_custom_user_claims(uid=user.uid, custom_claims=custom_claims)
        superuser = auth.get_user(uid=user.uid)
        user_record_dict = self.get_user_record_dict(superuser)
        return CreateUserSechma().dump(user_record_dict)
    
      
class LoginUser(UserBaseResource):
    def post(self):
        try:
            email, password = self.parse_request_authorization()
            
            # login in & get user data
            user = client_auth.sign_in_with_email_and_password(email, password)
            id_token = user["idToken"]
            user_record = auth.get_user(uid=user["localId"])
            data = self.get_user_record_dict(user_record)
            
            # create JWT
            expires_in = datetime.timedelta(days=5)
            expires = datetime.datetime.now() + expires_in
            session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
            
            # create response
            response = self.handle_success_response(data=data)
            response.set_cookie(SESSION_ID_NAME, session_cookie,
                                expires=expires, httponly=True, secure=False)
            return response
        except Exception as e:
            return self.handle_errors_response(e)
      
        
class LogoutUser(BaseResource):
    @login_required
    def post(self, *args, **kwargs):
        try:
            response = self.handle_success_response()
            response.set_cookie(SESSION_ID_NAME, "", expires=0)
            return response
        except Exception as e:
            return self.handle_errors_response(e)
            
            
class CreateSuperuser(UserBaseResource):
    def post(self):
        try:
            data = self.create_user(Role.SUPERUSER)
            return self.handle_success_response(status_code=201, data=data)
        except Exception as e:
            return self.handle_errors_response(e)


class CreateAdmin(UserBaseResource):
    @superuser_required
    def post(self, user_id, email):
        try:
            data = self.create_user(Role.ADMIN)
            return self.handle_success_response(status_code=201, data=data)
        except Exception as e:
            return self.handle_errors_response(e)
            

class ResetCurrentUserPassword(BaseResource):
    @login_required
    def post(self, user_id, email):
        try:
            url = auth.generate_password_reset_link(email=email)
            print(url)
            return redirect(url)
        except Exception as e:
            return self.handle_errors_response(e)

  

class UpdateUser(UserBaseResource):
    @superuser_required
    def post(self, user_id, email):
        try:
            json_dict = self.parse_request_json(UidRequiredSechma())
            user_record = auth.get_user(uid=json_dict["uid"])
            user_record_dict = self.get_user_record_dict(user_record)
            for key, value in json_dict.items():
                if value:
                    user_record_dict[key] = value
            print("before", user_record_dict)
            new_user_record = auth.update_user(**user_record_dict)
            user_record_dict = self.get_user_record_dict(new_user_record)
            print("after", user_record_dict)
            data = UidRequiredSechma().dump(user_record_dict)
            
            return self.handle_success_response(data=data)
        except Exception as e:
            return self.handle_errors_response(e)

  
class ListUsers(UserBaseResource):
    @admin_required
    def post(self, user_id, email):
        try:
            list = []
            for user_record in auth.list_users().iterate_all():
                user_record_dict = self.get_user_record_dict(user_record)
                json_dict = UserBaseSechma().dump(user_record_dict)
                list.append(json_dict)
            return self.handle_success_response(data={"list": list})
        except Exception as e:
            return self.handle_errors_response(e)


class DeleteAllUsers(UserBaseResource):
    @superuser_required
    def post(self, *args, **kwargs):
        try:
            uids = [user_record.uid  for user_record in auth.list_users().iterate_all() ]
            auth.delete_users(uids=uids)
            return self.handle_success_response()
        except Exception as e:
            return self.handle_errors_response(e)
        
    
class DeleteUser(BaseResource):
    @superuser_required
    def post(self, *args, **kwargs):
        try:
            json_dict = self.parse_request_json(UidRequiredSechma())
            auth.delete_user(uid=json_dict["uid"])
            return self.handle_success_response()
        except Exception as e:
            return self.handle_errors_response(e)