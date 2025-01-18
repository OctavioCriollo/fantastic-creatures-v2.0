# backend/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

from dotenv import load_dotenv
import os

# Inicializamos las extensiones
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()  # Crea una instancia de Marshmallow

def create_app(config_name='default'):
    # Cargar las variables de entorno
    load_dotenv()

    # Crear la aplicación Flask
    app = Flask(__name__)

    # Cargar la configuración de la aplicación desde config.py
    from config import config
    app.config.from_object(config[config_name])

    # Inicializar CORS para todas las rutas
    CORS(app)

    # Inicializar las extensiones
    db.init_app(app)    # Inicializar SQLAlchemy
    migrate.init_app(app, db)
    ma.init_app(app)  # Inicializa Marshmallow con la aplicación Flask

    # Registrar Blueprints (rutas)
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
