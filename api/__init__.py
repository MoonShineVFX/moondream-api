import os
from flask import Flask, json
from firebase_admin import credentials, initialize_app
import pyrebase

APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_MODE = os.getenv('ENV_MODE')
firebase_config_path = os.path.join(APP_ROOT,  "firebase", str(ENV_MODE) + "_firebase_config.json")
print(firebase_config_path)
firebae_config = json.load(open(firebase_config_path))
firebase_client = pyrebase.initialize_app(config=firebae_config)


cred = credentials.Certificate('firebase/' + ENV_MODE +'_service_account.json')
default_app = initialize_app(cred, {
    'storageBucket': os.environ.get('BUCKET_NAME', 'moondream-reality.appspot.com')
})


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
    
    from .user.resource import user_api
    from .session.resource import session_api
    app.register_blueprint(user_api)
    app.register_blueprint(session_api)

    return app
