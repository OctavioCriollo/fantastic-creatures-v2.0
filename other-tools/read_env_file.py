from dotenv import dotenv_values
import os

def leer_archivo_env(ruta_env='.env'):
    print(f"Intentando leer el archivo: {os.path.abspath(ruta_env)}")
    print("Variables del archivo .env:")
    print("-" * 40)
    
    # Leer directamente del archivo .env
    config = dotenv_values(ruta_env)
    
    if not config:
        print(f"No se encontraron variables en el archivo {ruta_env}")
        return
    
    # Mostrar cada variable y su valor
    for nombre, valor in config.items():
        print(f"{nombre}: {valor}")
    
    print("-" * 40)
    print(f"Total de variables en .env: {len(config)}")

if __name__ == "__main__":
    # Intenta leer el archivo .env en el directorio actual
    leer_archivo_env()
    
    # Si no se encuentra, pide al usuario que ingrese la ruta
    if input("¿Quieres especificar una ruta diferente para el archivo .env? (s/n): ").lower() == 's':
        ruta = input("Ingresa la ruta completa al archivo .env: ")
        leer_archivo_env(ruta)