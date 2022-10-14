API_PATH = "/api"

# Session routes
SESSIONS = API_PATH + "/sessions"
SESSION = SESSIONS + "/<session_id>"


# Session records
SESSION_RECORDS = API_PATH + "/session_records/<session_id>"
SESSION_RECORDS_LINK = API_PATH + "/session_records_link"
SESSION_RECORDS_LINK_BY_RANGE = API_PATH + "/session_records_link_by_range"
SESSION_RECORDS_BY_RANGE = API_PATH + "/session_records_by_range"

# Upload file
FILE_VIDEO = API_PATH + "/md_video"
FILE_PHOTO = API_PATH + "/md_photos"

# Download file
DOWNLOAD_VIDEO = FILE_VIDEO + "/<doc_id>"
DOWNLOAD_PHOTO = FILE_PHOTO + "/<doc_id>"

