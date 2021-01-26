"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for,send_file
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from os.path import join, dirname, realpath
from random import randrange
from utils import APIException, generate_sitemap
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from admin import setup_admin
from models import db, User,Recipe
from encrypted import encrypted_pass, compare_pass

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
HOST = "https://3000-ed542743-ef07-4d5c-a241-d1227819290b.ws-eu03.gitpod.io/"

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

#para mostrar la imagen de la receta
@app.route('/<filename>', methods=['GET'])
def send_image(filename):
    return send_file('./img/'+filename)

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

##### METHODS RECIPE #######
#Crear nueva receta
@app.route('/user/<int:id>/recipe',methods=['POST'])
def create_recipe(id):
    try:
        #como validar que el usuario esta en db necesito TOKEN
        user_select = db.session.query(User).filter_by(id=id).first()
        if not user_select:
            return jsonify("User not found"),404
        body = dict(request.form)
            #validar los inputs de la receta title ingredients y elaboration
        if request.form.get('title')=='':
            return jsonify("Title cannot be empty"),400
        if request.form.get('ingredients')=='' :
            return jsonify("Ingredients cannot be empty"),400
        if request.form.get('elaboration')=='' :
            return jsonify("Elaboration cannot be empty"),400
        if request.files['image']=='':
            return jsonify("Image cannot be empty"),400
        new_file = request.files['image']
        file_name = secure_filename(new_file.filename)
        #validar la extension de la foto .jpg o .png
        exten = file_name.rsplit('.')
        if (exten[1].lower()=='jpg' or exten[1].lower()=='png'):
            #validacion si el nombre de la imagen ya existe en db
            if os.path.exists('./src/img/' + file_name):
                num = str(randrange(100))+'.'
                file_name = file_name.replace('.', num)
            new_file.save(os.path.join('./src/img', file_name))
            url = HOST + file_name
            new_recipe=Recipe(body['title'],url,body['ingredients'],body['elaboration'],body['num_comment'],id)
            db.session.add(new_recipe)
            db.session.commit()
            return jsonify(new_recipe.serialize()),200
        else:
            return jsonify('extencion de archivo no permitido'),400
        return jsonify("todo bien"), 200
    except OSError as error:
        return jsonify("error"), 400
    except KeyError as error_key:
        return jsonify("error_key" + str(error_key)), 400

#Consultar las recetar por usuario
@app.route('/recipe/<int:id>',methods=['GET'])
def user_recipes(id):
    try:
        todo_recipes= db.session.query(Recipe).filter_by(user_id=id).all()
        new_list=[]
        for recipe in todo_recipes:
            new_list.append(recipe.serialize())
            print(new_list)
        return jsonify(new_list),200
    except OSError as error:
        return jsonify("error"),400
    except KeyError as error_key:
        return jsonify("error_key"),400
#Consulta de todas las recetas para Home 
@app.route('/recipe',methods=['GET'])
def all_recipes():
    try:
        todo_recipes= db.session.query(Recipe).all()
        print(todo_recipes)
        new_list=[]
        for recipe in todo_recipes:
            new_list.append(recipe.serialize())
            print(new_list)
        return jsonify(new_list),200
    except OSError as error:
        return jsonify("error"),400
    except KeyError as error_key:
        return jsonify("error_key"),400

#Eliminar Receta con el id de la receta
@app.route('/recipe/<int:id>',methods=['DELETE'])
def delete_recipe(id):
    try:
        recipe= Recipe.query.filter_by(id=id)
        query_url= Recipe.query.filter_by(id=id).first() 
        url_photo = query_url.image.rsplit('/')
        recipe.delete()
        db.session.commit()
        os.remove('./src/img/'+url_photo[3]) # borrar la foto de la carpeta del servidor
        return jsonify('receta eliminada'),200
    except OSError as error:
        return jsonify("error" + str(error)), 400

#######   METHODS USER ##########
@app.route('/user/register', methods=['POST'])
def register_user():
    try:
        body = request.get_json()    
        if(body['email'] == ''):
            return jsonify({ "msg":"Email is not send"}), 400
        if body['email'] is None:
             return jsonify({ "msg":"Email is not send"}), 400    
        if(body['password'] == '' or body['password'] is None ):
                return jsonify({ "msg":"Password is not send"}), 400
        if(body['user_name'] == '' or body['user_name'] is None ):
                return jsonify({ "msg":"user_name is not send"}), 400  

        new_pass = encrypted_pass(body['password'])
        new_user = User(body['user_name'], body['email'], new_pass)
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
        
        return jsonify(user.serialize())

    except OSError as error:
        return jsonify("error"), 400

    except KeyError as error:      
        return jsonify("error del KeyError" + str(error)), 400


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
