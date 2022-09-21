import copy
import datetime
from re import M
from flask import json
from firebase_admin import auth, _user_mgt
from firebase_admin.auth import UserRecord



    

class FirebaseUser:
    def __init__(self, 
                email=None,
                password=None,
                uid=None,
                display_name=None,
                email_verified=False,
                phone_number=None,
                photo_url=None,
                disabled=False,
                custom_claims=None):
        
        self.email=email
        self.password=password
        self.uid=uid
        self.display_name=display_name
        self.email_verified=email_verified
        self.phone_number=phone_number
        self.photo_url=photo_url
        self.disabled=disabled
        self.custom_claims=custom_claims
    
    def create_user(self):
        current_user = copy.deepcopy(self.__dict__)
        del current_user['custom_claims']
        user_record = auth.create_user(**current_user)
        auth.set_custom_user_claims(uid=user_record.uid, custom_claims=self.custom_claims)
        self.uid = user_record.uid
        return self.get_user()
    
    def get_user(self):
        user_record = auth.get_user(uid=self.uid)
        return self.user_record_to_user(user_record)
    
    def get_users(self):
        users = []
        for user_record in auth.list_users().iterate_all():
            user = self.user_record_to_user(user_record)
            users.append(user)
        return users

    def delete_user(self):
        auth.delete_user(uid=self.uid)
        
    def update_user(self):
        old_user = self.get_user()
        print('old_user', old_user)
        
        update_info = {'uid': self.uid}
        for key in old_user:
            if self.__dict__[key]:
                update_info[key] = self.__dict__[key]
            else:
                update_info[key] = old_user[key]
           
        print('update_info', update_info)
        user_record = auth.update_user(**update_info)
        return self.user_record_to_user(user_record)
    
    def create_session_cookie(self, id_token, expires_in=datetime.timedelta):
        return auth.create_session_cookie(id_token, expires_in=expires_in)
    
    def user_record_to_user(self, user_obj: UserRecord):
        return {
            "email": user_obj.email,
            "uid": user_obj.uid,
            "display_name": user_obj.display_name,
            "email_verified": user_obj.email_verified,
            "phone_number": user_obj.phone_number,
            "photo_url": user_obj.photo_url,
            "disabled": user_obj.disabled,
            "custom_claims": user_obj.custom_claims
        }
        
def update_user():
    old_user = self.get_user()
    print('old_user', old_user)
    
    update_info = {'uid': self.uid}
    for key in old_user:
        if self.__dict__[key]:
            update_info[key] = self.__dict__[key]
        else:
            update_info[key] = old_user[key]
    
    print('update_info', update_info)
    user_record = auth.update_user(**update_info)
    return self.user_record_to_user(user_record)