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
from models import db, Categoria, Usuario,Contrato,Estado,Formapago,Municipio,Plan,Pregunta,Servicio
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
        return jsonify({ "mensaje": 'usuario no encontrado', "usuario": {}})
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

@app.route('/usuarios/<id>', methods=['PUT'])
def actualizar_usuarios(id):
    usuario_encontrado = Usuario.query.get(id)
    if not usuario_encontrado:
        return jsonify({ "mensaje": 'Usuario no encontrado', "usuario": {}})
    usuario_encontrado.nombreUsr = request.json["nombreUsr"]
    usuario_encontrado.correoUsr = request.json["correoUsr"]
    usuario_encontrado.txCredenciales = request.json["txCredenciales"]
    usuario_encontrado.rankVendedor = request.json["rankVendedor"]
    usuario_encontrado.rankComprador = request.json["rankComprador"]
    usuario_encontrado.foto = request.json["foto"]
    usuario_encontrado.idMunicipio = request.json["idMunicipio"]
    usuario_encontrado.idPlan = request.json["idPlan"]
    db.session.commit()
    return jsonify({ "mensaje": 'Usuario actualizado exitosamente', "Usuario": usuario_encontrado.serialize()})    

@app.route('/usuarios/<id>', methods=['DELETE'])
def borrar_usuarios(id):
    usuario_encontrado = Usuario.query.get(id)
    if not usuario_encontrado:
        return jsonify({ "mensaje": 'Usuario no encontrado', "Usuario": {}})
    db.session.delete(usuario_encontrado)
    db.session.commit()
    return jsonify({ "mensaje": 'Usuario eliminado satisfactoriamente', "Usuario": usuario_encontrado.serialize()})

@app.route('/estados', methods=['GET'])
def obtener_estados():
    estados = Estado.query.all() 
    Todoslosestados = [estados.serialize() for estados in estados] 
    return jsonify({"mensaje": "Lista de estados", "estados": Todoslosestados})

@app.route('/estados/<id>', methods=['GET'])
def obtener_estado_id(id):
    estado_encontrado = Estado.query.get(id)
    if not estado_encontrado:
        return jsonify({ "mensaje": 'estado no encontrada', "estado": {}})
    return jsonify({ "mensaje": 'estado obtenido satisfactoriamente', "estado": estado_encontrado.serialize()})    

@app.route('/formadepago', methods=['GET'])
def obtener_formas_de_pago():
    forma_de_pago = Formapago.query.all() 
    Todaslasformasdepago = [forma_de_pago.serialize() for forma_de_pago in forma_de_pago] 
    return jsonify({"mensaje": "Lista de pagos", "pagos": Todaslasformasdepago})

@app.route('/formadepago/<id>', methods=['GET'])
def obtener_formas_de_pago_id(id):
    forma_de_pago_encontrado = Formapago.query.get(id)
    if not forma_de_pago_encontrado:
        return jsonify({ "mensaje": 'Forma de pago no encontrada', "Forma de pago": {}})
    return jsonify({ "mensaje": 'forma de pago obtenida satisfactoriamente', "Forma de pago": forma_de_pago_encontrado.serialize()})    

@app.route('/municipios', methods=['GET'])
def obtener_municipios():
    municipios = Municipio.query.all() 
    Todoslosmunicipios = [municipios.serialize() for municipios in municipios] 
    return jsonify({"mensaje": "Lista de municipios", "municipios": Todoslosmunicipios})

@app.route('/municipios/<id>', methods=['GET'])
def obtener_municipios_id(id):
    municipio_encontrado = Municipio.query.get(id)
    if not municipio_encontrado:
        return jsonify({ "mensaje": 'municipio no encontrado', "municipio": {}})
    return jsonify({ "mensaje": 'municipio obtenido satisfactoriamente', "municipio": municipio_encontrado.serialize()}) 

@app.route('/plan', methods=['GET'])
def obtener_plan():
    planes = Plan.query.all() 
    Todoslosplanes = [planes.serialize() for planes in planes] 
    return jsonify({"mensaje": "Lista de planes", "planes": Todoslosplanes})

