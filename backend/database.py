# backend/database.py
from sqlalchemy import inspect
from sqlalchemy.exc import SQLAlchemyError
from app.models import *    #Importa los modelos, que ya están asociados a `db`
# Función para crear o reiniciar las tablas
def db_initialize(app):
    with app.app_context():
        inspector = inspect(db.engine)

        # Eliminar todas las tablas si existen y crear de nuevo
        try:
            if inspector.get_table_names():
                db.drop_all()
                print("Todas las tablas han sido eliminadas correctamente.")
            
            # Crear todas las tablas de nuevo
            db.create_all()
            print("Todas las tablas han sido creadas correctamente.")

            # Verificar si la tabla Wheel está vacía e inicializarla con datos
            if not db.session.query(Wheel).count():
                for i in range(1, 100):  # Cambia a 1 millón según sea necesario
                    wheel_entry = Wheel(numero=i)
                    db.session.add(wheel_entry)
                db.session.commit()

        except SQLAlchemyError as sae:
            print(f"Error de SQLAlchemy al modificar la base de datos: {str(sae)}")
            db.session.rollback()
        except Exception as e:
            print(f"Error inesperado al modificar la base de datos: {str(e)}")
            db.session.rollback()
