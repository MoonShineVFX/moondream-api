import os

SESSION_ID_NAME = os.environ.get("SESSION_ID_NAME", "mdra-session") 

class Role:
    SUPERUSER = "superuser"
    ADMIN = "admin"
    CLIENT = "client"

FILE_COLLECTION_NAME = os.environ.get("FILE_COLLECTION_NAME", "files") 
THUMBNAIL_SIZE = int(os.environ.get("THUMBNAIL_SIZE", 4))
IMAGE_TYPE = "image"
VIDEO_TYPE = "video"
