from flask import Flask,jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from flask_jwt_extended import (
    JWTManager, jwt_required,
    get_jwt_identity
)
import requests
import json
from bson.objectid import ObjectId
from flasgger import Swagger


app = Flask(__name__)
Swagger(app)
#JWT
app.config['JWT_SECRET_KEY'] = 'my top secret key'  # Change this!
app.config['JWT_IDENTITY_CLAIM'] = 'jti'
app.config['JWT_ALGORITHM'] = 'HS256'
jwt = JWTManager(app)


#https://docs.docker.com/compose/gettingstarted/-- za Flask za docker-ja



app.config['MONGO_DBNAME'] = 'knjiznice'
app.config['MONGO_URI'] = 'mongodb+srv://soa2020:soa2020@racuni.igsei.mongodb.net/knjiznice?retryWrites=true&w=majority'


mongo = PyMongo(app)



#get data from uporabnik
@app.route('/getuporabnikeKnjiznice', methods=['GET'])
@jwt_required
def index():

  n = get_jwt_identity()
  headers = {'content-type': 'application/json'}
  url = requests.get("http://172.17.0.27:3001/users/vrni", headers=headers)
 # url.headers['Content-Type']
  g = json.loads(url.content)
  return jsonify(g)




@app.route('/knjiznice', methods=['GET'])
@jwt_required
def users():
    """
    Api za prikaz vseh Knjiznic
    Call this api passing a language name and get back its features
    ---
    tags:
      - METODE
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: Deluje
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """

    knjiznice = get_jwt_identity()
    knjiznice = mongo.db.vse_knjiznice

    

    output = []

    for q in knjiznice.find():
        output.append({'ime': q['ime'],'naslov': q['naslov'],'telefon': q['telefon'], 'eposta':q['eposta']})
    
    return jsonify(output)

@app.route('/knjiznice/<eposta>',methods=['GET'])
@jwt_required
def isci(eposta):
    """
    Isci po e-posti
    Call this api passing a language name and get back its features
    ---
    tags:
      - METODE
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """
    knjiznice = get_jwt_identity()
    knjiznice = mongo.db.vse_knjiznice
    q = knjiznice.find_one({'eposta': eposta})

    
    output ={'ime': q['ime'],'naslov':q['naslov'],'telefon':q['telefon'],'eposta':q['eposta']}
    return jsonify(output)




@app.route('/knjiznice/i/<ime>',methods=['GET'])
@jwt_required
def isciI(ime):
    """
    Isci po e-posti
    Call this api passing a language name and get back its features
    ---
    tags:
      - METODE
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """
    knjiznice = get_jwt_identity()
    knjiznice = mongo.db.vse_knjiznice
    q = knjiznice.find_one({'ime': ime})

    
    output ={'ime': q['ime'],'naslov':q['naslov'],'telefon':q['telefon'],'eposta':q['eposta']}
    return jsonify(output)










'''
@app.errorhandler(500)
def internal_error(error):

    return "500 error"
'''
@app.errorhandler(404)
def not_found(error):
    return "404 error",404




@app.route('/delete/<id>', methods=['DELETE'])
@jwt_required
def delete_user(id):
    """
    Brisi knjiznico
    Call this api passing a language name and get back its features
    ---
    tags:
      - METODE
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """
    knjiznice = get_jwt_identity()
        
    mongo.db.vse_knjiznice.delete_one({'_id': ObjectId(id)})
    resp = jsonify('User deleted successfully!')
    resp.status_code = 200
    return resp

@app.route('/update/<id>', methods=['PUT'])
@jwt_required
def update_user(id):
    """
    Posodobi podatke
    Call this api passing a language name and get back its features
    ---
    tags:
      - METODE
    parameters:
      - name: language
        in: path
        type: string
        required: true
        description: The language name
      - name: size
        in: query
        type: integer
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """
    _json = request.json
    _ime = _json['ime']
    _naslov = _json['naslov']
    _telefon = _json['telefon']
    _eposta = _json['eposta']
    knjiznice = get_jwt_identity()
    mongo.db.vse_knjiznice.update_one({'_id': ObjectId(id)},{'$set': {'ime': _ime, 'naslov': _naslov, 'telefon': _telefon,'eposta':_eposta}})
    resp = jsonify('User updated successfully!')
    resp.status_code = 200
    return resp
'''

@app.route('/')
@jwt_required
def index():
    knjiznice = get_jwt_identity()
    headers = request.headers
    auth = headers.get("Authorization")
    if auth == 'asoidewfoef':
        return jsonify({"message": "OK: Authorized"}), 200
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401
'''


@app.route('/knjiznice',methods=['POST'])
@jwt_required
def add_knjiznice():
    """
    Dodaj
    Call this api passing a language name and get back its features
    ---
    tags:
      - METODE
    parameters:
      - name: ime
        in: path
        type: string
        required: true
      - name: naslov
        in: query
        type: string
        required: true
        description: size of awesomeness
      - name: telefon
        in: query
        type: string
        required: true
        description: size of awesomeness
      - name: eposta
        in: query
        type: string
        required: true
        description: size of awesomeness
    responses:
      500:
        description: Error The language is not awesome!
      200:
        description: A language with its awesomeness
        schema:
          id: awesome
          properties:
            language:
              type: string
              description: The language name
              default: Lua
            features:
              type: array
              description: The awesomeness list
              items:
                type: string
              default: ["perfect", "simple", "lovely"]

    """
    knjiznice = get_jwt_identity()
    knjiznice = mongo.db.vse_knjiznice

    ime = request.json['ime']
    naslov = request.json['naslov']
    telefon = request.json['telefon']
    eposta = request.json['eposta']

    knjiznice_id = knjiznice.insert({'ime':ime,'naslov':naslov, 'telefon': telefon, 'eposta': eposta})
    new_knjiznica = knjiznice.find_one({'_id': knjiznice_id})
    output = {'ime': new_knjiznica['ime'],'naslov': new_knjiznica['naslov'],'telefon': new_knjiznica['telefon'], 'eposta':[eposta]}

    return jsonify(output)


    if __name__=='__main__':
         app.run(host ='0.0.0.0', port = 5000, debug = True) 