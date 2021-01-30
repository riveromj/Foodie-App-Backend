"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, send_file
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Recipe, Recipe_Category, Category, Comments
from encrypted import encrypted_pass, compare_pass
from jwt_auth import encode_token, decode_token
import jwt
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from random import randrange
from datetime import datetime
from os.path import join, dirname, realpath
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasuperkey'
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
#host para armar la url de la imagen
HOST = "https://3000-eebc3df8-f426-41f7-8f32-d9211915975b.ws-eu03.gitpod.io/" 

#RECIPE END POINTS >>>>>>>>>>>>>>>>>>

def recipe_route(app, token_required):