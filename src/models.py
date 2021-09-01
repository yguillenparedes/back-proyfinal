from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.username
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Estado (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombreEstado  = db.Column(db.String(100), unique=False, nullable=False)
    municipios = db.relationship('Municipio', backref='estado', lazy=True)
    # usuarios = db.relationship('Usuario', backref='estado', lazy=True)
            
    def __repr__(self):
        return '<Estado %r>' % self.nombreEstado

    def serialize(self):
        return {
            "id": self.id,
            "nombreEstado": self.nombreEstado
       }
        
class Municipio (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombreMunicipio  = db.Column(db.String(100), unique=False, nullable=False)
    idEstado = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)
    usuarios = db.relationship('Usuario', backref='municipio', lazy=True)
   
    def __repr__(self):
        return '<Municipio %r>' % self.nombreMunicipio

    def serialize(self):
        return {
            "id": self.id,
            "nombreMunicipio": self.nombreMunicipio,
            "idEstado": self.idEstado,
        }
        
class Categoria (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombreCategoria  = db.Column(db.String(100), unique=False, nullable=False)
    servicios = db.relationship('Servicio', backref='categoria', lazy=True)   
    def __repr__(self):
        return '<Categoria %r>' % self.nombreCategoria

    def serialize(self):
        return {
            "id": self.id,
            "nombreCategoria": self.nombreCategoria
       }

class Plan (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombrePlan  = db.Column(db.String(100), unique=False, nullable=False)
    usuarios = db.relationship('Usuario', backref='plan', lazy=True)
   
    def __repr__(self):
        return '<Plan %r>' % self.nombrePlan

    def serialize(self):
        return {
            "id": self.id,
            "nombrePlan": self.nombrePlan
        }

class Usuario(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    logUsr = db.Column(db.String(100), unique=True, nullable=False)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    numPhone = db.Column(db.String(100), unique=True, nullable=False)
    nombreUsr = db.Column(db.String(100), unique=False, nullable=False)
    claveUsr = db.Column(db.String(50), unique=False, nullable=False)
    correoUsr = db.Column(db.String(100), unique=True, nullable=False)
    feRegistro = db.Column(db.Date, unique=False, nullable=False)
    txCredenciales = db.Column(db.String(1000), unique=False, nullable=True)
    rankVendedor = db.Column(db.Integer, unique=False, nullable=True, default = 0)
    edad = db.Column(db.Integer, unique=False, nullable=True, default = 18)
    rankComprador = db.Column(db.Integer, unique=False, nullable=True, default = 0)
    foto = db.Column(db.String(100), unique=True, nullable=False)
    idMunicipio  =  db.Column(db.Integer, db.ForeignKey('municipio.id'),nullable=False)
    # idEstado = db.Column(db.Integer, db.ForeignKey('estado.id'), nullable=False)
    idPlan = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    servicios = db.relationship('Servicio', backref='usuario.id', lazy=True)
    preguntas= db.relationship('Pregunta', backref='usuario.id', lazy=True)
    pagos = db.relationship('Pago', backref='usuario.id', lazy=True)
    contratos = db.relationship('Contrato', backref='usuario.id', lazy=True)
    favoritos = db.relationship('Favorito', backref='usuario.id', lazy=True)
    

    def __repr__(self):
        return '<Usuario %r>' % self.nombreUsr 
        

    def serialize(self):
        return {
            "id": self.id,
            "logUsr": self.logUsr,
            "nombreUsr": self.nombreUsr,
            "correoUsr": self.correoUsr,
            "feRegistro": self.feRegistro,
            "txCredenciales": self.txCredenciales,
            "rankVendedor": self.rankVendedor,
            "rankComprador": self.rankComprador,
            "foto": self.foto,
            "idMunicipio": self.idMunicipio,
            "idPlan": self.idPlan,
            "numPhone":self.numPhone,
            "cedula":self.cedula,
            # "idEstado":self.idEstado,
            "edad":self.edad
           }


class Servicio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombreServicio = db.Column(db.String(100), unique=False, nullable=False)
    idsUsrVende = db.Column(db.Integer,db.ForeignKey('usuario.id'), nullable=False)
    fePublicacion = db.Column(db.Date, unique=False, nullable=False)
    descripcion = db.Column(db.String(1000), unique=False, nullable=True)
    idCategoria =  db.Column(db.Integer,db.ForeignKey('categoria.id'), nullable=False)
    statusServicio = db.Column(db.Integer, unique=False, nullable=False)
    inDomicilio = db.Column(db.Boolean, unique=False, nullable=False, default=False)
    palabrasClave = db.Column(db.String(200), unique=False, nullable=True)
    preguntas = db.relationship('Pregunta', backref='servicio', lazy=True)
    contratos = db.relationship('Contrato', backref='servicio', lazy=True)
    favoritoServ = db.relationship('Favorito', backref='servicio', lazy=True)
    txCredenciales = db.Column(db.String(1000), unique=False, nullable=True)
    foto = db.Column(db.String(100), unique=True, nullable=False)
    
    def __repr__(self):
        return '<Servicio %r>' % self.nombreServicio

    def serialize(self):
        return {
            "id": self.id,
            "nombreServicio": self.nombreServicio,
            "idsUsrVende": self.idsUsrVende,
            "fePublicacion": self.fePublicacion,
            "descripcion": self.descripcion,
            "txCredenciales": self.txCredenciales,
            "idCategoria": self.idCategoria,
            "statusServicio": self.statusServicio,
            "foto": self.foto,
            "inDomicilio": self.inDomicilio,
            "palabrasClave": self.palabrasClave
        }

class Pregunta (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idServicio  = db.Column(db.Integer, db.ForeignKey('servicio.id'), nullable=False)
    idUsrPregunta =  db.Column(db.Integer,db.ForeignKey('usuario.id'), nullable=False)
    pregunta = db.Column(db.String(200), unique=False, nullable=True)
    fePregunta= db.Column(db.Date, unique=False, nullable=True)
    respuesta = db.Column(db.String(200), unique=False, nullable=True)
    ferespuesta = db.Column(db.Date, unique=False, nullable=True)
    
    def __repr__(self):
        return '<Pregunta %r>' % self.pregunta

    def serialize(self):
        return {
            "id": self.id,
            "nombreMunicipio": self.idServicio,
            "idUsrPregunta": self.idUsrPregunta,
            "pregunta": self.pregunta,
            "fePregunta": self.fePregunta,
            "respuesta": self.respuesta,
            "feRespuesta": self.ferespuesta
            
        }

class Formapago (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    formaPago  = db.Column(db.String(100), unique=False, nullable=False)
    pagos = db.relationship('Pago', backref='formapago', lazy=True)
   
    def __repr__(self):
        return '<Forma de pago %r>' % self.formaPago

    def serialize(self):
        return {
            "id": self.id,
            "formaPago": self.formaPago
        }
        
class Pago (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer,db.ForeignKey('usuario.id'), nullable=False)
    feFacturacion = db.Column(db.Date, unique=False, nullable=True)
    montoPago = db.Column(db.Float, unique=False, nullable=True)
    idFormaPago = db.Column(db.Integer, db.ForeignKey('formapago.id'), nullable=False)
    fePago = db.Column(db.Date, unique=False, nullable=True)
    statusPago = db.Column(db.Integer, unique=False, nullable=False)
    
    def __repr__(self):
        return '<Fecha facturación %r>' % self.feFacturacion

    def serialize(self):
        return {
            "id": self.id,
            "idUsuario": self.idUsuario,
            "feFacturacion": self.feFacturacion,
            "montoPago": self.montoPago,
            "idFormaPago": self.idFormaPago,
            "nroConfirmacion": self.nroConfirmacion,
            "fePago": self.fePago,
            "statusPago": self.statusPago,
            
        }
        
class Contrato (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idUsrCompra =  db.Column(db.Integer,db.ForeignKey('usuario.id'), nullable=False)
    fePago = db.Column(db.Date, unique=False, nullable=True)
    IdServicio = db.Column(db.Integer,db.ForeignKey('servicio.id'), nullable=False)
    feContrato = db.Column(db.Date, unique=False, nullable=True)
    puntosVendedor =  db.Column(db.Integer, unique=False, nullable=False)
    puntosComprador =  db.Column(db.Integer, unique=False, nullable=False)
    
    def __repr__(self):
        return '<Id Contrato %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "idUsrCompra": self.idUsrCompra,
            "IdServicio": self.IdServicio,
            "feContrato": self.feContrato,
            "puntosVendedor": self.puntosVendedor,
            "puntosComprador": self.puntosComprador
        } 
          
class Favorito (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idServicio =   db.Column(db.Integer, db.ForeignKey('servicio.id'), nullable=False)
    idUsuario  =  db.Column(db.Integer,db.ForeignKey('usuario.id'), nullable=False)
   
    def __repr__(self):
        return '<Servicio %r>' % self.idServicio

    def serialize(self):
        return {
            "id": self.id,
            "idServicio": self.idServicio,
            "idUsuario": self.idUsuario
        }