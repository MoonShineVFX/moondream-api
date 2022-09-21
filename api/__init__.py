import logging
from flask import Flask
from flask_restful import Api
import firebase

from .resources import user, file


def create_app():
    
    
    app = Flask(__name__)
    api = Api(app)
    
    api.add_resource(user.CreateSuperuser, "/warning/create_superuser", "/warning/create_superuser")
    api.add_resource(user.DeleteAllUsers, "/warning/delete_all_users", "/warning/delete_all_users")
    api.add_resource(user.LoginUser, "/user/login", "/user/login")
    api.add_resource(user.CreateAdmin, "/user/create_admin", "/user/create_admim")
    api.add_resource(user.ListUsers, "/user/list_users", "/user/list_users")
    api.add_resource(user.UpdateUser, "/user/update_user", "/user/update_user") # bug
    api.add_resource(user.ResetPassword, "/user/reset_password", "/user/reset_password")
    api.add_resource(user.DeleteUser, "/user/delete_user", "/user/delete_user")
    
    api.add_resource(file.ListFiles, "/file/list_files", "/file/list_files")
    api.add_resource(file.DownloadFiles, "/file/download_files", "/file/download_files")
    api.add_resource(file.DeleteFiles, '/file/delete_files', '/file/delete_files')
    api.add_resource(file.UploadFiles, '/file/upload_files', '/file/upload_files')

    return app
