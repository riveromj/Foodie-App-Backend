import os
from flask import Flask, request, jsonify, url_for
from models import db, User, Recipe, Comments, Favorites

def favorites_route(app, token_required):
    #TODO: recibir id de receta
    @app.route('/favorites', methods=['GET'])
    @token_required
    def get_all_favorites():
        all_favorites=Comments.query.filter_by(is_active=True)
        favorite_list=[]
        for favorite in all_favorites:
            favorite_list.append(favorite.serialize())
        return jsonify(favorite_list), 200

    @app.route('/favorites', methods=['POST'])
    @token_required 
    def add_favorites(user):
        body=request.get_json()
        print(body)
        new_favorite=Favorites(user_id = user['user']['id'], recipe_id = body['recipe_id'])
        print(new_favorite)
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(new_favorite.serialize()),201

    @app.route('/favorites/<int:id>', methods=['PUT'])
    @token_required
    def delete_favorite(user):
        favorite=Favorites.query.filter_by(id = id).first()
        if favorite.is_active == True : 
            favorite.is_active = False
            db.session.commit()
            return jsonify('favorito borrado'),200
        return jsonify('No se ha podido borrar el favorito de la lista'),406