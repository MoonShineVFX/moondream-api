import os
import re
import uuid
from flask import json
import pyrebase
from firebase_admin import credentials, initialize_app, auth, firestore, storage


APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_PATH = os.environ.get("FOLDER_PATH", "firebase")

FIREBASE_CONFIG_FILENAME = os.environ.get("FIREBASE_CONFIG_FILENAME", "firebase_config.json")
firebase_config_path = os.path.join(APP_ROOT,  FOLDER_PATH,  FIREBASE_CONFIG_FILENAME)
firebase_config = json.load(open(firebase_config_path))
firebase_client = pyrebase.initialize_app(config=firebase_config)

SERVICE_ACCOUNT_FILENAME = os.environ.get("SERVICE_ACCOUNT_FILENAME", "service_account.json")
cred = credentials.Certificate(os.path.join(FOLDER_PATH,  SERVICE_ACCOUNT_FILENAME))
default_app = initialize_app(cred, {
    "storageBucket": os.environ.get("STORAGE_BUCKET", "moondream-reality.appspot.com")
})

print("firebae_config:", firebase_config["projectId"])
print("service_account:", default_app.project_id)


class Auth:
    client_auth=firebase_client.auth()
    auth=auth
    
    def get_error_message_and_code(self, e):
        e_dict = json.loads(re.search('({(.|\s)*})', str(e)).group(0).replace("'", '"'))
        error = e_dict['error']
        return error['message'], error['code']

    
class Storage:
    bucket = storage.bucket()
    
    def upload_file_to_storage(self, destination_path, file, content_type):
        blob = self.bucket.blob(destination_path)
        blob.upload_from_file(file, content_type=content_type)
        return blob
   
    def delete_blobs_by_paths(self, paths):
        blobs = []
        for path in paths:
            blob = self.bucket.blob(path)
            if blob.exists():
                blobs.append(blob)
            thumb_path = self.create_thumb_name(path)
            thumb_blob = self.bucket.blob(thumb_path)
            if thumb_blob.exists():
                blobs.append(thumb_blob)
            
        self.bucket.delete_blobs(blobs)

class Firestore:
    DESCENDING = firestore.Query.DESCENDING
    db = firestore.client()
    col = ""
    
    def create_id(self):
        return uuid.uuid4().hex
    
    def convert_doc_to_dict(self, doc):
        return doc.to_dict()
    
    def get_col_ref(self):
        return self.db.collection(self.col)
    
    def get_all_docs(self):
        return self.get_col_ref().get()
    
    def get_doc_ref(self, id):
        return self.get_col_ref().document(id)
    
    def get_doc(self, id):
        return self.get_doc_ref(id).get()
    
    def get_doc_dict(self, id):
        doc = self.get_doc(id)
        return self.convert_doc_to_dict(doc)

    def set_doc(self, id, data_dict):
        doc = self.get_doc_ref(id)
        doc.set(data_dict)
    
    def update_doc(self, id, data_dict):
        doc = self.get_doc_ref(id)
        doc.update(data_dict)
        
    def delete_doc(self, id):
        doc = self.get_doc_ref(id)
        doc.delete()
        
    def delete_docs(self, docs):
        batch = self.db.batch()
        for doc in docs:
            batch.delete(doc.reference)
        batch.commit()