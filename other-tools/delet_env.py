import os
from dotenv import dotenv_values

print("Variables antes de eliminar:")
for key, value in os.environ.items():
    print(f"{key}: {value}")

def eliminar_variables_env(ruta_env='.env'):
    """
    Elimina las variables del entorno basándose en un archivo .env.
    Además, verifica si el archivo .env está configurado para cargarse automáticamente
    y deshabilita esta funcionalidad si es necesario.
    """

    # Deshabilitar la recarga automática desde .env (si aplica en tu entorno)
    if 'ENV_FILE_LOADED' in os.environ:
        os.environ.pop('ENV_FILE_LOADED', None)

    # Leer manualmente las variables desde el archivo .env
    try:
        variables_env = dotenv_values(ruta_env)
    except FileNotFoundError:
        print(f"El archivo {ruta_env} no se encontró.")
        return

    # Eliminar las variables del entorno actual
    for variable, value in variables_env.items():
        if variable in os.environ:
            del os.environ[variable]
            print(f"Variable eliminada: {variable}")
        else:
            print(f"Variable no encontrada en el entorno: {variable}")

    print("Proceso de eliminación completado.")

    # Opcional: Mostrar las variables restantes en el entorno actual
    print("\nVariables de entorno actuales:")
    for key, value in os.environ.items():
        print(f"{key}: {value}")

# Configuración para deshabilitar carga de .env desde Visual Studio Code
if __name__ == "__main__":
    # Agregar un aviso para depurar si .env se está cargando automáticamente
    if os.getenv('PYTHON_ENV_FILE'):
        print("Advertencia: Un archivo .env está siendo cargado automáticamente.")

    # Llamar a la función principal
    eliminar_variables_env()
