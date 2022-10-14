from flask import jsonify, send_file, redirect

from api.constants import IMAGE_TYPE, VIDEO_TYPE
from api.model.file import FileModel
from api.resources.base import BaseResource

from doge_api.models.session import SessionModel
from ..decoration import doge_auth_required
from ..schemas.doge_file import FileSchema, UploadFilesSchema


class FilesBase(BaseResource, FileModel):
    type = "undefined"     
    
    @doge_auth_required
    def post(self, user_id=""):
        try:
            file = self.parse_request_file()
            thumb_file = self.parse_request_file(key="thumb")
            
            if not self.is_image_or_video_files(files=[file, thumb_file]):
                raise TypeError("Only images and videos are allowed")
            
            form_dict = self.parse_request_data(UploadFilesSchema())
            session_id = form_dict["session_id"] or ""
            create = int(form_dict["created_at"].timestamp())
            
            destination_path = self.create_destination_path(type=self.type, name=file.filename)
            file_blob = self.upload_file_to_storage(destination_path, file, file.content_type)
            
            thumb_filename = self.create_thumb_name(file.filename)
            thumb_destination_path = self.create_destination_path(type=self.type, name=thumb_filename)
            thumb_blob = self.upload_file_to_storage(thumb_destination_path, thumb_file, file.content_type)

            data_dict = self.create_file_dict(
                create=create, 
                type=self.type, 
                path=destination_path, 
                size=file_blob.size,
                file_name=file.filename, 
                file_url=file_blob.public_url, 
                thumb_url=thumb_blob.public_url, 
                user_id=user_id, 
                session_id=session_id
            )
            
            json_dict = FileSchema().dump(data_dict)
            self.create_file_document_to_firestore(json_dict)
            return {"url_code": json_dict["id"]}
        except Exception as e:
            return jsonify(e)
        
class DogePhoto(FilesBase):
    type = IMAGE_TYPE
    
class DogeVideo(FilesBase):
    type = VIDEO_TYPE
    
    
class FileDownload(BaseResource, FileModel, SessionModel):
    def get(self, doc_id):
        
        data_dict = self.get_file(doc_id)
        print(data_dict)
        return redirect(data_dict["fileURL"])
        # download_name = doc_id + ".zip"
        # memory_file = self.create_zip(paths=[data_dict["path"]])
        # return send_file(memory_file, download_name=download_name, as_attachment=True )
    
class DogePhotosDownload(FileDownload):
    pass

class DogeVideoDownload(FileDownload):
    pass