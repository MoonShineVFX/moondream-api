import os
from flask import json

import pyrebase
from firebase_admin import credentials, initialize_app
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_PATH = os.environ.get("FOLDER_PATH", "firebase")

FIREBASE_CONFIG_FILENAME = os.environ.get("FIREBASE_CONFIG_FILENAME", "firebase_config.json")
firebase_config_path = os.path.join(APP_ROOT,  FOLDER_PATH,  FIREBASE_CONFIG_FILENAME)
firebase_config = json.load(open(firebase_config_path))
firebase_client = pyrebase.initialize_app(config=firebase_config)

SERVICE_ACCOUNT_FILENAME = os.environ.get("SERVICE_ACCOUNT_FILENAME", "service_account.json")
cred = credentials.Certificate(os.path.join(FOLDER_PATH,  SERVICE_ACCOUNT_FILENAME))
default_app = initialize_app(cred, {
    "storageBucket": os.environ.get("STORAGE_BUCKET", "moondream-reality.appspot.com")
})

print("firebae_config:", firebase_config["projectId"])
print("service_account:", default_app.project_id)