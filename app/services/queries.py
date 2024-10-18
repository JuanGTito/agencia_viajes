from app.services.database import crear_conexion

def insertar_turista(cursor, nombre, fecha_nacimiento, genero, telefono, email, numero_pasaporte, nacionalidad):
    cursor.execute("""
        INSERT INTO Turistas (Nombre_Completo, Fecha_de_nacimiento, Genero, Telefono, Email, Numero_de_pasaporte, Nacionalidad)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (nombre, fecha_nacimiento, genero, telefono, email, numero_pasaporte, nacionalidad))
    return cursor.lastrowid  # Retornar el ID del nuevo turista

def insertar_destino(cursor, id_turista, destino, precio, fecha_salida, fecha_regreso):
    cursor.execute("""
        INSERT INTO Destinos (ID_Turista, Destino_principal, Precio, Fecha_de_salida, Fecha_de_regreso)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_turista, destino, precio, fecha_salida, fecha_regreso))

def insertar_pago(cursor, id_turista, metodo_pago, monto, numero_referencia):
    cursor.execute("""
        INSERT INTO Pagos (ID_Turista, Metodo_de_pago, Monto, Numero_de_referencia)
        VALUES (%s, %s, %s, %s)
    """, (id_turista, metodo_pago, monto, numero_referencia))

def obtener_reserva(dni_pasaporte):
    """Buscar una reserva en la base de datos usando el número de pasaporte."""
    conn = crear_conexion()  # Conectar a la base de datos
    if conn is not None:
        cursor = conn.cursor()

        # Consultar en la tabla Turistas usando solo el número de pasaporte
        cursor.execute("""
            SELECT Nombre_Completo, Telefono, Nacionalidad
            FROM Turistas
            WHERE Numero_de_pasaporte = %s
        """, (dni_pasaporte,))

        turista = cursor.fetchone()

        if turista:
            nombre, telefono, nacionalidad = turista

            # Consultar en la tabla Destinos
            cursor.execute("""
                SELECT Destino_principal
                FROM Destinos
                WHERE ID_Turista = (
                    SELECT ID_Turista
                    FROM Turistas
                    WHERE Numero_de_pasaporte = %s
                )
            """, (dni_pasaporte,))

            destino = cursor.fetchone()

            conn.close()  # Cerrar la conexión

            # Devolver los datos en un diccionario
            return {
                'nombre': nombre,
                'telefono': telefono,
                'destino': destino[0] if destino else "No disponible",
                'nacionalidad': nacionalidad
            }
        
        conn.close()  # Cerrar la conexión
    return None  # Si no se encuentra la reserva

