from app.services.database import crear_conexion

def insertar_turista(cursor, nombre, apellido, fecha_nacimiento, genero, telefono, email, tipo_documento, numero_documento, nacionalidad):
    """Inserta un nuevo turista en la base de datos."""
    try:
        cursor.execute(""" 
            INSERT INTO turista (nombre, apellido, fnac, genero, telefono, email, tipo_doc, num_doc, nacionalidad)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, fecha_nacimiento, genero, telefono, email, tipo_documento, numero_documento, nacionalidad))
        return cursor.lastrowid  # Retornar el ID del nuevo turista

    except Exception as e:
        print(f"Error al insertar turista: {e}")  # Manejo de errores
        raise  # Propagar el error para manejo externo

def insertar_destino(cursor, id_turista, id_destino, fecha_salida, fecha_regreso):
    """Inserta un nuevo destino asociado a un turista."""
    try:
        cursor.execute(""" 
            INSERT INTO destino (id_turista, id_cat_destino, f_salida, f_regreso)
            VALUES (%s, %s, %s, %s)
        """, (id_turista, id_destino, fecha_salida, fecha_regreso))

    except Exception as e:
        print(f"Error al insertar destino: {e}")  # Manejo de errores
        raise  # Propagar el error para manejo externo

def insertar_pago(cursor, id_turista, metodo_pago, monto, numero_referencia):
    """Inserta un nuevo pago realizado por un turista."""
    try:
        cursor.execute(""" 
            INSERT INTO pago (id_turista, metodo, monto, ref_num)
            VALUES (%s, %s, %s, %s)
        """, (id_turista, metodo_pago, monto, numero_referencia))

    except Exception as e:
        print(f"Error al insertar pago: {e}")  # Manejo de errores
        raise  # Propagar el error para manejo externo

def obtener_reserva(numero_documento):
    """Buscar una reserva en la base de datos usando el número de documento."""
    conn = crear_conexion()  # Conectar a la base de datos
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return None  # Retornar None si no se puede conectar

    cursor = conn.cursor()
    try:
        # Consultar en la tabla turistas usando el número de documento
        cursor.execute(""" 
            SELECT nombre, apellido, telefono, nacionalidad
            FROM turista
            WHERE num_doc = %s
        """, (numero_documento,))

        turista = cursor.fetchone()
        if not turista:
            return None  # Si no se encuentra el turista, retornar None

        nombre, apellido, telefono, nacionalidad = turista

        # Consultar en la tabla destinos
        cursor.execute(""" 
            SELECT cd.destino
            FROM destino d
            JOIN catalogo_destino cd ON d.id_cat_destino = cd.id_destino
            WHERE d.id_turista = (
                SELECT id_turista
                FROM turista
                WHERE num_doc = %s
            )
        """, (numero_documento,))

        destino = cursor.fetchone()

        # Devolver los datos en un diccionario
        resultado = {
            'nombre': nombre,
            'apellido': apellido,
            'telefono': telefono,
            'destino': destino[0] if destino else "No disponible",
            'nacionalidad': nacionalidad
        }
        return resultado
        
    except Exception as e:
        print(f"Error durante la consulta: {e}")  # Manejo de errores
        return None  # Retornar None si ocurre un error

    finally:
        cursor.close()  # Cerrar cursor
        conn.close()  # Cerrar la conexión