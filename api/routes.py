API_PATH = "/api"

# Warning routes
WARNING_PATH = API_PATH + "/warning"
USER_CREATE_SUPERUSER = WARNING_PATH + "/create_superuser"
USER_DELETE_ALL_USERS = WARNING_PATH + "/delete_all_users"

# User routes
USER_PATH = API_PATH + "/user"
USER_GET_USER = USER_PATH + "/get_user"
USER_LOGIN = USER_PATH + "/login"
USER_LOGOUT = USER_PATH + "/logout"
USER_CREATE_ADMIN = USER_PATH + "/create_admin"
USER_CREATE_CLIENT = USER_PATH + "/create_client"
USER_LIST_USERS = USER_PATH + "/list_users" 
USER_UPDATE_USER = USER_PATH + "/update_user"
USER_RESET_CURRENT_USER_PASSWORD = USER_PATH + "/reset_current_user_password"
USER_DELETE_USER = USER_PATH + "/delete_user"

# File routes
FILE_PATH = API_PATH + "/file"
FILE_LIST_FILES = FILE_PATH + "/list_files"
FILE_DOWNLOAD_ZIP = FILE_PATH + "/download_zip"
FILE_DELETE_FILES = FILE_PATH + "/delete_files"
FILE_UPLOAD_FILE = FILE_PATH + "/upload_file"
FILE_UPLOAD_FILES = FILE_PATH + "/upload_files"
