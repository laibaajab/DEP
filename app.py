from flask import Flask, request
from flask_restful import Api, Resource
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
api = Api(app)

users = {}

class Register_User(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if username in users:
            return {"notification": "User registered"}, 400

        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        return {"notification": "User created successfully"}, 201

class Login_User(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if username not in users or not check_password_hash(users[username], password):
            return {"notification": "Invalid credentials"}, 401
        
        
        return {"access_token": "fake-token-for-{}".format(username)}, 200

class Resource_Item(Resource):
    def get(self, item_id):
        item = {"item_id": item_id, "name": "Test Item"}  
        return item, 200

api.add_resource(Register_User, '/register')
api.add_resource(Login_User, '/login')
api.add_resource(Resource_Item, '/items/<int:item_id>')

if __name__ == '__main__':
    app.run(debug=True)
