from pymongo import MongoClient
WTF_CSRF_ENABLED = True
SECRET_KEY = 'herpaderp'
DB_NAME = 'hardware'


DATABASE = MongoClient()[DB_NAME]
USERS_COLLECTION = DATABASE.users
MONGO_URI = "mongodb://josh:password@ds137729.mlab.com:37729/hardware"
