import uuid
import io
import zipfile
from datetime import datetime
from PIL import Image
from werkzeug.utils import secure_filename
from firebase import Firestore, Storage
from api.common.constants import VIDEO_TYPE, IMAGE_TYPE, FILE_COLLECTION_NAME, THUMBNAIL_SIZE


class FileModel(Firestore, Storage):
    col = FILE_COLLECTION_NAME
    
    def get_now_timestamp(self):
        return int(datetime.now().timestamp())
    def is_image_or_video_files(self, files):
        return all([file.content_type.startswith(IMAGE_TYPE) or file.content_type.startswith(VIDEO_TYPE) for file in files])
    
    def create_destination_path(self, type, name):
        return "/".join([self.col, type, name])
    
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
        
    def handle_image(self, file, filename, content_type, create, user_id, session_id):
        filename = secure_filename(filename)
        destination_path = self.create_destination_path(IMAGE_TYPE, filename)
        blob = self.upload_file_to_storage(destination_path, file, content_type)
        
        thumb_file = self.create_thumb_of_image(file)
        thumb_filename = self.create_thumb_name(filename)
        thumb_destination_path = self.create_destination_path(IMAGE_TYPE, thumb_filename)
        thumb_blob = self.upload_file_to_storage(thumb_destination_path, thumb_file, content_type)
        
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
    
    def handle_video(self, file, filename, content_type, create, user_id, session_id):
        filename = secure_filename(filename)
        destination_path = self.create_destination_path(VIDEO_TYPE, filename)
        blob = self.upload_file_to_storage(destination_path, file, content_type)
        
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
        
    
    def query_file_doc_dict_list(self, begin, end):
        docs = self.get_col_ref().where("create", ">=", begin).where("create", "<=", end).order_by("create", direction=self.DESCENDING).get()
        return [self.convert_doc_to_dict(doc) for doc in docs]
    

    def delete_files(self, paths):
        docs = self.get_col_ref().where("path", "in", paths).get()
        self.delete_docs(docs)  
        self.delete_blobs_by_paths(paths)
        
    
    def create_zip(self, paths):
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, "w") as zf:
            for path in paths:
                file_name = path.rsplit("/", 1)[1]
                blob = self.bucket.blob(path)
                data = blob.download_as_bytes()
                zf.writestr(file_name, data=data, compress_type=zipfile.ZIP_DEFLATED)
        memory_file.seek(0)
        
        return memory_file
    