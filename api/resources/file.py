import io
import os
import uuid
import zipfile
from datetime import datetime
from flask import send_file
from firebase_admin import firestore, storage
from PIL import Image

from .base import BaseResource
from ..decoration import admin_required, login_required
from ..schemas.file import FileSchema, FileQuerySchema, PathsOfFilesSchema, UploadFilesSchema
from ..constants import FILE_COLLECTION_NAME, IMAGE_TYPE, VIDEO_TYPE, THUMBNAIL_SIZE, ALLOWED_IMAGE_EXTENSIONS, ALLOWED_VIDEO_EXTENSIONS

db = firestore.client()
col_ref = db.collection(FILE_COLLECTION_NAME)
bucket = storage.bucket()


class FileBaseResource(BaseResource):
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
    
        

class ListFiles(FileBaseResource):
    @login_required
    def post(self, *args, **kwargs):
        try:
            json_dict = self.parse_request_json(FileQuerySchema())
            begin, end = json_dict["begin"], json_dict["end"]
            docs = col_ref.where("create", ">=", begin).where("create", "<=", end).order_by("create", direction=firestore.Query.DESCENDING).get()
            list = [doc.to_dict() for doc in docs]
           
            return self.handle_success_response(data={"list": list})
        except Exception as e:
            return self.handle_errors_response(e)
    
class DownloadFilesInZip(FileBaseResource):
    @login_required
    def post(self, *args, **kwargs):
        try:
            json_dict = self.parse_request_json(PathsOfFilesSchema())
            
            memory_file = io.BytesIO()
            download_name = datetime.now().strftime("%Y-%m-%d") + ".zip"
            compress_type = zipfile.ZIP_DEFLATED
            with zipfile.ZipFile(memory_file, "w") as zf:
                for path in json_dict["paths"]:
                    file_name = path.rsplit("/", 1)[1]
                    blob = bucket.blob(path)
                    data = blob.download_as_bytes()
                    zf.writestr(file_name, data=data,compress_type=compress_type)
            memory_file.seek(0)
            return send_file(memory_file, download_name=download_name, as_attachment=True)
        except Exception as e:
            return self.handle_errors_response(e)
        
class DeleteFiles(FileBaseResource):
    @admin_required
    def post(self, *args, **kwargs):
        try:
            json_dict = self.parse_request_json(PathsOfFilesSchema())
            paths = json_dict["paths"]
            
            # Delete firestore documents
            batch = db.batch()
            docs = col_ref.where("path", "in", paths).get()
            for doc in docs:
                batch.delete(doc.reference)
            batch.commit()
            
            # Delete storage files
            blobs = []
            for path in paths:
                if IMAGE_TYPE in path:
                    thumb_path = self.create_thumb_name(path)
                    thumb_blob = bucket.blob(thumb_path)
                    blobs.append(thumb_blob)
                blob = bucket.blob(path)
                blobs.append(blob)
            bucket.delete_blobs(blobs)
            
            return self.handle_success_response()
        except Exception as e:
            return self.handle_errors_response(e)
            
class UploadFiles(FileBaseResource):
    @admin_required
    def post(self, user_id, email):
        try:
            files = self.parse_request_files()
            form_dict = self.parse_request_form(UploadFilesSchema())
            session_id = form_dict["session_id"] or ""
            create = int(datetime.now().timestamp())
            batch = db.batch()
            list = []
            for file in files:
                file_dict = self.handle_file_upload_to_storage(file, user_id, create, session_id)
                json_dict = FileSchema().dump(file_dict)
                batch.set(col_ref.document(json_dict["id"]), json_dict)
                list.append(json_dict)
            batch.commit()
            
            return self.handle_success_response(data={"list": list})
        except Exception as e:
            return self.handle_errors_response(e)
        
