import firebase_admin
from firebase_admin import db

cred = firebase_admin.credentials.Certificate('online-chess-6eb6b-firebase-adminsdk-3uoqy-be9bbcb25d.json')
app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://online-chess-6eb6b-default-rtdb.firebaseio.com/'
})
