from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask import jsonify
from flask import request
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['MONGO_DBNAME'] = 'farm'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/farm'
app.config['CORS_HEADERS'] = 'Content-Type'

mongo = PyMongo(app)


@app.route('/current/<name>', methods=['GET'])
def get_phase(name):
    current = mongo.db.current
    s = current.find_one({'location': name})
    if s:
        output = {'moisture': s['moisture'], 'temperature': s['temperature'],
                  'humidity': s['humidity'], 'status': s['status'], 'location': s['location']}
    else:
        output = "false"
    return jsonify(output)


@app.route('/')
@cross_origin()
def index():
    return render_template('./index.html')


app.run()
