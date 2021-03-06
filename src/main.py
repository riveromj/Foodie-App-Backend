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
from models import db, User, Recipe, Recipe_Category, Category, Comments, Favorites
from router.user import user_route
from router.recipe import recipe_route
from router.comments import comments_route
from router.favorites import favorites_route
import cloudinary
from functools import wraps
from jwt_auth import encode_token, decode_token
import jwt
#-----------
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasuperkey'
app.config['HOST'] = "https://3000-eebc3df8-f426-41f7-8f32-d9211915975b.ws-eu03.gitpod.io/" 
MIGRATE = Migrate(app, db)
db.init_app(app)

CORS(app)
setup_admin(app)

cloudinary.config(
    cloud_name = os.environ.get('CLOUD_NAME'),
    api_key = os.environ.get('CLOUD_API_KEY'),
    api_secret = os.environ.get('CLOUD_SECRET')
)

#TODO: mover return de 51 a 42 y pasar data en los parametros

#decorador
def token_required(f):
    @wraps(f)
    def decorador(*args , **kwargs ):
        try:
            auth = request.headers.get('Authorization')
            if auth is None:
                return jsonify("no token"), 403
            token = auth.split(' ')
            data = decode_token(token[1], app.config['SECRET_KEY'] )
            user = User.query.get(data['user']['id'])
            if user is None:
                return jsonify("no authorization"), 401
            return f(data,*args , **kwargs)
        except OSError as err:
            
            return jsonify("no authorization"), 401

        except jwt.exceptions.ExpiredSignatureError as err:
            
            return jsonify("expired token"), 403

        return f(*args , **kwargs)
    return decorador

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/<filename>', methods=['GET'])
def send_image(filename):
    return send_file('./img/'+filename)    

#ROUTES ------------
user = user_route(app, token_required)
recipe = recipe_route(app, token_required)
comments = comments_route(app, token_required)
favorites = favorites_route(app, token_required)


#--------

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