@app.route('/plan/<id>', methods=['GET'])
def obtener_plan_id(id):
    plan_encontrado = Plan.query.get(id)
    if not plan_encontrado:
        return jsonify({ "mensaje": 'plan no encontrado', "plan": {}})
    return jsonify({ "mensaje": 'plan obtenido satisfactoriamente', "plan": plan_encontrado.serialize()})   

@app.route('/servicios', methods=['GET'])
def obtener_servicios():
    servicios = Servicio.query.all() 
    TodoslosServicios = [servicios.serialize() for servicios in servicios] 
    return jsonify({"mensaje": "Lista de servicios", "servicios": TodoslosServicios})

@app.route('/servicios/<id>', methods=['GET'])
def obtener_servicios_id(id):
    servicio_encontrado = Servicio.query.get(id)
    if not servicio_encontrado:
        return jsonify({ "mensaje": 'servicio no encontrado', "servicio": {}})
    return jsonify({ "mensaje": 'servicio obtenido satisfactoriamente', "servicio": servicio_encontrado.serialize()})

@app.route('/servicios', methods=['POST'])
def agregar_servicios_post():
    nombreServicio = request.json["nombreServicio"]
    idsUsrVende = int(request.json["idsUsrVende"])
    fePublicacion = request.json["fePublicacion"]
    descripcion = request.json["descripcion"]
    txCredenciales = request.json["txCredenciales"]
    inDomicilio = request.json["inDomicilio"]
    foto = request.json["foto"]
    idCategoria = int(request.json["idCategoria"])
    statusServicio = int(request.json["statusServicio"])
    palabrasClave= request.json["palabrasClave"]
    nuevo_servicio = Servicio(nombreServicio = nombreServicio, idsUsrVende=idsUsrVende, fePublicacion=fePublicacion, descripcion=descripcion, txCredenciales=txCredenciales, inDomicilio=inDomicilio,foto=foto, idCategoria=idCategoria, statusServicio = statusServicio, palabrasClave=palabrasClave)
    db.session.add(nuevo_servicio)
    db.session.commit()
    return jsonify({"mensaje":"servicio registrado exitosamente", "servicio": nuevo_servicio.serialize()})

@app.route('/servicios/<id>', methods=['PUT'])
def actualizar_servicios(id):
    servicio_encontrado = Servicio.query.get(id)
    if not servicio_encontrado:
        return jsonify({ "mensaje": 'Servicio no encontrado', "Servicio": {}})
    servicio_encontrado.nombreServicio = request.json["nombreServicio"]
    servicio_encontrado.descripcion = request.json["descripcion"]
    servicio_encontrado.txCredenciales = request.json["txCredenciales"]
    servicio_encontrado.inDomicilio = request.json["inDomicilio"]
    servicio_encontrado.foto = request.json["foto"]
    servicio_encontrado.idCategoria = request.json["idCategoria"]
    servicio_encontrado.statusServicio = request.json["statusServicio"]
    db.session.commit()
    return jsonify({ "mensaje": 'Servicio actualizado exitosamente', "Servicio": servicio_encontrado.serialize()})    

@app.route('/servicios/<id>', methods=['DELETE'])
def borrar_servicios(id):
    servicio_encontrado = Servicio.query.get(id)
    if not servicio_encontrado:
        return jsonify({ "mensaje": ' no encontrado', "": {}})
    db.session.delete(servicio_encontrado)
    db.session.commit()
    return jsonify({ "mensaje": ' eliminado satisfactoriamente', "": servicio_encontrado.serialize()})


# @app.route('/pregunta', methods=['GET'])
# def obtener_pregunta():
#     pregunta = Pregunta.query.all() 
#     Todaslospregunta = [pregunta.serialize() for pregunta in pregunta] 
#     return jsonify({"mensaje": "Lista de preguntas", "pregunta": Todaslospregunta})

# @app.route('/pregunta/<id>', methods=['GET'])
# def obtener_pregunta_id(id):
#     pregunta_encontrada = Pregunta.query.get(id)
#     if not pregunta_encontrada:
#         return jsonify({ "mensaje": 'pregunta no encontrada', "pregunta": {}})
#     return jsonify({ "mensaje": 'pregunta obtenida satisfactoriamente', "pregunta": pregunta_encontrada.serialize()})

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


