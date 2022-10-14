import uuid
import io
import zipfile
from PIL import Image
from werkzeug.utils import secure_filename
from firebase_admin import firestore, storage

from api.firebase import Firebase

from api.constants import VIDEO_TYPE, IMAGE_TYPE, FILE_COLLECTION_NAME, THUMBNAIL_SIZE

db = firestore.client()
files_col_ref = db.collection(FILE_COLLECTION_NAME)
bucket = storage.bucket()

class FileModel(Firebase):
    def is_image_or_video_files(self, files):
        return all([file.content_type.startswith(IMAGE_TYPE) or file.content_type.startswith(VIDEO_TYPE) for file in files])
    
    
    def create_destination_path(self, type, name):
        return "/".join([FILE_COLLECTION_NAME, type, name])
    
    def upload_file_to_storage(self, destination_path, file, content_type):
        blob = self.bucket.blob(destination_path)
        blob.upload_from_file(file, content_type=content_type)
        return blob
    
    def create_file_dict(self, create, type, path, size, file_name, file_url, thumb_url, user_id, session_id):
        return {
            "id": uuid.uuid4().hex,
            "create": create,
            "type": type,
            "path": path,
            "size": size,
            "file_name": file_name,
            "file_url": file_url,
            "thumb_url": thumb_url,
            "creator": user_id,
            "session_id": session_id,
        }
        
    def create_thumb_name(self, name):
        arr = name.rsplit(".", 1)
        arr[0] += "_thumb"
        return ".".join(arr)
    
    def create_thumb_of_image(self, file):
        pil_image = Image.open(file)
        pil_image.thumbnail(size=(pil_image.width//THUMBNAIL_SIZE, pil_image.height//THUMBNAIL_SIZE))
        memory_file = io.BytesIO()
        pil_image.save(memory_file, format=pil_image.format)
        print(pil_image.format)
        memory_file.seek(0)
        
        return memory_file
        
    def handle_image(self, file, create, user_id, session_id):
        print(file.filename, file.content_type)
        filename = secure_filename(file.filename)
        destination_path = self.create_destination_path(IMAGE_TYPE, filename)
        print("filename", filename, destination_path)
        blob = self.upload_file_to_storage(destination_path, file, file.content_type)
        
        thumb_filename = self.create_thumb_name(filename)
        thumb_destination_path = self.create_destination_path(IMAGE_TYPE, thumb_filename)
        print("thumb_filename", thumb_filename, thumb_destination_path)
        
        thumb_file = self.create_thumb_of_image(file)
        thumb_blob = self.upload_file_to_storage(thumb_destination_path, thumb_file, file.content_type)
        
        return self.create_file_dict(
                create=create, 
                type=IMAGE_TYPE, 
                path=destination_path, 
                size=blob.size,
                file_name=filename, 
                file_url=blob.public_url, 
                thumb_url=thumb_blob.public_url, 
                user_id=user_id, 
                session_id=session_id
            )
    
    def handle_video(self, file, create, user_id, session_id):
        filename = secure_filename(file.filename)
        destination_path = self.create_destination_path(VIDEO_TYPE, filename)
        blob = self.upload_file_to_storage(destination_path, file, file.content_type)
        
        return self.create_file_dict(
                create=create, 
                type=VIDEO_TYPE, 
                path=destination_path, 
                size=blob.size, 
                file_name=filename, 
                file_url=blob.public_url, 
                thumb_url="", 
                user_id=user_id, 
                session_id=session_id
            )
        
    def create_file_document_to_firestore(self, json_dict):
        print("json_dict", json_dict)
        files_col_ref.document(json_dict["id"]).set(json_dict)
    
    def get_file(self, id):
        doc = files_col_ref.document(id).get()
        if doc.exists:
            return doc.to_dict()
        return None
    
    def get_files(self, begin, end):
        docs = files_col_ref.where("create", ">=", begin).where("create", "<=", end).order_by("create", direction=firestore.Query.DESCENDING).get()
        return [doc.to_dict() for doc in docs]
    
    
        
    def delete_documents_from_firestore(self, paths):
        batch = db.batch()
        docs = files_col_ref.where("path", "in", paths).get()
        for doc in docs:
            batch.delete(doc.reference)
        batch.commit()
        
        
    def delete_files_from_storage(self, paths):
        blobs = []
        for path in paths:
            if IMAGE_TYPE in path:
                thumb_path = self.create_thumb_name(path)
                thumb_blob = bucket.blob(thumb_path)
                blobs.append(thumb_blob)
            blob = bucket.blob(path)
            blobs.append(blob)
        bucket.delete_blobs(blobs)
        
    def delete_files(self, paths):
        self.delete_documents_from_firestore(paths)
        self.delete_files_from_storage(paths)
        
    
    def create_zip(self, paths):
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, "w") as zf:
            for path in paths:
                file_name = path.rsplit("/", 1)[1]
                blob = bucket.blob(path)
                data = blob.download_as_bytes()
                zf.writestr(file_name, data=data, compress_type=zipfile.ZIP_DEFLATED)
        memory_file.seek(0)
        
        return memory_file
    