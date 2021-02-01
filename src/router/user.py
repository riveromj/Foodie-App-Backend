from flask import Flask, request, jsonify
from models import db, User
from jwt_auth import encode_token, decode_token
import jwt
from encrypted import encrypted_pass, compare_pass
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
import os
from datetime import datetime
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
            new_pass = encrypted_pass(body['password'])
            new_user = User(user_name = body['user_name'], email = body['email'], password = new_pass)
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

    @app.route('/user/<int:id>', methods=['PUT'])
    def update_user(id):
        body = dict(request.form)
        user = db.session.query(User).filter_by(id=id).first()
        user.user_name = body['user_name']  
        user_image = request.files['urlImg']
        filename = secure_filename(user_image.filename)
        user_image.save(os.path.join('./src/img', filename))
        now = datetime.now()   
        url_Img = app.config['HOST'] + str(now) + '/' + filename 
        user.urlImg = url_Img    
        db.session.commit()
        response_body = {
                "msg": user.serialize()
            }
        return jsonify(response_body), 201


