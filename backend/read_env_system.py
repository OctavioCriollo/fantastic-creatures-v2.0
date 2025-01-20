import os
from dotenv import load_dotenv

def mostrar_variables_env():
    print("Variables del archivo .env:")
    print("-" * 40)
    
    # Cargar las variables del archivo .env
    load_dotenv(override=True)
    
    # Obtener todas las variables de entorno
    variables = dict(os.environ)
    
    # Filtrar solo las variables que están en el archivo .env
    variables_env = {k: v for k, v in variables.items() if k in os.environ and os.environ[k] == v}
    
    # Ordenar las variables alfabéticamente por nombre
    variables_ordenadas = sorted(variables_env.items())
    
    # Mostrar cada variable y su valor
    for nombre, valor in variables_ordenadas:
        print(f"{nombre}: {valor}")
    
    print("-" * 40)
    print(f"Total de variables en .env: {len(variables_env)}")

def mostrar_todas_variables():
    print("\nTodas las variables de entorno (incluyendo las del sistema):")
    print("-" * 40)
    
    # Obtener todas las variables de entorno
    variables = dict(os.environ)
    
    # Ordenar las variables alfabéticamente por nombre
    variables_ordenadas = sorted(variables.items())
    
    # Mostrar cada variable y su valor
    for nombre, valor in variables_ordenadas:
        print(f"{nombre}: {valor}")
    
    print("-" * 40)
    print(f"Total de variables de entorno: {len(variables)}")

if __name__ == "__main__":
    mostrar_variables_env()
    
    # Descomenta la siguiente línea si quieres ver todas las variables de entorno
    # mostrar_todas_variables()