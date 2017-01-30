from pymongo import MongoClient
WTF_CSRF_ENABLED = True
SECRET_KEY = 'herpaderp'
DB_NAME = 'hardware'


DATABASE = MongoClient()[DB_NAME]
USERS_COLLECTION = DATABASE.users
