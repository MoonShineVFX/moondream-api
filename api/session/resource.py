import os
import io
import uuid
import zlib
import zipfile
from datetime import datetime, time
from flask import Blueprint, request, jsonify, send_file, json
from firebase_admin import firestore, storage
from api import firebase_client
from PIL import Image
from .schema import SessionBaseSchema, SessionIdRequiredSchema, SessionDownloadSchema
from ..decoration import login_required, admin_required
from ..utils import handle_errors_response, successful_format, parse_request_form


SESSION_COLLECTION = os.getenv('SESSION_COLLECTION')
IMAGE_TYPE = os.getenv('IMAGE_TYPE')
VIDEO_TYPE = os.getenv('VIDEO_TYPE')

client_auth = firebase_client.auth()
db = firestore.client()
session_col = db.collection(SESSION_COLLECTION)
bucket = storage.bucket()
session_api = Blueprint('session_api', __name__, url_prefix='/session')


ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
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


def upload_blob_to_bucket(resource_path, destination_path) -> (str, int):
    blob = bucket.blob(destination_path)
    blob.upload_from_filename(resource_path)
    print(str(blob._get_download_url))

    return blob.public_url, blob.size


def size_of_thumbnail(data):
    scale = 4
    return data.width//scale, data.height//scale


def create_thumb_name(name):
    arr = name.rsplit('.', 1)
    arr[0] += '_thumb'
    return '.'.join(arr)


def create_thumb_of_image(filename,  destination_prefix) -> str:
    thumb_filename = create_thumb_name(filename)
    pil_image = Image.open(filename)
    pil_image.thumbnail(size_of_thumbnail(pil_image))
    pil_image.save(thumb_filename, format=pil_image.format)
    thumbnail_url, _ = upload_blob_to_bucket(
        thumb_filename, destination_prefix + thumb_filename)
    os.remove(thumb_filename)
    return thumbnail_url


def get_destination_path(path):
    return '/'.join([SESSION_COLLECTION, path, ''])


def handle_file(filename, type, user_id):
    destination_prefix = get_destination_path(type)
    original_url, original_size = upload_blob_to_bucket(
        filename, destination_prefix + filename)

    thumb_url = None
    # Handle thumbnail of image
    if type == IMAGE_TYPE:
        thumb_url = create_thumb_of_image(
            filename=filename,
            destination_prefix=destination_prefix
        )

    id = uuid.uuid4().hex
    return {
        "id": id,
        "type": type,
        "path": destination_prefix + filename,
        "size": original_size,
        "file_name": filename,
        "file_url": original_url,
        "thumb_url": thumb_url,
        "creator": user_id
    }


def handle_files(files, user_id) -> list:
    datas = []
    for file in files:
        file_ext = file.filename.rsplit('.', 1)[1].lower()
        is_image = file_ext in ALLOWED_IMAGE_EXTENSIONS
        is_video = file_ext in ALLOWED_VIDEO_EXTENSIONS

        if is_image or is_video:
            filename = file.filename
            file.save(filename)
            type = IMAGE_TYPE if is_image else VIDEO_TYPE
            datas.append(handle_file(filename, type, user_id))
            os.remove(filename)
        else:
            raise Exception("File extension is not allowed")
    return datas


@session_api.route('/create', methods=["POST"])
@admin_required
def create(user_id, email):
    try:
        form, files = parse_request_form(SessionBaseSchema(), request)
        timestamp = int(datetime.now().timestamp())
        id = form.get('id') or str(timestamp)
        datas = handle_files(files, user_id)
        document_obj = {
            "id": id,
            "create": timestamp,
            "datas": datas,
            "data_numbers": len(datas),
        }
        session_col.document(id).set(document_obj, merge=True)
        return jsonify(successful_format(data=document_obj)), 200
    except Exception as e:
        return handle_errors_response(e)


