import re
from flask import redirect, json

from .base import BaseResource
from api.constants import SESSION_ID_NAME, Role
from api.schemas.user import CreateUserSechma, UidRequiredSechma, UserBaseSechma
from api.decoration import login_required, admin_required, superuser_required
from api.model.user import UserModel

from api.utils import output_json


class GetUser(BaseResource, UserModel):
    @login_required
    def post(self, user_id, email):
        try:
            user = self.get_user(user_id)
            data = UserBaseSechma().dump(user)
            return self.handle_success_response(data=data)
        except Exception as e:
            return self.handle_errors_response(e)
    
      
class LoginUser(BaseResource, UserModel):
    def post(self):
        try:
            email, password = self.parse_request_authorization()
            user, id_token = self.login_user(email, password)
            data = UserBaseSechma().dump(user)
            
            response = self.handle_success_response(data=data)
            cookie = self.create_session_cookie(SESSION_ID_NAME,id_token, 5)
            response.set_cookie(**cookie)
            return response
          
        except Exception as e:
            print(e.__class__)
            e_dict = json.loads(re.search('({(.|\s)*})', str(e)).group(0).replace("'", '"'))
            error = e_dict['error']
           
            return output_json(data={"message":error['message']}, code=error['code'])
      
        
class LogoutUser(BaseResource, UserModel):
    @login_required
    def post(self, *args, **kwargs):
        try:
            cookie = self.disable_session_cookie(SESSION_ID_NAME)
            response = self.handle_success_response()
            response.set_cookie(**cookie)
            return response
        except Exception as e:
            return self.handle_errors_response(e)
            
            
class CreateSuperuser(BaseResource, UserModel):
    def post(self):
        try:
            json_dict = self.parse_request_data(CreateUserSechma())
            user = self.create_user(
                    role=Role.SUPERUSER,
                    email=json_dict['email'],
                    password=json_dict['password'] ,
                    email_verified=True
                )
            data = CreateUserSechma().dump(user)
            return self.handle_success_response(code=201, data=data)
        except Exception as e:
            return self.handle_errors_response(e)


class CreateAdmin(BaseResource, UserModel):
    @superuser_required
    def post(self, user_id, email):
        try:
            json_dict = self.parse_request_data(CreateUserSechma())
            user = self.create_user(
                    role=Role.ADMIN,
                    email=json_dict['email'],
                    password=json_dict['password'] ,
                    email_verified=True
                )
            data = CreateUserSechma().dump(user)
            return self.handle_success_response(code=201, data=data)
        except Exception as e:
            return self.handle_errors_response(e)
            

class CreateClient(BaseResource, UserModel):
    @admin_required
    def post(self, user_id, email):
        try:
            json_dict = self.parse_request_data(CreateUserSechma())
            user = self.create_user(
                    role=Role.CLIENT,
                    email=json_dict['email'],
                    password=json_dict['password'] ,
                    email_verified=False
                )
            data = CreateUserSechma().dump(user)
            return self.handle_success_response(code=201, data=data)
        except Exception as e:
            return self.handle_errors_response(e)


class ResetCurrentUserPassword(BaseResource, UserModel):
    @login_required
    def post(self, user_id, email):
        try:
            url = self.reset_password(email)
            return redirect(url)
        except Exception as e:
            return self.handle_errors_response(e)

  

class UpdateUser(BaseResource, UserModel):
    @superuser_required
    def post(self, user_id, email):
        try:
            json_dict = self.parse_request_data(UidRequiredSechma())
            user = self.update_user(uid=json_dict["uid"], update_dict=json_dict)
            data = UidRequiredSechma().dump(user)
            return self.handle_success_response(data=data)
        except Exception as e:
            return self.handle_errors_response(e)

  
class ListUsers(BaseResource, UserModel):
    @admin_required
    def post(self, user_id, email):
        try:
            records = self.list_users_record()
            list = []
            for user_record in records:
                user = self.get_user_record_dict(user_record)
                json_dict = UserBaseSechma().dump(user)
                list.append(json_dict)
            
            return self.handle_success_response(data={"list": list})
        except Exception as e:
            return self.handle_errors_response(e)


class DeleteAllUsers(BaseResource, UserModel):
    @superuser_required
    def post(self, *args, **kwargs):
        try:
            records = self.list_users_record()
            uids = [user_record.uid for user_record in records]
            self.delete_users(uids=uids)
            return self.handle_success_response()
        except Exception as e:
            return self.handle_errors_response(e)
        
    
class DeleteUser(BaseResource, UserModel):
    @superuser_required
    def post(self, *args, **kwargs):
        try:
            json_dict = self.parse_request_data(UidRequiredSechma())
            self.delete_user(uid=json_dict["uid"])
            return self.handle_success_response()
        except Exception as e:
            return self.handle_errors_response(e)