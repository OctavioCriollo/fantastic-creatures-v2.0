# backend/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

import os

# Inicializamos las extensiones
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()  # Crea una instancia de Marshmallow

def create_app(config_name='default'):
    # Cargar las variables de entorno
    #load_dotenv(override=True)

    # Verifica que FLASK_ENV esté correctamente asignada desde el .env
    print(f"FLASK_ENV: {os.getenv('FLASK_ENV')}") 
    # Seleccionar configuración en base al entorno                  
    config_name = os.getenv('FLASK_ENV')                            
    print(f"Configuración FLASK seleccionada: {config_name}")             
                                                                                               
    # Crear la aplicación Flask
    app = Flask(__name__)

    # Cargar la configuración de la aplicación desde config.py
    from config import config
    app.config.from_object(config[config_name])

    # Imprimir el valor de debug para verificar si está activado
    print(f"Debug Mode: {app.config['DEBUG']}")

    # Inicializar CORS para todas las rutas
    CORS(app)

    # Inicializar las extensiones
    db.init_app(app)    # Inicializar SQLAlchemy
    migrate.init_app(app, db)
    ma.init_app(app)  # Inicializa Marshmallow con la aplicación Flask

    # Inicializar la base de datos después de que SQLAlchemy ha sido inicializado
    from database import db_initialize  # Asegúrate de que la importación sea correcta aquí
    db_initialize(app)

    # Registrar Blueprints (rutas)
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
