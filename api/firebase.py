import os
import uuid
import io
import zipfile
from datetime import datetime, timedelta

from flask import json
from PIL import Image

import pyrebase
from firebase_admin import credentials, initialize_app, auth, firestore, storage
from firebase_admin.auth import UserRecord
from .constants import FILE_COLLECTION_NAME, IMAGE_TYPE, VIDEO_TYPE, THUMBNAIL_SIZE, ALLOWED_IMAGE_EXTENSIONS, ALLOWED_VIDEO_EXTENSIONS
from .schemas.file import FileSchema


APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_PATH = os.environ.get("FOLDER_PATH", "firebase")

FIREBASE_CONFIG_FILENAME = os.environ.get("FIREBASE_CONFIG_FILENAME", "firebase_config.json")
firebase_config_path = os.path.join(APP_ROOT,  FOLDER_PATH,  FIREBASE_CONFIG_FILENAME)
firebase_config = json.load(open(firebase_config_path))
firebase_client = pyrebase.initialize_app(config=firebase_config)
client_auth = firebase_client.auth()


SERVICE_ACCOUNT_FILENAME = os.environ.get("SERVICE_ACCOUNT_FILENAME", "service_account.json")
cred = credentials.Certificate(os.path.join(FOLDER_PATH,  SERVICE_ACCOUNT_FILENAME))
default_app = initialize_app(cred, {
    "storageBucket": os.environ.get("STORAGE_BUCKET", "moondream-reality.appspot.com")
})

print("firebae_config:", firebase_config["projectId"])
print("service_account:", default_app.project_id)

class FirebaseUser:

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
        # create JWT
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
        return [self.get_user_record_dict(user_record) for user_record in auth.list_users().iterate_all()]

    def delete_users(self, uids=[]):
        auth.delete_users(uids)

    def delete_user(self, uid):
        auth.delete_user(uid)
        

db = firestore.client()
col_ref = db.collection(FILE_COLLECTION_NAME)
bucket = storage.bucket()

class FirebaseFile:
    def upload_file_to_storage(self, resource_path, destination_path):
        blob = bucket.blob(destination_path)
        blob.upload_from_filename(resource_path)
        return blob

    def create_thumb_name(self, name):
        arr = name.rsplit(".", 1)
        arr[0] += "_thumb"
        return ".".join(arr)
    
    def create_thumb_of_image(self,filename,  destination_prefix) -> str:
        thumb_filename = self.create_thumb_name(filename)
        
        pil_image = Image.open(filename)
        pil_image.thumbnail(size=(pil_image.width//THUMBNAIL_SIZE, pil_image.height//THUMBNAIL_SIZE))
        
        pil_image.save(thumb_filename, format=pil_image.format)
        blob = self.upload_file_to_storage(
            thumb_filename, destination_prefix + thumb_filename)
        os.remove(thumb_filename)
        return blob.public_url


    def handle_file_upload_to_storage(self, file, user_id, create, session_id=""):
        file_ext = file.filename.rsplit(".", 1)[1].lower()

        file_type = None
        if file_ext in ALLOWED_IMAGE_EXTENSIONS:
            file_type = IMAGE_TYPE
        elif file_ext in ALLOWED_VIDEO_EXTENSIONS:
            file_type = VIDEO_TYPE
        else:
            raise Exception("File extension is not allowed")
        
        # save file to locale
        filename = file.filename.replace("/", "_")
        file.save(filename)
        destination_prefix = "/".join([FILE_COLLECTION_NAME, file_type, ""])

        # handle original image
        blob = self.upload_file_to_storage(filename, destination_prefix + filename)

        # Handle thumbnail of image
        thumb_url = ""
        if file_type == IMAGE_TYPE:
            thumb_url = self.create_thumb_of_image(
                filename=filename,
                destination_prefix=destination_prefix
            )
            
        
        doc_dict = {
            "id": uuid.uuid4().hex,
            "create": create,
            "type": file_type,
            "path": destination_prefix + filename,
            "size": blob.size,
            "file_name": filename,
            "file_url": blob.public_url,
            "thumb_url": thumb_url,
            "creator": user_id,
            "session_id": session_id,
        }
        
        os.remove(filename)
        return doc_dict

    def upload_files(self, files, user_id, session_id):
        create = int(datetime.now().timestamp())
        batch = db.batch()
        list = []
        for file in files:
            file_dict = self.handle_file_upload_to_storage(file, user_id, create, session_id)
            json_dict = FileSchema().dump(file_dict)
            batch.set(col_ref.document(json_dict["id"]), json_dict)
            list.append(json_dict)
        batch.commit()
        
        return list

    def get_files(self, begin, end):
        docs = col_ref.where("create", ">=", begin).where("create", "<=", end).order_by("create", direction=firestore.Query.DESCENDING).get()
        return [doc.to_dict() for doc in docs]
    
    def delete_documents(self, paths):
        batch = db.batch()
        docs = col_ref.where("path", "in", paths).get()
        for doc in docs:
            batch.delete(doc.reference)
        batch.commit()
        
        
    def delete_files(self, paths):
        blobs = []
        for path in paths:
            if IMAGE_TYPE in path:
                thumb_path = self.create_thumb_name(path)
                thumb_blob = bucket.blob(thumb_path)
                blobs.append(thumb_blob)
            blob = bucket.blob(path)
            blobs.append(blob)
        bucket.delete_blobs(blobs)
        
    
    def create_zip(self, paths):
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, "w") as zf:
            for path in paths:
                file_name = path.rsplit("/", 1)[1]
                blob = bucket.blob(path)
                data = blob.download_as_bytes()
                zf.writestr(file_name, data=data, compress_type=zipfile.ZIP_DEFLATED)
        memory_file.seek(0)
        
        return memory_file