from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask('__name__')
api = Api(app)
client = MongoClient('mongodb://db')

db = client.aNewDB

# Collection - Table
UserNum = db['UserNum']

# Document - Record
UserNum.insert({
    'num_of_users':0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update({}, {'$set':{'num_of_users':new_num}})
        return str('Hello user # ' + str(new_num))

def checkInputData(ipData, fnName):
    if fnName == 'add' or fnName == 'subtract' or fnName == 'multiply':
        if 'x' not in ipData or 'y' not in ipData:
            return 301
        return 200
    elif fnName == 'divide':
        if 'x' not in ipData or 'y' not in ipData:
            return 301
        elif ipData['y'] == 0:
            return 302
        else:
            return 200

class Add(Resource):
    def post(self):
        inputData = request.get_json()
        status_code = checkInputData(inputData, 'add')

        if status_code != 200:
            jsonObj = {
                'Message' : 'One or more input parameters are missing',
                'Status Code' : 301
            }
            return jsonify(jsonObj)

        x = int(inputData['x'])
        y = int(inputData['y'])
        res = x + y
        jsonObj = {
            'Message' : res,
            'Status Code' : 200
        }
        return jsonify(jsonObj)

class Subtract(Resource):
    def post(self):
        inputData = request.get_json()
        status_code = checkInputData(inputData, 'subtract')

        if status_code != 200:
            jsonObj = {
                'Message' : 'One or more input parameters are missing',
                'Status Code' : 301
            }
            return jsonify(jsonObj)

        x = int(inputData['x'])
        y = int(inputData['y'])
        res = x - y
        jsonObj = {
            'Message' : res,
            'Status Code' : 200
        }
        return jsonify(jsonObj)

class Multiply(Resource):
    def post(self):
        inputData = request.get_json()
        status_code = checkInputData(inputData, 'multiply')

        if status_code != 200:
            jsonObj = {
                'Message' : 'One or more input parameters are missing',
                'Status Code' : 301
            }
            return jsonify(jsonObj)

        x = int(inputData['x'])
        y = int(inputData['y'])
        res = x * y
        jsonObj = {
            'Message' : res,
            'Status Code' : 200
        }
        return jsonify(jsonObj)

class Divide(Resource):
    def post(self):
        inputData = request.get_json()
        status_code = checkInputData(inputData, 'divide')

        if status_code != 200:
            jsonObj = {
                'Message' : 'One or more input parameters are missing',
                'Status Code' : 301
            }
            return jsonify(jsonObj)

        x = int(inputData['x'])
        y = int(inputData['y'])
        res = x / y
        jsonObj = {
            'Message' : res,
            'Status Code' : 200
        }
        return jsonify(jsonObj)

api.add_resource(Add, '/add')
api.add_resource(Subtract, '/subtract')
api.add_resource(Multiply, '/multiply')
api.add_resource(Divide, '/divide')
api.add_resource(Visit, '/hello')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
