from app.services.database import crear_conexion
from datetime import datetime

def insertar_turista(cursor, nombre, apellido, fecha_nacimiento, genero, telefono, email, tipo_documento, numero_documento, nacionalidad):
    """Inserta un nuevo turista en la base de datos."""
    print(f"Insertando turista: {nombre}, {apellido}, {fecha_nacimiento}, {genero}, {telefono}, {email}, {tipo_documento}, {numero_documento}, {nacionalidad}")
    try:
        cursor.execute(""" 
            INSERT INTO turista (nombre, apellido, fnac, genero, telefono, email, tipo_doc, num_doc, nacionalidad)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, fecha_nacimiento, genero, telefono, email, tipo_documento, numero_documento, nacionalidad))
        return cursor.lastrowid  # Retornar el ID del nuevo turista

    except Exception as e:
        print(f"Error al insertar turista: {e}")  # Manejo de errores
        raise  # Propagar el error para manejo externo

fecha_reserva = datetime.now().date()  # Obtiene la fecha en formato 'YYYY-MM-DD'
fecha_reserva = fecha_reserva.strftime('%Y-%m-%d')  # Aseguramos el formato correcto # Convertir a 'DD-MM-YYYY'

print(f"Fecha de reserva generada: {fecha_reserva}")

def insertar_reserva(cursor, id_turista, id_paquete, fecha_salida, duracion_dias):
    """Inserta una nueva reserva asociada a un turista."""
    print(f"Insertando reserva: id_turista={id_turista}, id_paquete={id_paquete}, f_reserva={fecha_reserva}, f_salida={fecha_salida}, duracion_dias={duracion_dias}")
    try:

        print(f"Insertando reserva: id_turista={id_turista}, id_paquete={id_paquete}, f_reserva={fecha_reserva}, f_salida={fecha_salida}, duracion_dias={duracion_dias}")
        
        cursor.execute(""" 
            INSERT INTO reserva (id_turista, id_paquete, f_reserva, f_salida, duracion_dias)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_turista, id_paquete, fecha_reserva, fecha_salida, duracion_dias))
        
        # Retornar el ID de la reserva insertada
        id_reserva = cursor.lastrowid

        print(f"Reserva insertada con ID: {id_reserva}")

        return id_reserva

    except Exception as e:
        print(f"Error al insertar reserva: {e}")  # Manejo de errores
        raise  # Propagar el error para manejo externo


def insertar_pago(cursor, id_turista, id_reserva, metodo, monto_total, ref_num=None):
    """Inserta un nuevo pago realizado por un turista."""
    print(f"Insertando pago: id_turista={id_turista}, id_reserva={id_reserva}, metodo={metodo}, monto_total={monto_total}, ref_num={ref_num}")
    try:
        cursor.execute(""" 
            INSERT INTO pago (id_turista, id_reserva, metodo, monto_total, ref_num)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_turista, id_reserva, metodo, monto_total, ref_num))

    except Exception as e:
        print(f"Error al insertar pago: {e}")  # Manejo de errores
        raise  # Propagar el error para manejo externo

def obtener_reserva(numero_documento):
    """Buscar una reserva en la base de datos usando el número de documento."""
    if not numero_documento:
        print("El número de documento es obligatorio.")
        return None  # Validación previa de entrada

    conn = crear_conexion()  # Conectar a la base de datos
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return None  # Retornar None si no se puede conectar

    cursor = conn.cursor()
    try:
        # Consultar en la tabla turistas usando el número de documento
        cursor.execute(""" 
            SELECT nombre, apellido, telefono, nacionalidad, email
            FROM turista
            WHERE num_doc = %s
        """, (numero_documento,))

        turista = cursor.fetchone()
        if not turista:
            print(f"No se encontró un turista con el número de documento: {numero_documento}")
            return None  # Si no se encuentra el turista, retornar None

        nombre, apellido, telefono, nacionalidad, email = turista

        # Consultar en la tabla pagos, reservas, paquetes y destinos
        cursor.execute(""" 
            SELECT 
                cd.destino,
                pt.tipo_paquete,
                p.monto_total,
                r.f_reserva,
                r.f_salida,
                r.duracion_dias,
                p.metodo
            FROM 
                pago p
            JOIN 
                reserva r ON p.id_reserva = r.id_reserva
            JOIN 
                paquete_turistico pt ON r.id_paquete = pt.id_paquete
            JOIN 
                catalogo_destino cd ON pt.id_cat_destino = cd.id_destino
            WHERE 
                p.id_turista = (
                    SELECT id_turista
                    FROM turista
                    WHERE num_doc = %s
                )
        """, (numero_documento,))

        destino = cursor.fetchone()

        if destino:
            print("Resultado de la consulta destino:", destino)  # Imprimir el resultado para verificar

            # Ahora esperamos 7 valores, así que ajustamos el unpacking
            destino, tipo_paquete, monto_total, f_reserva, f_salida, duracion_dias, metodo = destino

            # Devolver los datos en un diccionario
            resultado = {
                'nombre': nombre,
                'apellido': apellido,
                'telefono': telefono,
                'email': email,
                'nacionalidad': nacionalidad,
                'destino': destino,  # Asignar el destino correctamente
                'tipo_paquete': tipo_paquete,
                'monto_total': monto_total,
                'f_reserva': f_reserva,
                'f_salida': f_salida,
                'duracion_dias': duracion_dias,
                'metodo': metodo
            }

            return resultado
        else:
            print(f"No se encontró una reserva asociada al documento: {numero_documento}")
            return None  # Si no se encuentra la reserva

    except Exception as e:
        print(f"Error durante la consulta: {e}")  # Manejo de errores
        return None  # Retornar None si ocurre un error

    finally:
        cursor.close()  # Cerrar cursor
        conn.close()  # Cerrar la conexión
