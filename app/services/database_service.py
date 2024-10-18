# app/services/database_service.py
from app.services.database import crear_conexion

def verificar_conexion_bd():
    """Verificar si la conexión a la base de datos es exitosa."""
    print("Verificando conexión a la base de datos...")
    conexion = crear_conexion()
    if conexion is not None:
        print("Conexión exitosa.")
        conexion.close()  # Cerrar la conexión después de la verificación
        return True
    else:
        print("No se pudo conectar.")
        return False
