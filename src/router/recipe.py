from flask import Flask, request, jsonify, send_file
from models import db, Recipe, User, Recipe_Category, Category, Comments
from datetime import datetime
from random import randrange
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from os.path import join, dirname, realpath
import os
#RECIPE END POINTS >>>>>>>>>>>>>>>>>>

def recipe_route(app, token_required):

    #TODO: dejar el path como recipe y recibir el user por el token
    @app.route('/recipe',methods=['POST'])
    @token_required
    def create_recipe(user):
        try:
            id = user['user']['id']
            
            #como validar que el usuario esta en db necesito TOKEN
            # user_select = db.session.query(User).filter_by(id=id).first()
            # if not user_select:
            #     return jsonify("User not found"),404
            body = request.form.to_dict()
            
                #validar los inputs de la receta title ingredients y elaboration
            if request.form.get('title')=='':
                return jsonify("Title cannot be empty"),400
            if request.form.get('ingredients')=='' :
                return jsonify("Ingredients cannot be empty"),400
            if request.form.get('elaboration')=='' :
                return jsonify("Elaboration cannot be empty"),400
            # if request.files['image']=='':
            #     return jsonify("Image cannot be empty"),400
            # new_file = request.files['image']
            # file_name = secure_filename(new_file.filename)
            # #validar la extension de la foto .jpg o .png
            # exten = file_name.rsplit('.')
            # if (exten[1].lower()=='jpg' or exten[1].lower()=='png'):
            #     #validacion si el nombre de la imagen ya existe en db
            #     if os.path.exists('./src/img/' + file_name):
            #         num = str(randrange(100))+'.'
            #         file_name = file_name.replace('.', num)
            #     new_file.save(os.path.join('./src/img/', file_name))
            #     url = app.config['HOST'] + file_name
        #         new_recipe=Recipe(title = body['title'], image = url,ingredients = body['ingredients'], elaboration = body['elaboration'], num_comment = body['num_comment'], user_id = id)
        #         db.session.add(new_recipe)
        #         db.session.commit()
        #         return jsonify(new_recipe.serialize()),200
        #     else:
        #         return jsonify('extencion de archivo no permitido'),400
        #     return jsonify("todo bien"), 200

            new_recipe=Recipe(title = body['title'], image = body['image'],ingredients = body['ingredients'], elaboration = body['elaboration'], user_id = id)
            db.session.add(new_recipe)
            db.session.commit()
            print(new_recipe.id)
            print(body["categories"])
            #For 
            category = Category.query.filter_by(name_category = body['categories']).first()
            print(category)

            new_recipe_category = Recipe_Category(id_category = category.id, id_recipe = new_recipe.id)
            db.session.add(new_recipe_category)
            db.session.commit()
            print(new_recipe_category)

            return jsonify(new_recipe.serialize()),200
            print(new_recipe)

        except OSError as error:
            return jsonify("error" +str(error)), 400
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