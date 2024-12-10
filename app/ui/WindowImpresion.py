from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
from datetime import datetime
import win32print
import win32api
from app.services.database import crear_conexion  # Importa la función para crear la conexión

class VentanaImpresion(QDialog):
    def __init__(self, num_doc, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Impresión de Boleta")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        # Obtención de datos desde la base de datos usando tipo_doc y num_doc
        # Se debe asegurarse de que obtener_datos_boleta reciba tipo_doc y num_doc
        datos = self.obtener_datos_boleta(num_doc)

        # Verifica que los datos han sido obtenidos correctamente
        if not datos:
            QMessageBox.critical(self, "Error", "No se encontraron datos para la boleta.")
            return

        # Asigna los valores obtenidos
        self.tipo_doc, self.num_doc, self.nombre, self.apellido, self.telefono, self.fecha_salida, self.monto_total = datos

        # Validación de los datos
        if not all([self.tipo_doc, self.num_doc, self.nombre, self.apellido, self.telefono, self.fecha_salida, self.monto_total]):
            QMessageBox.critical(self, "Error", "Faltan datos para generar la boleta.")
            return

        # Agregar la información al layout
        layout.addWidget(QLabel(f"Documento: {self.tipo_doc} {self.num_doc}"))
        layout.addWidget(QLabel(f"Cliente: {self.nombre} {self.apellido}"))
        layout.addWidget(QLabel(f"Fecha de Salida: {self.fecha_salida}"))
        layout.addWidget(QLabel(f"Monto Total: ${self.monto_total:.2f} USD"))

        # Botón para imprimir
        btn_imprimir = QPushButton("Imprimir")
        btn_imprimir.clicked.connect(self.imprimir_boleta)
        layout.addWidget(btn_imprimir)

        # Botón para cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.close)
        layout.addWidget(btn_cerrar)

        self.setLayout(layout)

    def obtener_datos_boleta(self, num_doc):
        """Obtiene los datos de la boleta desde la base de datos usando el número de documento del turista."""
        try:
            # Verifica si num_doc está vacío o es None
            if not num_doc:
                raise ValueError("El número de documento no es válido.")

            # Si num_doc es una cadena y debería ser un número (entero), lo convertimos
            if num_doc.isdigit():  # Verifica si num_doc es un número
                num_doc = int(num_doc)  # Convierte a entero

            print(f"Buscando datos para num_doc: {num_doc}")
            print(f"Tipo de num_doc: {type(num_doc)}")

            # Usamos la función crear_conexion para conectar a la base de datos
            connection = crear_conexion()  # Cambia a la función que importa la conexión
            cursor = connection.cursor()

            # Consulta SQL para obtener los datos de la boleta usando num_doc
            query = """
                SELECT t.tipo_doc, t.num_doc, t.nombre, t.apellido, t.telefono, r.f_salida, p.monto_total
                FROM reserva r
                JOIN turista t ON r.id_turista = t.id_turista
                JOIN pago p ON p.id_reserva = r.id_reserva
                WHERE t.num_doc = %s
            """

            # Ejecutar la consulta pasando el num_doc como parámetro
            cursor.execute(query, (num_doc,))

            # Obtener los resultados
            datos = cursor.fetchone()

            # Si no se encuentra la reserva
            if not datos:
                raise ValueError("Reserva no encontrada para el número de documento proporcionado.")

            print(f"Datos obtenidos: {datos}")

            # Desempaquetar los datos obtenidos de la consulta
            tipo_doc, num_doc, nombre, apellido, telefono, fecha_salida, monto_total = datos

            # Asegurarnos de que el monto sea un float
            monto_total = float(monto_total) if monto_total else 0.0

            return tipo_doc, num_doc, nombre, apellido, telefono, fecha_salida, monto_total

        except Exception as e:
            print(f"Error al obtener los datos de la boleta: {str(e)}")
            return None, None, None, None, None, None, None



    def imprimir_boleta(self):
        """Envía la boleta a la impresora predeterminada con el formato solicitado."""
        
        # Datos de la boleta
        agencia_nombre = "[Nombre de la Agencia de Viajes]"
        agencia_ruc = "12345678910"
        agencia_direccion = "Av. Turismo 123, Ciudad"
        agencia_telefono = "987654321"
        fecha = datetime.now().strftime("%d/%m/%Y")  # Fecha actual
        hora = datetime.now().strftime("%I:%M %p")   # Hora actual en formato 12 horas
        boleta_numero = "AGT-000123"
        
        # Formato de la boleta
        contenido_boleta = (
            f"Boleta de Pago - Agencia de Viajes\n"
            f"{agencia_nombre}\n"
            f"RUC: {agencia_ruc}\n"
            f"Dirección: {agencia_direccion}\n"
            f"Teléfono: {agencia_telefono}\n"
            f"Fecha: {fecha}\n"
            f"Hora: {hora}\n\n"
            
            f"Boleta de Venta N°: {boleta_numero}\n\n"
            
            f"CLIENTE\n"
            f"Nombre: {self.nombre} {self.apellido}\n"
            f"DNI/Pasaporte: {self.tipo_doc} {self.num_doc}\n"
            f"Teléfono: {self.telefono}\n\n"
            
            f"DETALLE DEL SERVICIO\n"
            f"Servicio: Paquete Turístico\n"
            f"Cantidad: 1\n"
            f"Precio Unitario: S/. {self.monto_total:.2f}\n"
            f"Total: S/. {self.monto_total:.2f}\n\n"
            
            f"TOTAL A PAGAR: S/. {self.monto_total:.2f}\n\n"
            
            f"FORMA DE PAGO:\n"
            f"Efectivo\n\n"
            
            f"POLÍTICAS DE SERVICIO\n"
            f"Las reservas se confirman con el pago completo. No se aceptan devoluciones una vez iniciado el viaje, y cualquier cambio en las fechas está sujeto a disponibilidad y costos adicionales. "
            f"Es responsabilidad del cliente tener toda la documentación necesaria (DNI/Pasaporte). La agencia no se hace responsable por inconvenientes causados por terceros, como aerolíneas, y los itinerarios pueden modificarse por razones externas. "
            f"En caso de emergencia, comuníquese al número: {agencia_telefono}.\n\n"
            
            f"¡Gracias por confiar en nosotros!\n"
            f"{agencia_nombre}\n"
        )

        try:
            # Obtener la impresora predeterminada
            impresora = win32print.GetDefaultPrinter()
            
            # Abrir un manejador de la impresora
            handle = win32print.OpenPrinter(impresora)
            
            # Configurar el trabajo de impresión
            job = win32print.StartDocPrinter(handle, 1, ("Boleta de Pago", None, "RAW"))
            win32print.StartPagePrinter(handle)
            
            # Enviar datos a la impresora
            win32print.WritePrinter(handle, contenido_boleta.encode("utf-8"))
            win32print.EndPagePrinter(handle)
            win32print.EndDocPrinter(handle)
            win32print.ClosePrinter(handle)

            # Mensaje de éxito
            QMessageBox.information(self, "Impresión Exitosa", "La boleta se ha enviado a la impresora.")
        except win32print.error as e:
            # Manejo de errores relacionados con la impresora
            QMessageBox.critical(self, "Error de Impresión", f"No se pudo imprimir la boleta. Error en la impresora: {str(e)}")
        except Exception as e:
            # Manejo de otros errores
            QMessageBox.critical(self, "Error General", f"No se pudo imprimir la boleta. Error: {str(e)}")