from flask import Flask, request, jsonify
from models import db

@app.route('/') #Esto es un decorador
def home():
    return jsonify({"mensaje":"Bienvenidos al crud de categorías"})