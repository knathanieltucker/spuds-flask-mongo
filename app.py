import os
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_dotenv import DotEnv

app = Flask(__name__)
# We try to read in env vars if they exist
env = DotEnv()
env.init_app(app, verbose_mode=False)

MONGO_URI = os.environ.get("MONGO_URI")

mongo = PyMongo(app, uri=MONGO_URI, retryWrites=False)

@app.route('/test', methods=['GET'])
def get_all_frameworks():
    test = mongo.db.test

    output = []

    for q in test.find():
        output.append({'stuff' : q['stuff']})

    return jsonify({'result' : output})

@app.route('/test', methods=['POST'])
def add_framework():
    test = mongo.db.test

    stuff = request.json['stuff']
    print({'stuff' : stuff})

    test_id = test.insert_one({'stuff' : stuff})
    print(test_id)
    new_test = test.find_one({'_id' : test_id.inserted_id})

    output = {'stuff' : new_test['stuff']}

    return jsonify({'result' : output})


if __name__ == '__main__':
    app.run(debug=True)
