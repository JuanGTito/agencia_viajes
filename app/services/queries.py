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

def obtener_reserva(campo_busqueda, valor):
    """Buscar reservas en la base de datos usando un campo y un valor."""
    if not campo_busqueda or not valor:
        print("El campo y el valor de búsqueda son obligatorios.")
        return None

    conn = crear_conexion()  # Conectar a la base de datos
    if conn is None:
        print("No se pudo conectar a la base de datos.")
        return None

    cursor = conn.cursor()
    try:
        # Construir la consulta dinámica basada en el campo
        query = f"""
            SELECT 
                t.nombre, t.apellido, t.telefono, t.nacionalidad, t.email,
                cd.destino, pt.tipo_paquete, p.monto_total,
                r.f_reserva, r.f_salida, r.duracion_dias, p.metodo
            FROM 
                turista t
            JOIN 
                pago p ON t.id_turista = p.id_turista
            JOIN 
                reserva r ON p.id_reserva = r.id_reserva
            JOIN 
                paquete_turistico pt ON r.id_paquete = pt.id_paquete
            JOIN 
                catalogo_destino cd ON pt.id_cat_destino = cd.id_destino
            WHERE 
                {campo_busqueda} LIKE %s
        """
        cursor.execute(query, (f"%{valor}%",))  # Usar LIKE para búsquedas parciales

        # Obtener todas las filas coincidentes
        resultados = cursor.fetchall()

        # Si no hay resultados, retornar vacío
        if not resultados:
            print(f"No se encontraron reservas para el criterio: {campo_busqueda} con valor: {valor}")
            return []

        # Procesar los resultados y devolverlos como una lista de diccionarios
        reservas = []
        for resultado in resultados:
            reservas.append({
                'nombre': resultado[0],
                'apellido': resultado[1],
                'telefono': resultado[2],
                'nacionalidad': resultado[3],
                'email': resultado[4],
                'destino': resultado[5],
                'tipo_paquete': resultado[6],
                'monto_total': resultado[7],
                'f_reserva': resultado[8],
                'f_salida': resultado[9],
                'duracion_dias': resultado[10],
                'metodo': resultado[11]
            })

        return reservas

    except Exception as e:
        print(f"Error durante la consulta: {e}")
        return []

    finally:
        cursor.close()  # Cerrar el cursor
        conn.close()  # Cerrar la conexión
