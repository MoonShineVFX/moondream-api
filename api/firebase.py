import os
from flask import json
import pyrebase
from firebase_admin import credentials, initialize_app, auth, firestore, storage

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

class Firebase:
    client_auth = firebase_client.auth()
    auth = auth
    firestore = firestore.client()
    bucket = storage.bucket()
#     col = ""
#     def create_id(self):
#         return uuid.uuid4().hex
    
#     def get_col_ref(self):
#         return db.collection(self.col)
    
#     def convert_doc_to_dict(self, doc):
#         return doc.to_dict()
    
#     def get_doc_ref(self, id):
#         return self.get_col_ref().document(id)
    
#     def get_doc(self, id):
#         return self.get_doc_ref(id).get()
    
#     def get_docs(self):
#         return self.get_col_ref().get()
    
#     def get_doc_dict(self, id):
#         doc = self.get_doc(id)
#         return self.convert_doc_to_dict(doc)

#     def query_docs_by_timestamp(self, begin, end):
#         return self.get_col_ref().where("create", ">=", begin).where("create", "<=", end).order_by("create", direction=firestore.Query.DESCENDING).get()
    
#     def query_session_by_date_and_order(self, timestamp, order):
#         docs = self.get_col_ref().where("start_at", ">=", timestamp).where("order_today", "==", order).limit(1).get()
#         if docs:
#             return self.convert_doc_to_dict(docs[0])
#         return None    
#     def set_doc(self, id, data_dict):
#         doc = self.get_doc_ref(id)
#         doc.set(data_dict)
    
#     def update_doc(self, id, data_dict):
#         doc = self.get_doc_ref(id)
#         doc.update(data_dict)
        
#     def delete_doc(self, id):
#         doc = self.get_doc_ref(id)
#         doc.delete()
        
    