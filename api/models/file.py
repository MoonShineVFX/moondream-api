import os
import uuid
from datetime import datetime, time

from firebase_admin import firestore, storage
from PIL import Image

from ..constants import FILE_COLLECTION_NAME, IMAGE_TYPE, VIDEO_TYPE, THUMBNAIL_SIZE, ALLOWED_IMAGE_EXTENSIONS, ALLOWED_VIDEO_EXTENSIONS

# firestore
db = firestore.client()
file_col = db.collection(FILE_COLLECTION_NAME)

# cloud storage
bucket = storage.bucket()

class MediaFile:
    def __init__(self, file_name, file_url, id, path, size, thumb_url, type, user_id, session_id, create):
        self.file_name = file_name
        self.file_url = file_url
        self.id = id
        self.path = path
        self.size = size
        self.thumb_url = thumb_url
        self.type = type
        self.user_id = user_id
        self.session_id = session_id
        self.create = create
        
    def __str__(self):
        return f"{self.id}, {self.path}"

    def query_by_timestamp(self, begin, end):
        begin = int(begin) or int(datetime.combine(datetime.now(), time.min).timestamp())
        end = end(int) or int(datetime.combine(datetime.now(), time.max).timestamp())
        ref = file_col.where("create", ">=", begin).where("create", "<=", end).order_by("create", direction=firestore.Query.DESCENDING).get()
        docs = [doc.to_dict() for doc in ref]
        return docs
    
    
    

def upload_file_to_storage(resource_path, destination_path):
    blob = bucket.blob(destination_path)
    blob.upload_from_filename(resource_path)
    return blob



def create_thumb_name(name):
    arr = name.rsplit(".", 1)
    arr[0] += "_thumb"
    return ".".join(arr)

def create_thumb_of_image(filename,  destination_prefix) -> str:
    thumb_filename = create_thumb_name(filename)
    pil_image = Image.open(filename)
    pil_image.thumbnail(pil_image.width//THUMBNAIL_SIZE, pil_image.height//THUMBNAIL_SIZE)
    pil_image.save(thumb_filename, format=pil_image.format)
    blob = upload_file_to_storage(
        thumb_filename, destination_prefix + thumb_filename)
    os.remove(thumb_filename)
    return blob.public_url


def handle_file_upload(file, user_id, create, session_id=""):
    file_ext = file.filename.rsplit(".", 1)[1].lower()

    type = None
    if file_ext in ALLOWED_IMAGE_EXTENSIONS:
        type = IMAGE_TYPE
    elif file_ext in ALLOWED_VIDEO_EXTENSIONS:
        type = VIDEO_TYPE
    else:
        raise Exception("File extension is not allowed")
    
    filename = file.filename
    file.save(filename)
    destination_prefix = "/".join([FILE_COLLECTION_NAME, type, ""])
    # handle original image
    blob = upload_file_to_storage(filename, destination_prefix + filename)

    thumb_url = None
    # Handle thumbnail of image
    if type == IMAGE_TYPE:
        thumb_url = create_thumb_of_image(
            filename=filename,
            destination_prefix=destination_prefix
        )
    
    document_obj = {
        "id": uuid.uuid4().hex,
        "create": create,
        "type": type,
        "path": destination_prefix + filename,
        "size": blob.size,
        "file_name": filename,
        "file_url": blob.public_url,
        "thumb_url": thumb_url,
        "creator": user_id,
        "session_id": session_id,
    }
    
    file_col.document(document_obj.id).set(document_obj)
    os.remove(filename)
    return document_obj
