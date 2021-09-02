"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import sys
from flask import Flask, request, jsonify, url_for,redirect,flash,render_template   
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Categoria, Usuario,Contrato,Estado,Formapago,Municipio,Plan,Pregunta,Servicio,Pago
from flask_login import LoginManager,logout_user
from flask_mail import Message

#from models import Person

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
login_manager = LoginManager(app)
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

@login_manager.user_loader
def load_user(user_id):
    for user in Usuario:
        if user.id == int(user_id):
            return user
    return None    

@app.route('/usuarios/<id>', methods=['GET'])
def obtener_usuario_id(id):
    usuario_encontrado = Usuario.query.get(id)
    if not usuario_encontrado:
        return jsonify({ "mensaje": 'usuario no encontrado', "usuario": {}})
    return jsonify({ "mensaje": 'usuario obtenido satisfactoriamente', "usuario": usuario_encontrado.serialize()})

@app.route('/usuarios', methods=['POST'])
def agregar_usuarios_post():
    logUsr = request.json["logUsr"]
    nombreUsr = request.json["nombreUsr"]
    correousuario = request.json["correoUsr"]
    feRegistro = request.json["feRegistro"]
    txCredenciales = request.json["txCredenciales"]
    rankVendedor = int(request.json["rankVendedor"])
    rankComprador = int(request.json["rankComprador"])
    foto = request.json["foto"]
    idMunicipio = int(request.json["idMunicipio"])
    idPlan = int(request.json["idPlan"])
    claveUsr= request.json["claveUsr"]
    numPhone=request.json["numPhone"]
    cedula=request.json["cedula"]
    edad=int(request.json["edad"])
    direccion=request.json["direccion"]
    nuevo_usuario = Usuario(edad=edad,direccion=direccion, nombreUsr = nombreUsr, cedula=cedula,logUsr=logUsr, numPhone=numPhone, correoUsr=correousuario, feRegistro=feRegistro, txCredenciales=txCredenciales, rankVendedor=rankVendedor, rankComprador=rankComprador,foto=foto, idMunicipio=idMunicipio, idPlan = idPlan, claveUsr=claveUsr)
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
    TodosPagos = [pago.serialize() for pago in pagos] 
    return jsonify({"mensaje": "Lista de pagos", "Pagos": TodosPagos})

@app.route('/pago/<id>', methods=['GET'])
def obtener_pago_id(id):
    pago_encontrado = Pago.query.get(id)
    if not pago_encontrado:
        return jsonify({ "mensaje": 'Pago no encontrado', "Pago": {}})
    return jsonify({ "mensaje": 'Pago leido satisfactoriamente', "Pago": pago_encontrado.serialize()})

@app.route('/pagoUsr/<idUsr>', methods=['GET'])
def obtener_pago_usr(idUsr):
    pago_encontrado = Pago.query.filter_by(idUsuario = idUsr).first()
    if not pago_encontrado:
        return jsonify({ "mensaje": 'Pago no encontrado', "Pago": {}})
    pagos = Pago.query.filter_by(idUsuario = idUsr).all()
    TodosPagosUsr = [pago.serialize() for pago in pagos] 
    print(pago_encontrado)
    return jsonify({ "mensaje": 'Pago leido satisfactoriamente', "Pago": TodosPagosUsr})

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
    usuario_encontrado.numPhone = request.json["numPhone"]
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
    return jsonify({"mensaje": "Lista de formas de pago", "pagos": Todaslasformasdepago})

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


@app.route('/servicioUsr/<idUsr>', methods=['GET'])
def obtener_servicio_usr(idUsr):
    servicio_encontrado = Servicio.query.filter_by(idUsrVende = idUsr).first()
    if not servicio_encontrado:
        return jsonify({ "mensaje": 'Servicio no encontrado', "Servicio": {}})
    servicios = Servicio.query.filter_by(idUsrVende = idUsr).all()
    TodosServiciosUsr = [servicio.serialize() for servicio in servicios] 
    print(servicio_encontrado)
    return jsonify({ "mensaje": 'Servicios leidos satisfactoriamente', "Servicios": TodosServiciosUsr})


@app.route('/servicioCat/<idCat>', methods=['GET'])
def obtener_servicio_cat(idCat):
    servicio_encontrado = Servicio.query.filter_by(idCategoria = idCat).first()
    if not servicio_encontrado:
        return jsonify({ "mensaje": 'Servicio no encontrado', "Servicio": {}})
    servicios = Servicio.query.filter_by(idCategoria = idCat).all()
    TodosServiciosCat = [servicio.serialize() for servicio in servicios] 
    print(servicio_encontrado)
    return jsonify({ "mensaje": 'Servicios leidos satisfactoriamente', "Servicios": TodosServiciosCat})

