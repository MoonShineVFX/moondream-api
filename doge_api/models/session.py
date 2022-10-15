from firebase import Firestore
from api.common.constants import IMAGE_TYPE, VIDEO_TYPE
from doge_api.common.constants import SESSION_COLLECTION_NAME
from doge_api.schemas.session import SessionRecordsByRangeSchema


class SessionModel(Firestore):
    col = SESSION_COLLECTION_NAME
    
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