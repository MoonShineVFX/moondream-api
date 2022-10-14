from datetime import datetime, timedelta

from api.firebase import client_auth
from firebase_admin import auth
from firebase_admin.auth import UserRecord


class UserModel:

    def get_user_record_dict(self, user: UserRecord):
        return {
            "custom_claims": user.custom_claims,
            "disabled": user.disabled,
            "email": user.email,
            "uid": user.uid
        }
        

    def get_user(self, uid):
        user = auth.get_user(uid=uid)
        return self.get_user_record_dict(user)


    def create_custom_claims(self, role):
        return {"role": role}


    def create_user(self, role, email, password, email_verified, uid=None):
        custom_claims = self.create_custom_claims(role)
        user: UserRecord = auth.create_user(uid=uid, email=email, password=password, email_verified=email_verified)
        auth.set_custom_user_claims(uid=user.uid, custom_claims=custom_claims)
        
        return self.get_user(user.uid)



    def create_cookie(self, key, value, expires, httponly=True, secure=True, samesite="None"):
        return {
            "key": key,
            "value": value,
            "expires":expires,
            "httponly":httponly, 
            "secure":secure, 
            "samesite":samesite
        }


    def disable_session_cookie(self, key):
        return self.create_cookie(key=key, value="", expires=0)


    def create_session_cookie(self, key, id_token, expires_days=5):
        expires_in = timedelta(days=expires_days)
        expires = datetime.now() + expires_in
        session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
        return self.create_cookie(key=key, value=session_cookie, expires=expires)

    def login_user(self, email, password):
        user = client_auth.sign_in_with_email_and_password(email, password)
        id_token = user["idToken"]
        return self.get_user(user["localId"]), id_token


    def reset_password(self, email):
        return auth.generate_password_reset_link(email=email)


    def update_user(self, uid, update_dict = {}):
        user = self.get_user(uid)
        
        for key, value in update_dict.items():
            if value:
                user[key] = value
                
        new_user_record = auth.update_user(**user)
        return self.get_user_record_dict(new_user_record)
            

    def list_users_record(self):
        return auth.list_users().iterate_all()

    def list_users(self):
        return [self.get_user_record_dict(user_record) for user_record in self.list_users_record()]

    def delete_users(self, uids=[]):
        auth.delete_users(uids)

    def delete_user(self, uid):
        auth.delete_user(uid)