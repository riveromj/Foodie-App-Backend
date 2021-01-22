"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from admin import setup_admin
from flask import Flask, request, jsonify, url_for,send_file
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from models import db, Recipe
from os.path import join, dirname, realpath
from random import randrange
from utils import APIException, generate_sitemap
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict

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

#Crear nueva receta
@app.route('/recipe',methods=['POST'])
def create_recipe():
    body = dict(request.form)
    #validar los inputs de la receta title ingredients y elaboration
    if request.form.get('title')=='' or request.form.get('title')==None:
        return jsonify("Title cannot be empty"),400
    if request.form.get('ingredients')=='' or request.form.get('ingredients')==None:
        return jsonify("Ingredients cannot be empty"),400
    if request.form.get('elaboration')=='' or request.form.get('elaboration')==None:
        return jsonify("Elaboration cannot be empty"),400
    #validar que exista un archivo
    filename = request.form.get('image')
    if filename != '':
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
            new_recipe=Recipe(body['title'],url,body['ingredients'],body['elaboration'],body['num_comment'])
            db.session.add(new_recipe)
            db.session.commit()
            return jsonify(new_recipe.serialize()),201
        else:
            return jsonify('extencion de archivo no permitido'),00
    else:
        return jsonify('no hay archivo'),400

#Consulta de todas las recetas
@app.route('/recipe',methods=['GET'])
def all_recipes():
    todo_recipes= db.session.query(Recipe).all()
    print(todo_recipes)
    new_list=[]
    for recipe in todo_recipes:
        new_list.append(recipe.serialize())
        print(new_list)
    return jsonify(new_list),200

#Eliminar Receta
@app.route('/recipe/<int:id>',methods=['DELETE'])
def delete_recipe(id):
    recipe= Recipe.query.filter_by(id=id)
    recipe.delete()
    db.session.commit()
    return jsonify('receta eliminada'),200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
