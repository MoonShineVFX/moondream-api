SESSION_ID_NAME = "mdra-session"

class Role:
    SUPERUSER = "superuser"
    ADMIN = "admin"
    CLIENT = "client"

FILE_COLLECTION_NAME = "files"
THUMBNAIL_SIZE = 4
IMAGE_TYPE = "image"
VIDEO_TYPE = "video"

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
ALLOWED_VIDEO_EXTENSIONS = {
    "3g2",
    "3gp",
    "aaf",
    "asf",
    "avchd",
    "avi",
    "drc",
    "flv",
    "m2v",
    "m3u8",
    "m4p",
    "m4v",
    "mkv",
    "mng",
    "mov",
    "mp2",
    "mp4",
    "mpe",
    "mpeg",
    "mpg",
    "mpv",
    "mxf",
    "nsv",
    "ogg",
    "ogv",
    "qt",
    "rm",
    "rmvb",
    "roq",
    "svi",
    "vob",
    "webm",
    "wmv",
    "yuv"
}