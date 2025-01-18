# app/config.py
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de la base de datos usando PostgreSQL
DATABASE = os.environ.get('DATABASE')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DEV_DB_HOST = os.environ.get('DEV_DB_HOST')
TEST_DB_HOST = os.environ.get('TEST_DB_HOST')
DB_HOST = os.environ.get('DB_HOST')

# Construir la URI de conexión
DEV_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DEV_DB_HOST}/{DATABASE}'
TEST_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{TEST_DB_HOST}/{DATABASE}'
DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DATABASE}'

# Clase base con la configuración común
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desactivar el rastreo de modificaciones de SQLAlchemy

    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    OPENAI_ORG_ID = os.getenv('OPENAI_ORG_ID')
    OPENAI_PROJECT_ID = os.getenv('OPENAI_PROJECT_ID')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')                       
    # Agregar aquí cualquier configuración común a todos los entornos

# Configuración para el entorno de desarrollo
class DevelopmentConfig(Config):
    DEBUG = True  # Activar el modo de depuración
    SQLALCHEMY_DATABASE_URI = DEV_DATABASE_URL

# Configuración para el entorno de pruebas
class TestingConfig(Config):
    TESTING = True  # Activar el modo de pruebas
    SQLALCHEMY_DATABASE_URI = TEST_DATABASE_URL
    WTF_CSRF_ENABLED = False  # Desactivar CSRF para facilitar las pruebas

# Configuración para el entorno de producción
class ProductionConfig(Config):
    DEBUG = False  # Desactivar el modo de depuración
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    # Agrega cualquier otra configuración relacionada con producción

# Diccionario que mapea nombres de configuraciones a clases
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
