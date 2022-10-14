from datetime import datetime
from flask import send_file

from .base import BaseResource
from ..decoration import admin_required, login_required
from ..schemas.file import FileSchema, FileQuerySchema, PathsOfFilesSchema, UploadFilesSchema
from ..model.file import FileModel

class ListFiles(BaseResource, FileModel):
    @login_required
    def post(self, *args, **kwargs):
        try:
            json_dict = self.parse_request_data(FileQuerySchema())
            begin, end = json_dict["begin"], json_dict["end"]
            list = self.get_files(begin, end)
            return self.handle_success_response(data={"list": list})
        except Exception as e:
            return self.handle_errors_response(e)


class DownloadFilesInZip(BaseResource, FileModel):
    # @login_required
    def post(self, *args, **kwargs):
        try:
            json_dict = self.parse_request_data(PathsOfFilesSchema())
            paths = set(json_dict["paths"])
            download_name = datetime.now().strftime("%Y-%m-%d") + ".zip"
            memory_file = self.create_zip(paths)
            
            return send_file(memory_file, download_name=download_name, as_attachment=True )
        except Exception as e:
            return self.handle_errors_response(e)
        
class DeleteFiles(BaseResource, FileModel):
    @admin_required
    def post(self, *args, **kwargs):
        try:
            json_dict = self.parse_request_data(PathsOfFilesSchema())
            paths = set(json_dict["paths"])
            self.delete_files(paths)
            return self.handle_success_response()
        except Exception as e:
            return self.handle_errors_response(e)
            
class UploadFiles(BaseResource, FileModel):
    @admin_required
    def post(self, user_id, email):
        try:
            files = self.parse_request_files()
            if not self.is_image_or_video_files(files):
                raise TypeError("Only images and videos are allowed")
            
            form_dict = self.parse_request_data(UploadFilesSchema())
            session_id = form_dict["session_id"] or ""
            create = int(datetime.now().timestamp())
            
            list = []
            for file in files:
                file_dict=None
                if file.content_type.startswith('image'):
                    file_dict = self.handle_image(file, create, user_id, session_id)
                elif file.content_type.startswith('video'):
                    file_dict = self.handle_video(file, create, user_id, session_id)
                    
                json_dict = FileSchema().dump(file_dict)
                self.create_file_document_to_firestore(json_dict)
                list.append(json_dict)
                
            return self.handle_success_response(code=201, data={"list": list})
        except Exception as e:
            return self.handle_errors_response(e)
        

class UploadFile(BaseResource, FileModel):
    @admin_required
    def post(self, user_id, email):
        try:
            file = self.parse_request_file()
            if not self.is_image_or_video_files(files=[file]):
                raise TypeError("Only images and videos are allowed")
            
            form_dict = self.parse_request_data(UploadFilesSchema())
            session_id = form_dict["session_id"] or ""
            create = int(datetime.now().timestamp())
            
            file_dict=None
            if file.content_type.startswith('image'):
                file_dict = self.handle_image(file, create, user_id, session_id)
            elif file.content_type.startswith('video'):
                file_dict = self.handle_video(file, create, user_id, session_id)
                
            json_dict = FileSchema().dump(file_dict)
            self.create_file_document_to_firestore(json_dict)
            return self.handle_success_response(code=201, data=json_dict)
        except Exception as e:
            return self.handle_errors_response(e)