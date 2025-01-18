from dotenv import load_dotenv
from flask_cors import CORS
from datetime import datetime
import os
from app import create_app
from database import db_initialize
from app.routes import *

## Cargar el archivo .env solo si no estamos en un contenedor Docker
if not os.getenv('DOCKERIZED', False):
    load_dotenv()

#################################################################
# Seleccionar configuración en base al entorno                  #
config_name = os.getenv('FLASK_ENV') or 'default'               #
                                                                #
# Crear la aplicación Flask                                     #
app = create_app(config_name)                                   #
                                                                #
# Inicializar la base de datos                                  #
db_initialize(app)                                              #
#################################################################

# Ejecutar la aplicación
#========================================#
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
#========================================#

