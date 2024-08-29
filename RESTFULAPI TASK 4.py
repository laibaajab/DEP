from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Item

class Register_User(Resource):
    def post(self):
        data = request.get_json()
        if User.query.filter_by(username=data['username']).first():
            return {'notification': 'User created'}, 400

        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return {'notification': 'User registered successfully'}, 201

class Login_User(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()

        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200

        return {'notification': 'Invalid credentials'}, 401

class Resource_Item(Resource):
    @jwt_required()
    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        return {'id': item.id, 'name': item.name, 'description': item.description}

    @jwt_required()
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, item_id):
        putdata = request.get_json()
        item = Item.query.get_or_404(item_id)
        item.name = putdata['name']
        item.description = putdata['description']
        db.session.commit()
        return {'id': item.id, 'name': item.name, 'description': item.description}

class ShowItemListResource(Resource):
    @jwt_required()
    def get(self):
        items = Item.checkquery.all()
        return [{'id': item.id, 'name': item.name, 'description': item.description} for item in items]

    @jwt_required()
    def post(self):
        postdata = request.get_json()
        item = Item(name=postdata['name'], description=postdata['description'])
        db.session.add(item)
        db.session.commit()
        return {'id': item.id, 'name': item.name, 'details': item.details}, 201
        


       