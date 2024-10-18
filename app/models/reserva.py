from app.services.queries import insertar_turista, insertar_destino, insertar_pago, obtener_reserva
from app.services.database import crear_conexion

class Reserva:
    def __init__(self):
        self.destinos = {
            "Playa del Carmen": 500,
            "Cusco": 600,
            "Buenos Aires": 700,
            "Barcelona": 800,
            "Cancún": 550
        }

    def guardar_reserva(self, nombre, fecha_nacimiento, genero, telefono, email, pasaporte, nacionalidad,
                        destino, fecha_salida, fecha_regreso, metodo_pago, referencia):
        conn = crear_conexion()  # Conectar a la base de datos
        
        if conn is None:
            return False  # Si no se puede conectar, retornar False

        try:
            cursor = conn.cursor()

            # Verificar que el destino exista en el diccionario de destinos
            if destino not in self.destinos:
                raise ValueError(f"El destino '{destino}' no está disponible.")

            # Insertar en la tabla Turistas
            id_turista = insertar_turista(cursor, nombre, fecha_nacimiento, genero, telefono, email, pasaporte, nacionalidad)

            # Insertar en la tabla Destinos
            insertar_destino(cursor, id_turista, destino, self.destinos[destino], fecha_salida, fecha_regreso)

            # Insertar en la tabla Pagos
            insertar_pago(cursor, id_turista, metodo_pago, self.destinos[destino], referencia)

            conn.commit()  # Guardar cambios
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

    def obtener_reserva(self, dni_pasaporte):
        """Buscar una reserva en la base de datos usando DNI o pasaporte."""
        return obtener_reserva(dni_pasaporte)  # Utilizar la función de búsqueda en el servicio