@session_api.route('/add', methods=['POST'])
@admin_required
def add():
    try:
        form, files = parse_request_form(SessionIdRequiredSchema(), request)
        id = form['id']
        session_doc = session_col.document(id)
        doc = session_doc.get()
        if not doc.exists:
            raise Exception(f"Not Found with id: {id}")

        datas = handle_files(files)
        session_doc.update({
            'datas': firestore.ArrayUnion(datas),
            "data_numbers": firestore.Increment(len(datas))
        })

        return jsonify(successful_format(data={
            "id": id,
            "datas": datas
        })), 200

    except Exception as e:
        return handle_errors_response(e)


def parse_files_of_session(doc):
    arr = []
    for data in doc.get('datas', []):
        data['create'] = doc['create']
        data['creator'] = 'test'
        arr.append(data)
    return arr


@session_api.route('/files_of_interval', methods=['POST'])
@admin_required
def session_files(user_id, email):
    try:
        form = request.form.to_dict()
        begin = form.get('startTime') or int(
            datetime.combine(datetime.now(), time.min).timestamp())
        end = form.get('endTime') or int(
            datetime.combine(datetime.now(), time.max).timestamp())
        ref = session_col.where('create', '>=', begin).where(
            'create', '<=', end).get()
        docs = []
        for doc in ref:
            tmp = parse_files_of_session(doc.to_dict())
            print(tmp)
            docs.extend(tmp)

        return jsonify(successful_format(data=docs)), 200

    except Exception as e:
        return handle_errors_response(e)


def delete_files_of_storage(datas):
    blobs = [data.path+'/'+data.file_name for data in datas]
    bucket.delete_blobs(blobs)


def delete_session_files_of_firestore(id, datas):
    session_col.document(id).update({
        "datas": firestore.ArrayRemove(datas),
        "data_numbers": firestore.Increment(-len(datas))
    })


def delete_sessions_files_of_firestore(datas):
    obj = {}
    for data in datas:
        create = data['create']
        del data['create']
        del data['creator']
        if create not in obj:
            obj[create] = [data]
        else:
            obj[create].append(data)

    for key, values in obj.items():
        delete_session_files_of_firestore(key, values)


@session_api.route('/delete', methods=['POST'])
@admin_required
def delete_session_files():
    try:
        form = request.form.to_dict()
        datas = form.get('datas') or []
        delete_files_of_storage(datas)
        delete_sessions_files_of_firestore(datas)
        return jsonify(successful_format(data=datas)), 200

    except Exception as e:
        return handle_errors_response(e)


@session_api.route('/download', methods=['GET', 'POST'])
def session_list():
    try:
        datas = DATAS
        memory_file = io.BytesIO()
        compression = zipfile.ZIP_DEFLATED
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for data in datas:
                path = data['path'] + data['file_name']
                blob = bucket.blob(path)
                file = blob.download_as_bytes()
                zf.writestr(data['file_name'], data=file,
                            compress_type=compression)
        memory_file.seek(0)
        return send_file(memory_file, download_name='capsule.zip', as_attachment=True)
    except Exception as e:
        return handle_errors_response(e)


DATAS = [
    {
        "create": 1663561309,
        "creator": "test",
        "file_name": "file_2.mp4",
        "file_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/video/file_2.mp4",
        "id": "93b4764783d04468b449b0ac477446c8",
        "path": "session/video/file_2.mp4",
        "size": 1572966,
        "thumb_url": None,
        "type": "video"
    },
    {
        "create": 1663561309,
        "creator": "test",
        "file_name": "file_8T1riaM.jpg",
        "file_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/image/file_8T1riaM.jpg",
        "id": "7e01fcc4fe94469680355a03f295a958",
        "path": "session/image/",
        "size": 367167,
        "thumb_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/image/file_8T1riaM_thumb.jpg",
        "type": "image"
    },
    {
        "create": 1663561389,
        "creator": "test",
        "file_name": "file_2.mp4",
        "file_url": "https://storage.googleapis.com/moondream-reality.appspot.com/session/video/file_2.mp4",
        "id": "cdef79cec24f4735adcff8ab5b8ed06e",
        "path": "session/video/",
        "size": 1572966,
        "thumb_url": None,
        "type": "video"
    }
]
