from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from api.common import routes
from api.common.custom_api import CustomApi
from api.resources import user, file

from doge_api.common import routes as doge_routes
from doge_api.common.custom_api import DogeCustomApi
from doge_api.resources import doge_file, session

def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True, methods="POST", allow_headers="*")
    api = CustomApi(app)
    
    # user
    api.add_resource(user.CreateSuperuser, routes.USER_CREATE_SUPERUSER, routes.USER_CREATE_SUPERUSER)
    api.add_resource(user.DeleteAllUsers, routes.USER_DELETE_ALL_USERS, routes.USER_DELETE_ALL_USERS)
    api.add_resource(user.GetUser, routes.USER_GET_USER, routes.USER_GET_USER )
    api.add_resource(user.LoginUser, routes.USER_LOGIN, routes.USER_LOGIN)
    api.add_resource(user.LogoutUser, routes.USER_LOGOUT, routes.USER_LOGOUT)
    api.add_resource(user.CreateAdmin, routes.USER_CREATE_ADMIN, routes.USER_CREATE_ADMIN)
    api.add_resource(user.CreateClient, routes.USER_CREATE_CLIENT, routes.USER_CREATE_CLIENT)
    api.add_resource(user.ListUsers, routes.USER_LIST_USERS, routes.USER_LIST_USERS)
    api.add_resource(user.UpdateUser, routes.USER_UPDATE_USER, routes.USER_UPDATE_USER)
    api.add_resource(user.ResetCurrentUserPassword, routes.USER_RESET_CURRENT_USER_PASSWORD, routes.USER_RESET_CURRENT_USER_PASSWORD)
    api.add_resource(user.DeleteUser, routes.USER_DELETE_USER, routes.USER_DELETE_USER)
    
    # file
    api.add_resource(file.ListFiles, routes.FILE_LIST_FILES, routes.FILE_LIST_FILES)
    api.add_resource(file.DownloadFilesInZip, routes.FILE_DOWNLOAD_ZIP, routes.FILE_DOWNLOAD_ZIP)
    api.add_resource(file.DeleteFiles, routes.FILE_DELETE_FILES, routes.FILE_DELETE_FILES)
    api.add_resource(file.UploadFiles, routes.FILE_UPLOAD_FILES, routes.FILE_UPLOAD_FILES)
    api.add_resource(file.UploadFile, routes.FILE_UPLOAD_FILE, routes.FILE_UPLOAD_FILE)
    
    
    
    
    doge_api = DogeCustomApi(app)
    # Doge APIs
    # session
    # http://gitlab.moonshine.tw/1234another.liang/moondreamreality/-/wikis/%E5%A0%B4%E6%AC%A1%E8%A8%AD%E5%AE%9A#%E5%8F%96%E5%BE%97%E5%A0%B4%E6%AC%A1%E5%88%97%E8%A1%A8
    doge_api.add_resource(session.Sessions, doge_routes.SESSIONS, doge_routes.SESSIONS)
    # http://gitlab.moonshine.tw/1234another.liang/moondreamreality/-/wikis/%E5%A0%B4%E6%AC%A1%E8%A8%AD%E5%AE%9A#%E4%BF%AE%E6%94%B9%E5%A0%B4%E6%AC%A1%E8%B3%87%E6%96%99
    doge_api.add_resource(session.Session, doge_routes.SESSION, doge_routes.SESSION)
    # http://gitlab.moonshine.tw/1234another.liang/moondreamreality/-/wikis/%E5%A0%B4%E6%AC%A1%E5%BD%B1%E5%83%8F#%E5%8F%96%E5%BE%97%E7%89%B9%E5%AE%9A%E5%A0%B4%E6%AC%A1%E5%BD%B1%E5%83%8F%E7%B6%B2%E5%9D%80
    doge_api.add_resource(session.SessionRecordsLink, doge_routes.SESSION_RECORDS_LINK, doge_routes.SESSION_RECORDS_LINK)
    # http://gitlab.moonshine.tw/1234another.liang/moondreamreality/-/wikis/%E5%A0%B4%E6%AC%A1%E5%BD%B1%E5%83%8F#%E5%8F%96%E5%BE%97%E6%99%82%E9%96%93%E7%AF%84%E5%9C%8D%E5%85%A7%E7%9A%84%E5%BD%B1%E5%83%8F%E7%B6%B2%E5%9D%80
    doge_api.add_resource(session.SessionRecordsLinkByRange, doge_routes.SESSION_RECORDS_LINK_BY_RANGE, doge_routes.SESSION_RECORDS_LINK_BY_RANGE)
    # http://gitlab.moonshine.tw/1234another.liang/moondreamreality/-/wikis/%E5%A0%B4%E6%AC%A1%E5%BD%B1%E5%83%8F#%E5%8F%96%E5%BE%97%E7%89%B9%E5%AE%9A%E5%A0%B4%E6%AC%A1%E5%BD%B1%E5%83%8F%E5%88%97%E8%A1%A8
    doge_api.add_resource(session.SessionRecords, doge_routes.SESSION_RECORDS, doge_routes.SESSION_RECORDS)
    # http://gitlab.moonshine.tw/1234another.liang/moondreamreality/-/wikis/%E5%A0%B4%E6%AC%A1%E5%BD%B1%E5%83%8F#%E5%8F%96%E5%BE%97%E6%99%82%E9%96%93%E7%AF%84%E5%9C%8D%E5%85%A7%E7%9A%84%E5%BD%B1%E5%83%8F%E5%88%97%E8%A1%A8
    doge_api.add_resource(session.SessionRecordsByRange, doge_routes.SESSION_RECORDS_BY_RANGE, doge_routes.SESSION_RECORDS_BY_RANGE)
    
    # file
    # http://gitlab.moonshine.tw/1234another.liang/moondreamreality/-/wikis/%E5%A4%A2%E5%A2%83%E7%8F%BE%E5%AF%A6%E7%85%A7%E7%89%87/MD-Asset#%E4%B8%8A%E5%82%B3%E5%A0%B4%E5%9F%9F%E6%8B%8D%E6%94%9D%E7%85%A7%E7%89%87
    doge_api.add_resource(doge_file.DogePhoto, doge_routes.FILE_PHOTO, doge_routes.FILE_PHOTO)
    # http://gitlab.moonshine.tw/1234another.liang/moondreamreality/-/wikis/%E5%A4%A2%E5%A2%83%E7%8F%BE%E5%AF%A6%E7%85%A7%E7%89%87/MD-Asset#%E4%B8%8A%E5%82%B3%E5%A0%B4%E5%9F%9F%E6%8B%8D%E6%94%9D%E5%BD%B1%E7%89%87
    doge_api.add_resource(doge_file.DogeVideo, doge_routes.FILE_VIDEO, doge_routes.FILE_VIDEO)
    # http://gitlab.moonshine.tw/1234another.liang/moondreamreality/-/wikis/%E5%A4%A2%E5%A2%83%E7%8F%BE%E5%AF%A6%E7%85%A7%E7%89%87/MD-Asset#%E4%B8%8B%E8%BC%89%E5%A0%B4%E5%9F%9F%E6%8B%8D%E6%94%9D%E7%85%A7%E7%89%87
    doge_api.add_resource(doge_file.DogePhotosDownload, doge_routes.DOWNLOAD_PHOTO, doge_routes.DOWNLOAD_PHOTO)
    # http://gitlab.moonshine.tw/1234another.liang/moondreamreality/-/wikis/%E5%A4%A2%E5%A2%83%E7%8F%BE%E5%AF%A6%E7%85%A7%E7%89%87/MD-Asset#%E4%B8%8B%E8%BC%89%E5%A0%B4%E5%9F%9F%E6%8B%8D%E6%94%9D%E5%BD%B1%E7%89%87
    doge_api.add_resource(doge_file.DogeVideoDownload, doge_routes.DOWNLOAD_VIDEO, doge_routes.DOWNLOAD_VIDEO)
    
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
