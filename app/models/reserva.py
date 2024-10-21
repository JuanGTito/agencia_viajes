from app.services.queries import insertar_turista, insertar_destino, insertar_pago, obtener_reserva
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
            cursor.execute("SELECT id_destino, destino, precio FROM catalogo_destino")  # Cambia esta consulta según tu estructura de tabla
            destinos = cursor.fetchall()

            # Convertir la lista de tuplas a un diccionario
            # ID como clave y una tupla (nombre, precio) como valor
            return {id_destino: (nombre, precio) for id_destino, nombre, precio in destinos}

        except Exception as e:
            print(f"Error al obtener destinos: {e}")
            return {}

        finally:
            cursor.close()
            conn.close()


    def guardar_reserva(self, tipo_documento, num_documento, nombre, apellido, fecha_nacimiento, genero, telefono, email,
                    nacionalidad, destino, fecha_salida, fecha_regreso, metodo_pago, referencia=None):
        """Guarda una nueva reserva en la base de datos."""
        conn = crear_conexion()  # Conectar a la base de datos

        if conn is None:
            print("No se pudo conectar a la base de datos.")
            return False  # Si no se puede conectar, retornar False

        try:
            cursor = conn.cursor()

            # Obtener el ID del destino para la inserción
            id_destino = next((id for id, (d, _) in self.destinos.items() if d.strip().lower() == destino.strip().lower()), None)

            if id_destino is None:
                raise ValueError(f"El destino '{destino}' no está disponible.")

            # Insertar en la tabla Turistas
            try:
                id_turista = insertar_turista(cursor, nombre, apellido, fecha_nacimiento, genero, telefono, email, tipo_documento, num_documento, nacionalidad)
            except Exception as e:
                print(f"Error al insertar en la tabla Turistas: {e}")
                conn.rollback()  # Deshacer cambios si ocurre un error
                return False

            # Insertar en la tabla Destinos
            try:
                insertar_destino(cursor, id_turista, id_destino, fecha_salida, fecha_regreso)
            except Exception as e:
                print(f"Error al insertar en la tabla Destinos: {e}")
                conn.rollback()  # Deshacer cambios si ocurre un error
                return False

            # Insertar en la tabla Pagos
            try:
                insertar_pago(cursor, id_turista, metodo_pago, self.destinos[id_destino][1], referencia)
            except Exception as e:
                print(f"Error al insertar en la tabla Pagos: {e}")
                conn.rollback()  # Deshacer cambios si ocurre un error
                return False

            conn.commit()  # Guardar cambios si todo fue exitoso
            return True  # Retornar True si la reserva fue guardada correctamente

        except ValueError as ve:
            print(f"Error: {ve}")  # Manejar un error en el destino seleccionado
            return False

        except Exception as e:
            print(f"Error durante la transacción: {e}")  # Manejar cualquier otro error
            conn.rollback()  # Deshacer los cambios en caso de error
            return False

        finally:
            cursor.close()  # Cerrar cursor
            conn.close()  # Cerrar la conexión

    def obtener_reserva(self, num_documento):
        """Buscar una reserva en la base de datos usando el número de documento."""
        return obtener_reserva(num_documento)  # Utilizar la función de búsqueda en el servicio
