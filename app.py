from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from api.resources import user, file
from api import routes

app = Flask(__name__)



def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True, methods="POST", allow_headers="*")
    api = Api(app)
    
    # user
    api.add_resource(user.CreateSuperuser, routes.USER_CREATE_SUPERUSER, routes.USER_CREATE_SUPERUSER)
    api.add_resource(user.DeleteAllUsers, routes.USER_DELETE_ALL_USERS, routes.USER_DELETE_ALL_USERS)
    api.add_resource(user.GetUser, routes.USER_GET_USER, routes.USER_GET_USER )
    api.add_resource(user.LoginUser, routes.USER_LOGIN, routes.USER_LOGIN)
    api.add_resource(user.LogoutUser, routes.USER_LOGOUT, routes.USER_LOGOUT)
    api.add_resource(user.CreateAdmin, routes.USER_CREATE_ADMIN, routes.USER_CREATE_ADMIN)
    api.add_resource(user.ListUsers, routes.USER_LIST_USERS, routes.USER_LIST_USERS)
    api.add_resource(user.UpdateUser, routes.USER_UPDATE_USER, routes.USER_UPDATE_USER)
    api.add_resource(user.ResetCurrentUserPassword, routes.USER_RESET_CURRENT_USER_PASSWORD, routes.USER_RESET_CURRENT_USER_PASSWORD)
    api.add_resource(user.DeleteUser, routes.USER_DELETE_USER, routes.USER_DELETE_USER)
    
    # file
    api.add_resource(file.ListFiles, routes.FILE_LIST_FILES, routes.FILE_LIST_FILES)
    api.add_resource(file.DownloadFilesInZip, routes.FILE_DOWNLOAD_ZIP, routes.FILE_DOWNLOAD_ZIP)
    api.add_resource(file.DeleteFiles, routes.FILE_DELETE_FILES, routes.FILE_DELETE_FILES)
    api.add_resource(file.UploadFiles, routes.FILE_UPLOAD_FILES, routes.FILE_UPLOAD_FILES)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
