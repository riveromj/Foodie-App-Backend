from flask import Flask, request, jsonify, send_file
from models import db, Recipe, User, Recipe_Category, Category, Comments
from datetime import datetime
from random import randrange
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from os.path import join, dirname, realpath
import os
from jwt_auth import encode_token, decode_token
import jwt
#RECIPE END POINTS >>>>>>>>>>>>>>>>>>


def recipe_route(app, token_required):

    #TODO: dejar el path como recipe y recibir el user por el token
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
            if request.files['image']=='' or not request.files['image']:
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
                new_file.save(os.path.join('./src/img/', file_name))
                url = app.config['HOST'] + file_name
                new_recipe=Recipe(title = body['title'], image = url,ingredients = body['ingredients'], elaboration = body['elaboration'], num_comment = body['num_comment'], user_id = id)
                db.session.add(new_recipe)
                db.session.commit()
                return jsonify(new_recipe.serialize()),200
            else:
                return jsonify('extencion de archivo no permitido'),400
            return jsonify("todo bien"), 200
        except OSError as error:
            return jsonify("error" +str(error)), 400
        except KeyError as error_key:
            return jsonify("error_key" + str(error_key)), 400

    #Consultar las recetar por usuario
    @app.route('/user/recipes',methods=['GET'])
    @token_required
    def user_recipes(user):
        try:
            todo_recipes= db.session.query(Recipe).filter_by(Recipe.is_active==True,user_id=user['user']['id']).all()
            new_list=[]
            for recipe in todo_recipes:
                new_list.append(recipe.serialize())
            return jsonify(new_list),200
        except OSError as error:
            return jsonify("error"),400
        except KeyError as error_key:
            return jsonify("error_key"),400
    #Consulta de todas las recetas para Home 
    @app.route('/recipes/page/<int:page>',methods=['GET'])
    def all_recipes(page):
        try:
            todo_recipes= db.session.query(Recipe).filter(Recipe.is_active==True).order_by(Recipe.date_recipe.desc()).paginate(page, 3, False).items
            new_list=[]
            for recipe in todo_recipes:
                new_list.append(recipe.serialize())  
            return jsonify(new_list),200
        except OSError as error:
            return jsonify("error"),400
        except KeyError as error_key:
            return jsonify("error_key"),400

    #Eliminar Receta con el id de la receta
    @app.route('/delete/recipe/<int:id>',methods=['PUT'])
    @token_required
    def delete_recipe(user,id):
        try:
            recipe=Recipe.query.filter_by(id=id, user_id = user['user']['id']).first()
            query_url= Recipe.query.filter_by(id=id).first() 
            url_photo = query_url.image.rsplit('/')
            if recipe.is_active== True: 
                recipe.is_active = False
                db.session.commit()
                #os.remove('./src/img/'+url_photo[3]) # borrar la foto de la carpeta del servidor
                return jsonify('Receta eliminada'),200
        except OSError as error:
            return jsonify("error" + str(error)), 400