"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from encrypted import encrypted_pass, compare_pass
from jwt_auth import encode_token, decode_token
import jwt
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from random import randrange
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'thisisasuperkey'
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

#host para armar la url de la imagen de perfil del usuario
HOST = "https://3000-eebc3df8-f426-41f7-8f32-d9211915975b.ws-eu03.gitpod.io/" 

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

        except OSError as err:
            print(err)
            return jsonify("no authorization"), 401

        except jwt.exceptions.ExpiredSignatureError as err:
            print(err)
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

@app.route('/user/register', methods=['POST'])
def register_user():
    try:
        body = request.get_json()    
        if(body['email'] == '' or body['email']== None):
            return jsonify({ "msg":"Email is not send"}), 400       
        if(body['password'] == '' or body['password'] is None ):
                return jsonify({ "msg":"Password is not send"}), 400
        if(body['user_name'] == '' or body['user_name'] is None ):
                return jsonify({ "msg":"user_name is not send"}), 400 
        new_file = request.files['image']
        file_name = secure_filename(new_file.filename)
        #validar la extension de la foto .jpg o .png
        exten = file_name.rsplit('.')
        if (exten[1].lower()=='jpg' or exten[1].lower()=='png'):
            #validacion si el nombre de la imagen ya existe en db
            if os.path.exists('./src/img/' + file_name):
                num = str(randrange(100))+'.'
                file_name = file_name.replace('.', num)
            new_file.save(os.path.join('./src/img/', file_name))
            urlImg = HOST + file_name                   
        new_pass = encrypted_pass(body['password'])
        new_user = User(body['user_name'], body['email'], new_pass, urlImg)
        db.session.add(new_user)
        db.session.commit()
        response_body = {
            "msg": new_user.serialize()
         }
        return jsonify(response_body), 201

    except OSError as error:
        return jsonify("error"), 400

    except KeyError as error:      
        return jsonify("error del KeyError" + str(error)), 400

@app.route('/user/login', methods=['POST'])
def login_user():
    try:    
        body = request.get_json()    
        user = User.query.filter_by(email=body['email']).first()   
        if(user is None):
            return "user not exist", 401  
        is_validate = compare_pass(body['password'], user.password_bcrypt())
        if(is_validate == False):
            return "password incorrect", 401
        token=encode_token(user.serialize(), app.config['SECRET_KEY'])
        return jsonify({"access_token":token})

    except OSError as error:
        return jsonify("error"), 400

    except KeyError as error:      
        return jsonify("error del KeyError" + str(error)), 400

@app.route('/user/<int:id>', methods=['GET'])
def get_one_member(id):
    try:
        user = db.session.query(User).filter_by(id=id).first()
        print(user.user_name)
        print(user.id, "****************")  
       # if user:
        return jsonify(user.serialize()), 200
    except OSError as error:
        return jsonify("error"), 400

    except KeyError as error:      
        return jsonify("error del KeyError" + str(error)), 400   

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    print(id)
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    print(user)
    return jsonify('user borrado'), 200 

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    body = request.get_json()  
    user = db.session.query(User).filter_by(id=id).first()
    user.user_name = body['user_name']
    db.session.commit()
    print(user, body)
    response_body = {
            "msg": user.serialize()
        }
    return jsonify(response_body), 201




    
    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
