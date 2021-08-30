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
from models import db, Categoria, Usuario, Pago, Pregunta
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

@app.route('/categoria/<id>', methods=['DELETE'])
def borrar_categorias(id):
    categoria_encontrada = Categoria.query.get(id)
    if not categoria_encontrada:
        return jsonify({ "mensaje": 'Categoría no encontrada', "Categoría": {}})
    db.session.delete(categoria_encontrada)
    db.session.commit()
    return jsonify({ "mensaje": 'Categoría eliminada satisfactoriamente', "Categoría": categoria_encontrada.serialize()})

## Endpoints pagos
@app.route('/pago', methods=['GET'])
def obtener_pagos():
    pagos = Pago.query.all() 
    print(pagos)
    TodosPagos = [pago.serialize() for pago in pagos] 
    return jsonify({"mensaje": "Lista de pagos", "Pagos": TodosPagos})

@app.route('/pago/<id>', methods=['GET'])
def obtener_pago_id(id):
    pago_encontrado = Pago.query.get(id)
    if not pago_encontrado:
        return jsonify({ "mensaje": 'Pago no encontrado', "Pago": {}})
    return jsonify({ "mensaje": 'Pago leido satisfactoriamente', "Pago": pago_encontrado.serialize()})

@app.route('/pago', methods=['POST'])
def agregar_pagos_post():
    idUsuario = request.json["idUsuario"]
    feFacturacion = request.json["feFacturacion"]
    montoPago = request.json["montoPago"]
    idFormaPago = request.json["idFormaPago"]
    nroConfirmacion = request.json["nroConfirmacion"]
    fePago = request.json["fePago"]
    statusPago = request.json["statusPago"]
    nuevo_pago = Pago(idUsuario = idUsuario, feFacturacion = feFacturacion, montoPago = montoPago, idFormaPago = idFormaPago, nroConfirmacion = nroConfirmacion, fePago = fePago, statusPago = statusPago)
    nroConfirmacion_encontrado = Pago.query.filter_by(nroConfirmacion = nroConfirmacion).first()
    if nroConfirmacion_encontrado:
        return jsonify({ "mensaje": 'El número de confirmación asociado al pago ya está registrado', "Pagos": nroConfirmacion})
    db.session.add(nuevo_pago)
    db.session.commit()
    return jsonify({"mensaje":"Pago registrado exitosamente", "Pagos": nuevo_pago.serialize()})

@app.route('/pago/<id>', methods=['PUT'])
def actualizar_pago(id):
    pago_encontrado = Pago.query.get(id)
    if not pago_encontrado:
        return jsonify({ "mensaje": 'Pago no encontrado', "Pago": {}})
    pago_encontrado.idUsuario = request.json["idUsuario"]
    pago_encontrado.feFacturacion = request.json["feFacturacion"]
    pago_encontrado.montoPago = request.json["montoPago"]
    pago_encontrado.idFormaPago = request.json["idFormaPago"]
    pago_encontrado.nroConfirmacion = request.json["nroConfirmacion"]
    pago_encontrado.fePago = request.json["fePago"]
    pago_encontrado.statusPago = request.json["statusPago"]
    db.session.commit()
    return jsonify({ "mensaje": 'Pago actualizado exitosamente', "Pago": pago_encontrado.serialize()})

@app.route('/pago/<id>', methods=['DELETE'])
def borrar_pagos(id):
    pago_encontrado = Pago.query.get(id)
    if not pago_encontrado:
        return jsonify({ "mensaje": 'Pago no encontrado', "Pagos": {}})
    db.session.delete(pago_encontrado)
    db.session.commit()
    return jsonify({ "mensaje": 'Pago eliminado satisfactoriamente', "Pago": pago_encontrado.serialize()})

#Endpoints Preguntas
@app.route('/pregunta', methods=['GET'])
def obtener_preguntas():
    preguntas = Pregunta.query.all() 
    print(preguntas)
    TodasPreguntas = [pregunta.serialize() for pregunta in preguntas] 
    return jsonify({"mensaje": "Lista de preguntas", "Preguntas": TodasPreguntas})

@app.route('/pregunta/<id>', methods=['GET'])
def obtener_pregunta_id(id):
    pregunta_encontrada = Pregunta.query.get(id)
    if not pregunta_encontrada:
        return jsonify({ "mensaje": 'Pregunta no encontrada', "Pregunta": {}})
    return jsonify({ "mensaje": 'Pregunta leida satisfactoriamente', "Pregunta": pregunta_encontrada.serialize()})

@app.route('/pregunta', methods=['POST'])
def agregar_pregunta_post():
    idServicio = request.json["idServicio"]
    idUsrPregunta = request.json["idUsrPregunta"]
    pregunta = request.json["pregunta"]
    fePregunta = request.json["fePregunta"]
    respuesta = request.json["respuesta"]
    feRespuesta = request.json["feRespuesta"]
    nueva_pregunta = Pregunta(idServicio = idServicio, idUsrPregunta = idUsrPregunta, pregunta = pregunta, fePregunta = fePregunta, respuesta = respuesta, feRespuesta = feRespuesta)
    db.session.add(nueva_pregunta)
    db.session.commit()
    return jsonify({"mensaje":"Pregunta registrada exitosamente", "Pregunta": nueva_pregunta.serialize()})

@app.route('/pregunta/<id>', methods=['PUT'])
def actualizar_pregunta(id):
    pregunta_encontrada = Pregunta.query.get(id)
    if not pregunta_encontrada:
        return jsonify({ "mensaje": 'Pregunta no encontrada', "Pregunta": {}})
    pregunta_encontrada.idServicio = request.json["idServicio"]
    pregunta_encontrada.idUsrPregunta = request.json["idUsrPregunta"]
    pregunta_encontrada.pregunta = request.json["pregunta"]
    pregunta_encontrada.fePregunta = request.json["fePregunta"]
    pregunta_encontrada.respuesta = request.json["respuesta"]
    pregunta_encontrada.feRespuesta = request.json["feRespuesta"]
    db.session.commit()
    return jsonify({ "mensaje": 'Pregunta actualizada exitosamente', "Pregunta": pregunta_encontrada.serialize()})

@app.route('/pregunta/<id>', methods=['DELETE'])
def borrar_pregunta(id):
    pregunta_encontrada = Pregunta.query.get(id)
    if not pregunta_encontrada:
        return jsonify({ "mensaje": 'Pregunta no encontrada', "Pregunta": {}})
    db.session.delete(pregunta_encontrada)
    db.session.commit()
    return jsonify({ "mensaje": 'Pregunta eliminada satisfactoriamente', "Pregunta": pregunta_encontrada.serialize()})


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
