import os
from dotenv import dotenv_values

def eliminar_variables_env(ruta_env='.env'):
    # Leer las variables del archivo .env
    variables_env = dotenv_values(ruta_env)
    
    # Eliminar cada variable del entorno
    for variable in variables_env:
        if variable in os.environ:
            del os.environ[variable]
            print(f"Variable eliminada: {variable}")
        else:
            print(f"Variable no encontrada en el entorno: {variable}")

    print("Proceso de eliminación completado.")

# Ejecutar la función
eliminar_variables_env()

# Opcionalmente, puedes verificar que las variables se han eliminado
print("\nVariables de entorno actuales:")
for key, value in os.environ.items():
    print(f"{key}: {value}")