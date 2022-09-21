import io
import zipfile
from datetime import datetime, time
from flask import send_file
from firebase_admin import firestore, storage

from .base import BaseResource
from ..constants import FILE_COLLECTION_NAME, ALLOWED_IMAGE_EXTENSIONS, IMAGE_TYPE, ALLOWED_VIDEO_EXTENSIONS, VIDEO_TYPE
from ..decoration import admin_required, login_required
from ..schemas.file import FileQuerySchema, PathsOfFilesSchema, UploadFilesSchema
from ..models.file import handle_file_upload

db = firestore.client()
file_col = db.collection(FILE_COLLECTION_NAME)
bucket = storage.bucket()


class ListFiles(BaseResource):
    @login_required
    def post(self, *args, **kwargs):
        try:
            form = self.parse_request_files(FileQuerySchema())
            print(form)
            begin = int(begin) or int(datetime.combine(datetime.now(), time.min).timestamp())
            end = end(int) or int(datetime.combine(datetime.now(), time.max).timestamp())
            ref = file_col.where('create', '>=', begin).where('create', '<=', end).order_by("create", direction=firestore.Query.DESCENDING).get()
            docs = [doc.to_dict() for doc in ref]
            return self.handle_success_response(data={"list": docs})
        except Exception as e:
            return self.handle_errors_response(e)
    
class DownloadFiles(BaseResource):
    @login_required
    def post(self, *args, **kwargs):
        try:
            form = self.parse_request_form(PathsOfFilesSchema())
            memory_file = io.BytesIO()
            compress_type = zipfile.ZIP_DEFLATED
            with zipfile.ZipFile(memory_file, 'w') as zf:
                for path in form['paths']:
                    file_name = path.rsplit('/', 1)[1]
                    blob = bucket.blob(path)
                    data = blob.download_as_bytes()
                    zf.writestr(file_name, data=data,compress_type=compress_type)
            memory_file.seek(0)
            return send_file(memory_file, download_name='capsule.zip', as_attachment=True)
        except Exception as e:
            return self.handle_errors_response(e)
        
class DeleteFiles(BaseResource):
    @admin_required
    def post(self, *args, **kwargs):
        try:
            form = self.parse_request_form()
            paths = form['paths']
            file_docs = file_col.where('path', 'in', paths).get()
            for doc in file_docs:
                doc.delete()
                
            
            blobs = []
            for path in paths:
                blob = bucket.blob(path)
                blobs.append(blob)
                
            bucket.delete_blobs(blobs)
            
            return self.handle_success_response()
        except Exception as e:
            return self.handle_errors_response(e)
            
class UploadFiles(BaseResource):
    @admin_required
    def post(self, user_id, email):
        try:
            form = self.parse_request_form(UploadFilesSchema())
            session_id = form['session_id'] or ""
            files = self.parse_request_files()
            create = int(datetime.now().timestamp())
            
            datas = []
            for file in files:
                datas.append(handle_file_upload(file, user_id, create, session_id))
            
            return self.handle_success_response(data={'list': datas})
        except Exception as e:
            return self.handle_errors_response(e)
        
