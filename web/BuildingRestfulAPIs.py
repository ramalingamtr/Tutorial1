from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask('__name__')
api = Api(app)

client = MongoClient('mongodb://db')
db = client.SentencesDatabase

# Collection = Table
users = db['users']

class Register(Resource):
    def post(self):
        inputData = request.get_json()
        username = inputData['username']
        password = inputData['password']

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            'username' : username,
            'password' : hashed_pw,
            'sentences' : '',
            'tokens' : 6
        })

        retJson = {
            'status' : 200,
            'msg' : 'Registration successful'
        }
        return jsonify(retJson)

def verifyPw(username, password):
    storedPw = users.find({'username':username})[0]['password']
    return (bcrypt.hashpw(password.encode('utf8'), storedPw) == storedPw)

def countTokens(username):
    tokens = users.find({'username':username})[0]['tokens']
    return int(tokens)

class Store(Resource):
    def post(self):
        inputData = request.get_json()
        username = inputData['username']
        password = inputData['password']
        sentence = inputData['sentence']

        correct_pw = verifyPw(username, password)
        if not correct_pw:
            retJson = {
                'status' : 302
            }
            return jsonify(retJson)

        numTokens = countTokens(username)
        if numTokens <= 0:
            retJson = {
                'status' : 301
            }
            return jsonify(retJson)

        users.update({
            'username' : username
        },
        {
            '$set' : {
                'sentence' : sentence,
                'tokens' : numTokens - 1
            }
        }
        )

        retJson = {
            'status' : 200,
            'msg' : 'Sentence saved successfully'
        }
        return jsonify(retJson)

class Get(Resource):
    def post(self):
        inputData = request.get_json()
        username = inputData['username']
        password = inputData['password']

        correct_pw = verifyPw(username, password)
        if not correct_pw:
            retJson = {
                'status' : 302
            }
            return jsonify(retJson)

        numTokens = countTokens(username)
        if numTokens <= 0:
            retJson = {
                'status' : 301
            }
            return jsonify(retJson)

        users.update({
            'username' : username
        },
        {
            '$set' : {
                'tokens' : numTokens - 1
            }
        })

        sentence = users.find({'username':username})[0]['sentence']
        retJson = {
            'status' : 200,
            'msg' : sentence
        }
        return jsonify(retJson)

api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
