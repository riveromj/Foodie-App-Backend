from flask import Flask, request, jsonify
from models import db, User
from jwt_auth import encode_token, decode_token
import jwt
from encrypted import encrypted_pass, compare_pass
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import os
from datetime import datetime
from validate_file_format import validate_file_format
#USER END POINTS >>>>>>>>>>>>>>>>>>

def user_route(app, token_required):
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
            email_check= db.session.query(User).filter(User.email==body['email']).first()
            user_check= db.session.query(User).filter(User.user_name==body['user_name']).first()
            if  email_check is None and user_check is None:
                new_pass = encrypted_pass(body['password'])
                new_user = User(user_name = body['user_name'], email = body['email'], password = new_pass)
                db.session.add(new_user)
                db.session.commit()
                token=encode_token(new_user.serialize(), app.config['SECRET_KEY'])
                print(token,"TOKEN")
                return jsonify({"access_token":token}), 201
            else:
                return jsonify("user or email already exists"), 409
        except OSError as error:
            return jsonify("error"), 400

        except KeyError as error:      
            return jsonify("error del KeyError" + str(error)), 400

    @app.route('/user/login', methods=['POST'])
    def login_user():
        try:    
            body = request.get_json()
            print(body)    
            user = User.query.filter_by(email=body['email']).first()   
            if(user is None):
                return "user not exist", 404  
            is_validate = compare_pass(body['password'], user.password_bcrypt())
            if(is_validate == False):
                return "password incorrect", 401
            token=encode_token(user.serialize(), app.config['SECRET_KEY'])
            return jsonify({"access_token":token})

        except OSError as error:
            return jsonify("error"), 400

        except KeyError as error:      
            return jsonify("error del KeyError" + str(error)), 400

    @app.route('/user', methods=['GET'])
    @token_required
    def get_one_member(user):
        try:
            user = db.session.query(User).filter(User.id== user['user']['id']).first()      
            return jsonify(user.serialize()), 200
        except OSError as error:
            return jsonify("error"), 400

        except KeyError as error:      
            return jsonify("error del KeyError" + str(error)), 400   

    @app.route('/user/<int:id>', methods=['DELETE'])
    def delete_user(id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return jsonify('user borrado'), 200 


    #TODO: validar si el usuario esta enviando un file image
    @app.route('/user', methods=['PUT'])
    @token_required
    def update_user(user):
        body = dict(request.form)
        user = db.session.query(User).filter_by(id=user['user']['id']).first()
        existent_user= db.session.query(User).filter_by(user_name=body['user_name']).first()
        if existent_user:
            response_body = {
                "msg": "this user already exists"
            }
            return jsonify(response_body), 400,
        if user.user_name!=body['user_name'] and body['user_name']!="":
            setattr(user, 'user_name', body['user_name'])
        if request.files:
            user_image = request.files['urlImg']
            url_Img = validate_file_format(app, user_image)
            if url_Img is None: 
                return jsonify("Image format invalid"), 400
            user.urlImg = url_Img    
        db.session.commit()
        response_body = {
                "msg": user.serialize()
            }
        return jsonify(response_body), 201


