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
from models import db, Categoria, Usuario
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
CORS(app)
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
    return jsonify({"mensaje": "Lista de categorias", "Categorias": TodasCategorias})

@app.route('/categoria/<id>', methods=['GET'])
def obtener_categoria_id(id):
    categoria_encontrada = Categoria.query.get(id)
    if not categoria_encontrada:
        return jsonify({ "mensaje": 'categoria no encontrada', "categoria": {}})
    return jsonify({ "mensaje": 'tarea obtenida satisfactoriamente', "categoria": categoria_encontrada.serialize()})


@app.route('/categoria', methods=['POST'])
def agregar_categorias_post():
    nombreCategoria = request.json["nombreCategoria"]
    nueva_categoria = Categoria(nombreCategoria = nombreCategoria)
    db.session.add(nueva_categoria)
    db.session.commit()
    return jsonify({"mensaje":"Categoría registrada exitosamente", "categoría": nueva_categoria.serialize()})

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all() 
    Todoslosusuarios = [usuarios.serialize() for usuarios in usuarios] 
    return jsonify({"mensaje": "Lista de usuarios", "usuarios": Todoslosusuarios})

@app.route('/usuarios/<id>', methods=['GET'])
def obtener_usuario_id(id):
    usuario_encontrado = Usuario.query.get(id)
    if not usuario_encontrado:
        return jsonify({ "mensaje": 'usuario no encontrada', "usuario": {}})
    return jsonify({ "mensaje": 'usuario obtenido satisfactoriamente', "usuario": usuario_encontrado.serialize()})

@app.route('/usuarios', methods=['POST'])
def agregar_usuarios_post():
    logUsr = request.json["logUsr"]
    nombreUsuario = request.json["nombreUsr"]
    correousuario = request.json["correoUsr"]
    feRegistro = request.json["feRegistro"]
    txCredenciales = request.json["txCredenciales"]
    rankVendedor = int(request.json["rankVendedor"])
    rankComprador = int(request.json["rankComprador"])
    foto = request.json["foto"]
    idMunicipio = int(request.json["idMunicipio"])
    idPlan = int(request.json["idPlan"])
    claveUsr= request.json["claveUsr"]
    nuevo_usuario = Usuario(nombreUsr = nombreUsuario, logUsr=logUsr, correoUsr=correousuario, feRegistro=feRegistro, txCredenciales=txCredenciales, rankVendedor=rankVendedor, rankComprador=rankComprador,foto=foto, idMunicipio=idMunicipio, idPlan = idPlan, claveUsr=claveUsr)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"mensaje":"usuario registrado exitosamente", "usuario": nuevo_usuario.serialize()})

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
