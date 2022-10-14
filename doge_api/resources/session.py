from datetime import datetime
from flask import jsonify

from api.model.file import FileModel
from api.resources.base import BaseResource

from doge_api.constants import MOONDREAM_REALITY_CLIENT_SIDE_URL
from doge_api.decoration import doge_auth_required
from doge_api.models.session import SessionModel
from doge_api.schemas.session import SessionBaseSchema, SessionRecordsLinkByRangeSchema, SessionRecordsLinkSchema
from firebase_admin.exceptions import FirebaseError

class Sessions(BaseResource, SessionModel):
    @doge_auth_required
    def get(self):
        try:
            docs = self.get_docs()
            list_dicts = []
            for doc in docs:
                data_dict = self.convert_doc_to_dict(doc)
                json_dict = SessionBaseSchema().dump(data_dict)
                list_dicts.append(json_dict)
                
            return jsonify(list_dicts)
        except Exception as e:
            return self.handle_errors_response(e)
        
    @doge_auth_required
    def post(self):
        try:
            data_dict = self.parse_request_data(SessionBaseSchema())
            session_id = str(data_dict["order_today"])
            data_dict["id"] = session_id
            self.set_doc(session_id, data_dict)
            
            return jsonify(**data_dict)
        except Exception as e:
            return self.handle_errors_response(e)
        


class Session(BaseResource, SessionModel):
    @doge_auth_required
    def get(self, session_id):
        try:
            data_dict = self.get_doc_dict(session_id)
            json_dict = SessionBaseSchema().dump(data_dict)
            return jsonify(**json_dict)
        except Exception as e:
            return self.handle_errors_response(e)

    @doge_auth_required
    def patch(self, session_id):
        # try:
            data_dict = self.parse_request_data(SessionBaseSchema())
            self.update_doc(session_id, data_dict)
            data_dict["id"] = session_id
            json_dict = SessionBaseSchema().dump(data_dict)
            return json_dict, 200
        # except Exception as e:
            
        #     return self.handle_errors_response(e)
        
    @doge_auth_required
    def delete(self, session_id):
        try:
            self.delete_doc(session_id)
            return {}, 204
        except Exception as e:
            return jsonify("The session is used for MDPhoto or MDVideo."), 400
        
        

class SessionRecordsLink(BaseResource, SessionModel):
    @doge_auth_required
    def post(self):
        data_dict = self.parse_request_data(SessionRecordsLinkSchema())
        order = data_dict["order"]
        date = datetime.combine(data_dict["date"], datetime.min.time())
        timestamp = self.convert_timestamp(date)
        session = self.query_session_by_date_and_order(timestamp=timestamp, order=order)
        session_id = session["id"] if session else None
        
        return {
            "url": f"{MOONDREAM_REALITY_CLIENT_SIDE_URL}?session_id={session_id}&token={timestamp}"
        }
        
            
class SessionRecordsLinkByRange(BaseResource, SessionModel):
    @doge_auth_required
    def post(self):
        data_dict = self.parse_request_data(SessionRecordsLinkByRangeSchema())
        start = data_dict["start"]
        end = data_dict["end"]
        start_UTC = self.convert_UTC(start) 
        end_UTC = self.convert_UTC(end)
        end_timestamp = self.convert_timestamp(end)
        return {
            "url": f"{MOONDREAM_REALITY_CLIENT_SIDE_URL}/session_records?start={start_UTC}&end={end_UTC}&token={end_timestamp}"
        }
        
        
class SessionRecords(BaseResource, SessionModel, FileModel):
    def get(self, session_id):
        try:
            doc_dict = self.get_doc_dict(session_id)
            file_dicts = self.get_files(begin=doc_dict["start_at"], end=doc_dict["end_at"])
            data = self.separate_files(file_dicts)
            return data
        except Exception as e:
                return e
        
        
class SessionRecordsByRange(BaseResource, SessionModel, FileModel):
    def get(self):
        try:
            data_dict = self.parse_request_data(SessionRecordsLinkByRangeSchema())
            start = data_dict["start"]
            end = data_dict["end"]
            start_timestamp = self.convert_timestamp(start)
            end_timestamp = self.convert_timestamp(end)
            files = self.get_files(begin=start_timestamp, end=end_timestamp)
            data = self.separate_files(files)
            return data
            
        except Exception as e:
            return e
        
        
