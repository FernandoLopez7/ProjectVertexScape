from firebase_admin import credentials, initialize_app, storage
from django.conf import settings

cred = credentials.Certificate(settings.FIREBASE_JSON_PATH)
STORAGE_BUCKET_NAME = 'vertexscape.appspot.com'
firebase_app = initialize_app(cred, {'storageBucket': STORAGE_BUCKET_NAME})
bucket = storage.bucket(app=firebase_app)
