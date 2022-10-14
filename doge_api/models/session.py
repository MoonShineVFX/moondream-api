import uuid
from datetime import datetime, timedelta

from firebase_admin import firestore, exceptions


from api.constants import IMAGE_TYPE, VIDEO_TYPE
from doge_api.constants import SESSION_COLLECTION_NAME
from doge_api.schemas.session import SessionRecordsByRangeSchema

db = firestore.client()

class SessionModel:
    col = SESSION_COLLECTION_NAME
    
    def create_id(self):
        return uuid.uuid4().hex
    
    def get_col_ref(self):
        return db.collection(self.col)
    
    def convert_doc_to_dict(self, doc):
        return doc.to_dict()
    
    def get_doc_ref(self, id):
        return self.get_col_ref().document(id)
    
    def get_doc(self, id):
        return self.get_doc_ref(id).get()
    
    def get_docs(self):
        return self.get_col_ref().get()
    
    def get_doc_dict(self, id):
        doc = self.get_doc(id)
        return self.convert_doc_to_dict(doc)

    def query_session_by_begin_and_end(self, begin, end):
        docs = self.get_col_ref().where("start_at", "==", begin).where("end_at", "==", end).get()
        if docs:
            return self.convert_doc_to_dict(docs[0])
        return None
    
    def query_session_by_date_and_order(self, timestamp, order):
        docs = self.get_col_ref().where("start_at", ">=", timestamp).where("order_today", "==", order).limit(1).get()
        if docs:
            return self.convert_doc_to_dict(docs[0])
        return None    
    def set_doc(self, id, data_dict):
        doc = self.get_doc_ref(id)
        doc.set(data_dict)
    
    def update_doc(self, id, data_dict):
        doc = self.get_doc_ref(id)
        doc.update(data_dict)
    
    def delete_doc(self, id):
        doc = self.get_doc_ref(id)
        doc.delete()
        
    
    def separate_files(self, files):
        photos, videos = [], []
                
        for file_dict in files:
            if file_dict["type"] == IMAGE_TYPE:
                photos.append(
                    SessionRecordsByRangeSchema().dump(file_dict)
                )
                
            elif file_dict["type"] == VIDEO_TYPE:
                videos.append(
                    SessionRecordsByRangeSchema().dump(file_dict)
                )
        
        return {
            "photos": photos,
            "videos": videos
        }
        
    def convert_UTC(self, datetime):
        return datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        
    def convert_timestamp(self, datetime):
        return int(datetime.timestamp())