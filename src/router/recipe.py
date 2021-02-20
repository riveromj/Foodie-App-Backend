from flask import Flask, request, jsonify, send_file
from models import db, Recipe, User, Recipe_Category, Category, Comments
from datetime import datetime
from random import randrange
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from os.path import join, dirname, realpath
import os
from validate_file_format import validate_file_format
import json
from sqlalchemy import and_, or_, not_
#RECIPE END POINTS >>>>>>>>>>>>>>>>>>

def recipe_route(app, token_required):

    #TODO: dejar el path como recipe y recibir el user por el token
    @app.route('/recipe',methods=['POST'])
    @token_required
    def create_recipe(user):
        try:
            id = user['user']['id']
            body = request.form.to_dict()
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
            url_image = validate_file_format(app, new_file)
            
            new_recipe = Recipe(title = body['title'], image = url_image,ingredients = body['ingredients'], elaboration = body['elaboration'], user_id = id)
            db.session.add(new_recipe)
            db.session.commit()
            
    #Buscamos cada categoría en la base de datos y la añadimos a recipe category
            allCategories = json.loads(body["categories"])

            for category in allCategories:
                
                thisCategory = Category.query.filter_by(name_category = category).first()
                print(category, "category")
                if thisCategory:
                    new_recipe_category = Recipe_Category(id_category = thisCategory.id, id_recipe = new_recipe.id)
                    db.session.add(new_recipe_category)
                    db.session.commit()
            
            print(new_recipe)
            return jsonify(new_recipe.serialize()),200

        except OSError as error:
            return jsonify("error" +str(error)), 400
        except KeyError as error_key:
            return jsonify("error_key" + str(error_key)), 400

    #Consultar las recetar por usuario
    @app.route('/user/recipes',methods=['GET'])
    @token_required
    def user_recipes(user):
        try:
            todo_recipes= db.session.query(Recipe).order_by(Recipe.date_recipe.desc()).filter(Recipe.is_active==True, Recipe.user_id==user['user']['id']).all()
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
            todo_recipes= db.session.query(Recipe).filter(Recipe.is_active==True).order_by(Recipe.date_recipe.desc()).paginate(page, 6, False).items
            models = list(map(lambda x: x.serialize(), todo_recipes))
            new_list=[]
            for recipe in models:
                recipe["ingredients"] = recipe["ingredients"][1:-1].replace('"',"").split(",")
                new_list.append(recipe)
            print(new_list,"======")    
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


####PRUEBA GET RECIPE POR ID DE CATEGORÍA   
    @app.route('/category/<int:id_category>', methods = ['GET'])
    def get_recipe_id(id_category):
        print(id_category)
        todo_recipes = db.session.query(Recipe_Category, Recipe).join(Recipe_Category).order_by(Recipe.date_recipe.desc()).filter(Recipe.is_active==True).filter(
            Recipe_Category.id_category == id_category 
        ).paginate(1,6, False).items
        print(todo_recipes)
        list_by_category = []
        for recipe_category in todo_recipes:
            recipe = recipe_category[0].serialize()
            category = recipe_category[1].serialize()
            recipe["category"] = category
            list_by_category.append(recipe)
        return jsonify(list_by_category), 200
   