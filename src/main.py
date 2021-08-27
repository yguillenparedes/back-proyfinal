"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import sys
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Categoria
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
    

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/categoria', methods=['GET'])
def obtener_categorias():
    categorias = Categoria.query.all() 
    print(categorias)
    TodasCategorias = [categoria.serialize() for categoria in categorias] 
    return jsonify({"mensaje": "Lista de categorías", "Categorías": TodasCategorias})

@app.route('/categoria/<id>', methods=['GET'])
def obtener_categoria_id(id):
    categoria_encontrada = Categoria.query.get(id)
    if not categoria_encontrada:
        return jsonify({ "mensaje": 'categoría no encontrada', "Categoría": {}})
    return jsonify({ "mensaje": 'Categoría obtenida satisfactoriamente', "Categoría": categoria_encontrada.serialize()})


@app.route('/categoria', methods=['POST'])
def agregar_categorias_post():
    nombreCategoria = request.json["nombreCategoria"]
    nueva_categoria = Categoria(nombreCategoria = nombreCategoria)
    categoria_encontrada = Categoria.query.filter_by(nombreCategoria = nombreCategoria).first()
    if categoria_encontrada:
        return jsonify({ "mensaje": 'La categoría ya existe', "Categoría": nombreCategoria})
    db.session.add(nueva_categoria)
    db.session.commit()
    return jsonify({"mensaje":"Categoría registrada exitosamente", "Categoría": nueva_categoria.serialize()})
    

@app.route('/categoria/<id>', methods=['PUT'])
def actualizar_categorias(id):
    categoria_encontrada = Categoria.query.get(id)
    if not categoria_encontrada:
        return jsonify({ "mensaje": 'Categoría no encontrada', "Categoría": {}})
    categoria_encontrada.nombreCategoria = request.json["nombreCategoria"]
    db.session.commit()
    return jsonify({ "mensaje": 'Categoría actualizada exitosamente', "Categoría": categoria_encontrada.serialize()})


@app.route('/categoria/<id>', methods=['DELETE'])
def borrar_categorias(id):
    categoria_encontrada = Categoria.query.get(id)
    if not categoria_encontrada:
        return jsonify({ "mensaje": 'Categoría no encontrada', "Categoría": {}})
    db.session.delete(categoria_encontrada)
    db.session.commit()
    return jsonify({ "mensaje": 'Categoría eliminada satisfactoriamente', "Categoría": categoria_encontrada.serialize()})

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
