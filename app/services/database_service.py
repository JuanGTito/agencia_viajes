# app/services/database_service.py
from app.services.database import crear_conexion

# Variable global para controlar la conexión
conexion_establecida = False
conexion = None  # Mantener la conexión abierta

def verificar_conexion_bd():
    """Verificar si la conexión a la base de datos es exitosa."""
    global conexion_establecida, conexion
    if not conexion_establecida:
        print("Verificando conexión a la base de datos...")
        conexion = crear_conexion()
        if conexion is not None:
            print("Conexión exitosa.")  # Solo imprimir aquí
            conexion_establecida = True  # Marcar la conexión como establecida
            return True
        else:
            print("No se pudo conectar.")
            conexion_establecida = False
            return False
    else:
        print("Conexión ya verificada.")  # Solo imprimir si ya está verificada
        return True

def obtener_conexion():
    """Retorna la conexión establecida si está disponible."""
    return conexion
