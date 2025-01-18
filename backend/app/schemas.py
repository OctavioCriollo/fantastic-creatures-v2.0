# app/schemas.py
from flask_marshmallow import Marshmallow
from app import ma  # Importar el objeto ma inicializado en __init__.py
from .models import Creature

ma = Marshmallow()

# Definir el schema para Creature
class CreatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Creature
