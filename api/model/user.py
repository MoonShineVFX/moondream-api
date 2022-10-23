from datetime import datetime, timedelta

from firebase import Auth
from firebase_admin.auth import UserRecord


class UserModel(Auth):
    def create_custom_claims(self, role):
        return {"role": role}

    def create_user(self, role, email, password, email_verified, uid=None):
        custom_claims = self.create_custom_claims(role)
        user: UserRecord = self.auth.create_user(uid=uid, email=email, password=password, email_verified=email_verified)
        self.auth.set_custom_user_claims(uid=user.uid, custom_claims=custom_claims)
        
        return self.get_user(user.uid)
    
    def get_user_record_dict(self, user: UserRecord):
        return {
            "custom_claims": user.custom_claims,
            "disabled": user.disabled,
            "email": user.email,
            "uid": user.uid
        }
        

    def get_user(self, uid):
        user = self.auth.get_user(uid=uid)
        return self.get_user_record_dict(user)
    
    def get_user_by_email(self, email):
        user = self.auth.get_user_by_email(email=email)
        return self.get_user_record_dict(user)
    
    def list_users_record(self):
        return self.auth.list_users().iterate_all()

    def list_users(self):
        return [self.get_user_record_dict(user_record) for user_record in self.list_users_record()]

    def delete_users(self, uids=[]):
        self.auth.delete_users(uids)

    def delete_user(self, uid):
        self.auth.delete_user(uid)
    
    def login_user(self, email, password):
        user = self.client_auth.sign_in_with_email_and_password(email, password)
        id_token = user["idToken"]
        return self.get_user(user["localId"]), id_token

    def update_user(self, uid, update_dict = {}):
        user = self.get_user(uid)
        
        for key, value in update_dict.items():
            if value:
                user[key] = value
                
        new_user_record = self.auth.update_user(**user)
        return self.get_user_record_dict(new_user_record)

    def reset_password(self, email):
        return self.auth.generate_password_reset_link(email=email)
    
    def create_cookie(self, key, value, expires, httponly=True, secure=True, samesite="None"):
        return {
            "key": key,
            "value": value,
            "expires":expires,
            "httponly":httponly, 
            "secure":secure, 
            "samesite":samesite
        }

    def create_session_cookie(self, key, id_token, expires_days=5):
        expires_in = timedelta(days=expires_days)
        expires = datetime.now() + expires_in
        session_cookie = self.auth.create_session_cookie(id_token, expires_in=expires_in)
        return self.create_cookie(key=key, value=session_cookie, expires=expires)

    def disable_session_cookie(self, key):
        return self.create_cookie(key=key, value="", expires=0)