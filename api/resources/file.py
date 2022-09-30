from datetime import datetime
from flask import send_file

from .base import BaseResource
from ..decoration import admin_required, login_required
from ..schemas.file import FileQuerySchema, PathsOfFilesSchema, UploadFilesSchema
from ..firebase import FirebaseFile

class ListFiles(BaseResource, FirebaseFile):
    @login_required
    def post(self, *args, **kwargs):
        try:
            json_dict = self.parse_request_json(FileQuerySchema())
            begin, end = json_dict["begin"], json_dict["end"]
            list = self.get_files(begin, end)
            return self.handle_success_response(data={"list": list})
        except Exception as e:
            return self.handle_errors_response(e)


class DownloadFilesInZip(BaseResource, FirebaseFile):
    # @login_required
    def post(self, *args, **kwargs):
        try:
            json_dict = self.parse_request_json(PathsOfFilesSchema())
            paths = set(json_dict["paths"])
            download_name = datetime.now().strftime("%Y-%m-%d") + ".zip"
            memory_file = self.create_zip(paths)
            
            return send_file(memory_file, download_name=download_name, as_attachment=True )
        except Exception as e:
            return self.handle_errors_response(e)
        
class DeleteFiles(BaseResource, FirebaseFile):
    @admin_required
    def post(self, *args, **kwargs):
        try:
            json_dict = self.parse_request_json(PathsOfFilesSchema())
            paths = set(json_dict["paths"])
            self.delete_documents(paths)
            self.delete_files(paths)
            return self.handle_success_response()
        except Exception as e:
            return self.handle_errors_response(e)
            
class UploadFiles(BaseResource, FirebaseFile):
    @admin_required
    def post(self, user_id, email):
        try:
            files = self.parse_request_files()
            form_dict = self.parse_request_form(UploadFilesSchema())
            session_id = form_dict["session_id"] or ""
            
            list = self.upload_files(files, user_id, session_id)
            return self.handle_success_response(data={"list": list})
        except Exception as e:
            return self.handle_errors_response(e)
        
