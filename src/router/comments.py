import os
from flask import Flask, request, jsonify, url_for
from models import db, User, Recipe, Comments

def comments_route(app, token_required):
    #TODO: recibir id de receta
    @app.route('/comments', methods=['GET'])
    @token_required
    def get_all_comments():
        all_comments=Comments.query.filter_by(is_active=True)
        comment_list=[]
        for comment in all_comments:
            comment_list.append(comment.serialize())
        return jsonify(comment_list), 200

    @app.route('/comments', methods=['POST'])
    @token_required
    def create_comment():
        body=request.get_json()
        print(body)
        new_comment=Comments(text = body['text'], user_id = user['user']['id'], recipe_id = body['recipe_id'])
        print(new_comment)
        db.session.add(new_comment)
        db.session.commit()
        return jsonify(new_comment.serialize()),201

    @app.route('/comments/<int:id>', methods=['PUT'])
    @token_required
    def delete_comment(id):
        comment=Comments.query.filter_by(id=id).first()
        if comment.is_active == True : 
            comment.is_active = False
            db.session.commit()
            return jsonify('comentario borrado'),200
        return jsonify('No se ha podido borrar el comentario'),406