@app.route('/servicios', methods=['POST'])
def agregar_servicios_post():
    nombreServicio = request.json["nombreServicio"]
    idUsrVende = int(request.json["idUsrVende"])
    fePublicacion = request.json["fePublicacion"]
    descripcion = request.json["descripcion"]
    txCredenciales = request.json["txCredenciales"]
    inDomicilio = request.json["inDomicilio"]
    foto = request.json["foto"]
    idCategoria = int(request.json["idCategoria"])
    statusServicio = int(request.json["statusServicio"])
    palabrasClave= request.json["palabrasClave"]
    nuevo_servicio = Servicio(nombreServicio = nombreServicio, idUsrVende=idUsrVende, fePublicacion=fePublicacion, descripcion=descripcion, txCredenciales=txCredenciales, inDomicilio=inDomicilio,foto=foto, idCategoria=idCategoria, statusServicio = statusServicio, palabrasClave=palabrasClave)
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
    servicio_encontrado.palabrasClave = request.json["palabrasClave"]
    db.session.commit()
    return jsonify({ "mensaje": 'Servicio actualizado exitosamente', "Servicio": servicio_encontrado.serialize()})    

@app.route('/serviciosUsrAct', methods=['PUT'])
def actualizar_servicios_por_usuario():
    idServicio = request.json["idServicio"]
    idUsrVende = request.json["idUsrVende"]
    servicio_encontrado = Servicio.query.filter_by(id= idServicio, idUsrVende = idUsrVende).all()
    if not servicio_encontrado:
        return jsonify({ "mensaje": 'Servicio no encontrado', "Servicio": {}})
    servicio_encontrado = Servicio.query.get(idServicio)
    servicio_encontrado.nombreServicio = request.json["nombreServicio"]
    servicio_encontrado.descripcion = request.json["descripcion"]
    servicio_encontrado.txCredenciales = request.json["txCredenciales"]
    servicio_encontrado.inDomicilio = request.json["inDomicilio"]
    servicio_encontrado.foto = request.json["foto"]
    servicio_encontrado.idCategoria = int(request.json["idCategoria"])
    servicio_encontrado.palabrasClave = request.json["palabrasClave"]
    db.session.commit()
    return jsonify({ "mensaje": 'Servicio actualizado exitosamente', "Servicio": servicio_encontrado.serialize()}) 

@app.route('/serviciosDelUsr', methods=['DELETE'])
def borrar_servicios_usuario():
    idServicio = request.json["idServicio"]
    idUsrVende = request.json["idUsrVende"]
    servicio_encontrado = Servicio.query.filter_by(id = idServicio, idUsrVende = idUsrVende).all()
    if not servicio_encontrado:
        return jsonify({ "mensaje": 'Servicio no encontrado o no es posible ser eliminado', "Servicio": {}})
    servicio_encontrado = Servicio.query.get(idServicio)
    db.session.delete(servicio_encontrado)
    db.session.commit()
    return jsonify({ "mensaje": 'El servicio fue eliminado satisfactoriamente', "": servicio_encontrado.serialize()})




@app.route('/servicios/<id>', methods=['DELETE'])
def borrar_servicios(id):
    servicio_encontrado = Servicio.query.get(id)
    if not servicio_encontrado:
        return jsonify({ "mensaje": ' no encontrado', "": {}})
    db.session.delete(servicio_encontrado)
    db.session.commit()
    return jsonify({ "mensaje": ' eliminado satisfactoriamente', "": servicio_encontrado.serialize()})

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/'))


# @app.route("/usuarios/<string:logUsr>")
# def user_posts(logUsr):
#     page = request.args.get('page', 1, type=int)
#     user = Usuario.query.filter_by(logUsr=logUsr).first_or_404()
#     posts = Servicio.query.filter_by(author=user)\
#         .order_by(Servicio.date_posted.desc())\
#         .paginate(page=page, per_page=5)
#     return render_template('user_posts.html', posts=posts, user=user)

# def send_reset_email(user):
#     token = user.get_reset_token()
#     msg = Message('Password Reset Request',
#                   sender='noreply@demo.com',
#                   recipients=[user.email])
#     msg.body = f'''To reset your password, visit the following link:
# {url_for('reset_token', token=token, _external=True)}'''
    

# @app.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = Usuario.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('login'))
#     return render_template('reset_request.html', title='Reset Password', form=form)

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


