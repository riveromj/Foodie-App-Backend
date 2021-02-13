import os
from flask import Flask, request, jsonify, url_for
from models import db, User, Recipe, Comments, Favorites

def favorites_route(app, token_required):
    #TODO: recibir id de receta
    #de donde viene user, 
    @app.route('/favorites', methods=['GET'])
    @token_required
    def get_all_favorites(user):
        all_favorites=Favorites.query.filter_by(is_active=True, user_id = user['user']['id']).all()
        favorite_list=[]
        for favorite in all_favorites:
            favorite_list.append(favorite.serialize())
        return jsonify(favorite_list), 200

    @app.route('/favorites/<int:id>' , methods=['POST'])
    @token_required 
    def add_favorites(user, id):
        print(request, "@@@@@@@@@@@@@@@@@@@@@@@@@")
        body=request.get_json()
        print(body, "@@@@@@@@@@@@@@@@@@@@@@@@@")
        favorite_exists = Favorites.query.filter_by(user_id = user['user']['id'], recipe_id = id).first()
        if favorite_exists is not None: 
            if favorite_exists.is_active == False :
                favorite_exists.is_active = True
                db.session.commit()
                return jsonify(favorite_exists.serialize()),200
            return jsonify("favorite already exists"),409
        else:
            new_favorite=Favorites(user_id = user['user']['id'], recipe_id = id, title = body['title'], image = body['image'])
            print(new_favorite, "adios@@@@@@@@@@2@@@@")
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify(new_favorite.serialize()),201

    @app.route('/favorites/<int:id>', methods=['PUT'])
    @token_required
    def delete_favorite(user, id):
        favorite=Favorites.query.filter_by(id = id, user_id = user['user']['id'] ).first()
        print(user,id,favorite, "@@@@@@@@@@@@")
        if favorite is not None:
            if favorite.is_active == True : 
                favorite.is_active = False
                db.session.commit()
                return jsonify('favorito borrado'),200
            else: 
                return jsonify('favorito ya ha sido borrado'),200
        return jsonify('No se ha podido borrar el favorito de la lista'),406