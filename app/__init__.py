from flask_pymongo import PyMongo
from flask import Flask

app = Flask(__name__)
mongo = PyMongo(app)
MONGODB_URI = "mongodb://localhost/"
MONGO_DBNAME = "mobilism"
app.secret_key = "super secret key"

from app import routes