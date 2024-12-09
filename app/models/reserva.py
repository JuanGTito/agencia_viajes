from app.services.queries import insertar_turista, insertar_reserva, insertar_pago, obtener_reserva
from app.services.database import crear_conexion

class Reserva:
    def __init__(self):
        self.destinos = self.obtener_destinos()

    def obtener_destinos(self):
        """Obtiene los destinos disponibles desde la base de datos."""

        conn = crear_conexion()
        if conn is None:
            return {}

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id_destino, destino, descripcion FROM catalogo_destino")  # Cambia esta consulta según tu estructura de tabla
            destinos = cursor.fetchall()

            # Convertir la lista de tuplas a un diccionario
            # ID como clave y una tupla (nombre, precio) como valor
            return {id_destino: (destino, descripcion) for id_destino, destino, descripcion in destinos}
        
        except Exception as e:
            print(f"Error al obtener destinos: {e}")
            return {}

        finally:
            cursor.close()
            conn.close()
    
    def obtener_paquetes_por_destino(self, id_destino_seleccionado):
        conn = crear_conexion()
        paquetes = []

        if conn:
            cursor = conn.cursor()
            try:
                # Asegúrate de que el id_destino_seleccionado sea un entero válido
                if not isinstance(id_destino_seleccionado, int):
                    raise ValueError("El id_destino debe ser un número entero válido")

                print(f"ID de destino seleccionado: {id_destino_seleccionado}")

                # Crear la consulta sin usar parámetros
                consulta = f"""
                    SELECT id_paquete, tipo_paquete, hotel, precio_diario
                    FROM paquete_turistico
                    WHERE id_cat_destino = {id_destino_seleccionado}
                """
                cursor.execute(consulta)

                # Recuperar los paquetes
                paquetes = cursor.fetchall()
                print(f"Paquetes obtenidos: {paquetes}")

            except Exception as e:
                print(f"Error al obtener los paquetes turísticos: {e}")

            finally:
                cursor.close()
                conn.close()

        return paquetes
    
    def guardar_reserva(self, tipo_documento, num_documento, nombre, apellido, fecha_nacimiento, genero, telefono, email,
                    nacionalidad, duracion_dias, fecha_salida, monto_total, id_paquete, metodo_pago, referencia=None):
        """Guarda una nueva reserva en la base de datos."""

        print(f"tipo_documento: {tipo_documento}")
        print(f"num_documento: {num_documento}")
        print(f"nombre: {nombre}, apellido: {apellido}")
        print(f"fecha_nacimiento: {fecha_nacimiento}, genero: {genero}")
        print(f"telefono: {telefono}, email: {email}")
        print(f"nacionalidad: {nacionalidad}")
        print(f"duracion_dias: {duracion_dias}, fecha_salida: {fecha_salida}")
        print(f"monto_total: {monto_total}, id_paquete: {id_paquete}")
        print(f"metodo_pago: {metodo_pago}, referencia: {referencia}")

        conn = crear_conexion()  # Conectar a la base de datos

        if conn is None:
            print("No se pudo conectar a la base de datos.")
            return False  # Si no se puede conectar, retornar False

        try:
            with conn:  # Usar `with` para asegurar que la conexión se cierre automáticamente
                with conn.cursor() as cursor:  # Usar `with` para asegurar que el cursor se cierre automáticamente

                    # Insertar en la tabla Turistas
                    try:
                        id_turista = insertar_turista(cursor, nombre, apellido, fecha_nacimiento, genero, telefono, email, tipo_documento, num_documento, nacionalidad)
                    except Exception as e:
                        print(f"Error al insertar en la tabla Turistas: {e}")
                        return False  # Deshacer cambios si ocurre un error

                    # Insertar en la tabla Reserva
                    try:      
                        id_reserva = insertar_reserva(cursor, id_turista, id_paquete, fecha_salida, duracion_dias)
                    except Exception as e:
                        print(f"Error al insertar en la tabla Reserva: {e}")
                        return False  # Deshacer cambios si ocurre un error

                    # Insertar en la tabla Pagos
                    try:
                        insertar_pago(cursor, id_turista, id_reserva, metodo_pago, monto_total, referencia)
                    except Exception as e:
                        print(f"Error al insertar en la tabla Pagos: {e}")
                        return False  # Deshacer cambios si ocurre un error

                conn.commit()  # Guardar cambios si todo fue exitoso
                return True  # Retornar True si la reserva fue guardada correctamente

        except ValueError as ve:
            print(f"Error: {ve}")  # Manejar un error en el destino seleccionado
            return False

        except Exception as e:
            print(f"Error durante la transacción: {e}")  # Manejar cualquier otro error
            return False

    def obtener_reserva(self, num_documento):
        """Buscar una reserva en la base de datos usando el número de documento."""
        return obtener_reserva(num_documento)  # Utilizar la función de búsqueda en el servicio
