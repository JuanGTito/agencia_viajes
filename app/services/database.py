import pymysql
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

def crear_conexion():
    """Función para crear y verificar la conexión a la base de datos."""
    try:
        conexion = pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        print("Conexión a la base de datos establecida.")
        return conexion
    except pymysql.MySQLError as err:  # Cambiar a pymysql.MySQLError
        print(f"Error al conectar a la base de datos: {err}")
        return None