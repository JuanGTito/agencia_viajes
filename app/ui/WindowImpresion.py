from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel, QPushButton, QMessageBox
from datetime import datetime
import win32print
import win32api
import os  # Para manejar archivos
from app.services.database import crear_conexion  # Importa la función para crear la conexión

class VentanaImpresion(QDialog):
    def __init__(self, num_doc, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Impresión de Boleta")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        # Obtención de datos desde la base de datos usando tipo_doc y num_doc
        datos = self.obtener_datos_boleta(num_doc)

        if not datos:
            QMessageBox.critical(self, "Error", "No se encontraron datos para la boleta.")
            return

        # Asigna los valores obtenidos
        self.tipo_doc, self.num_doc, self.nombre, self.apellido, self.telefono, self.fecha_salida, self.monto_total = datos

        # Validación de los datos
        if not all([self.tipo_doc, self.num_doc, self.nombre, self.apellido, self.telefono, self.fecha_salida, self.monto_total]):
            QMessageBox.critical(self, "Error", "Faltan datos para generar la boleta.")
            return

        layout.addWidget(QLabel(f"Documento: {self.tipo_doc} {self.num_doc}"))
        layout.addWidget(QLabel(f"Cliente: {self.nombre} {self.apellido}"))
        layout.addWidget(QLabel(f"Fecha de Salida: {self.fecha_salida}"))
        layout.addWidget(QLabel(f"Monto Total: ${self.monto_total:.2f} USD"))

        btn_imprimir = QPushButton("Imprimir")
        btn_imprimir.clicked.connect(self.imprimir_boleta)
        layout.addWidget(btn_imprimir)

        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.close)
        layout.addWidget(btn_cerrar)

        self.setLayout(layout)

    def obtener_datos_boleta(self, num_doc):
        try:
            if not num_doc:
                raise ValueError("El número de documento no es válido.")
            if num_doc.isdigit():
                num_doc = int(num_doc)

            connection = crear_conexion()
            cursor = connection.cursor()

            query = """
                SELECT t.tipo_doc, t.num_doc, t.nombre, t.apellido, t.telefono, r.f_salida, p.monto_total
                FROM reserva r
                JOIN turista t ON r.id_turista = t.id_turista
                JOIN pago p ON p.id_reserva = r.id_reserva
                WHERE t.num_doc = %s
            """
            cursor.execute(query, (num_doc,))
            datos = cursor.fetchone()

            if not datos:
                raise ValueError("Reserva no encontrada para el número de documento proporcionado.")

            tipo_doc, num_doc, nombre, apellido, telefono, fecha_salida, monto_total = datos
            monto_total = float(monto_total) if monto_total else 0.0

            return tipo_doc, num_doc, nombre, apellido, telefono, fecha_salida, monto_total

        except Exception as e:
            print(f"Error al obtener los datos de la boleta: {str(e)}")
            return None, None, None, None, None, None, None

    def imprimir_boleta(self):
        """Genera el PDF y lo envía a la impresora predeterminada."""
        
        # Datos de la boleta
        agencia_nombre = "[Nombre de la Agencia de Viajes]"
        agencia_ruc = "12345678910"
        agencia_direccion = "Av. Turismo 123, Ciudad"
        agencia_telefono = "987654321"
        fecha = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%I:%M %p")
        boleta_numero = "AGT-000123"
        
        # Crear el archivo PDF con reportlab
        pdf_path = f"C:\\Users\\Darcknet\\Downloads\\boleta_{self.num_doc}_{self.tipo_doc}.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Escribir el contenido de la boleta en el PDF
        c.drawString(100, height - 50, f"Boleta de Pago - Agencia de Viajes")
        c.drawString(100, height - 70, f"{agencia_nombre}")
        c.drawString(100, height - 90, f"RUC: {agencia_ruc}")
        c.drawString(100, height - 110, f"Dirección: {agencia_direccion}")
        c.drawString(100, height - 130, f"Teléfono: {agencia_telefono}")
        c.drawString(100, height - 150, f"Fecha: {fecha}")
        c.drawString(100, height - 170, f"Hora: {hora}")
        c.drawString(100, height - 200, f"Boleta de Venta N°: {boleta_numero}")
        
        c.drawString(100, height - 220, f"CLIENTE")
        c.drawString(100, height - 240, f"Nombre: {self.nombre} {self.apellido}")
        c.drawString(100, height - 260, f"DNI/Pasaporte: {self.tipo_doc} {self.num_doc}")
        c.drawString(100, height - 280, f"Teléfono: {self.telefono}")
        
        c.drawString(100, height - 300, f"DETALLE DEL SERVICIO")
        c.drawString(100, height - 320, f"Servicio: Paquete Turístico")
        c.drawString(100, height - 340, f"Cantidad: 1")
        c.drawString(100, height - 360, f"Precio Unitario: S/. {self.monto_total:.2f}")
        c.drawString(100, height - 380, f"Total: S/. {self.monto_total:.2f}")
        
        c.drawString(100, height - 400, f"TOTAL A PAGAR: S/. {self.monto_total:.2f}")
        c.drawString(100, height - 420, f"FORMA DE PAGO: Efectivo")
        
        c.drawString(100, height - 440, f"POLÍTICAS DE SERVICIO")
        c.drawString(100, height - 460, f"Las reservas se confirman con el pago completo...")
        
        c.drawString(100, height - 480, f"¡Gracias por confiar en nosotros!")
        c.drawString(100, height - 500, f"{agencia_nombre}")
        
        c.save()

        # Enviar el PDF a la impresora
        try:
            win32api.ShellExecute(0, "print", pdf_path, None, ".", 0)
            QMessageBox.information(self, "Impresión Exitosa", "La boleta se ha enviado a la impresora.")
        except Exception as e:
            QMessageBox.critical(self, "Error de Impresión", f"No se pudo imprimir la boleta. Error: {str(e)}")

    def guardar_boleta_en_archivo(self, contenido_boleta):
        try:
            carpeta_destino = os.path.expanduser(r"C:\Users\Darcknet\Downloads")
            if not os.path.exists(carpeta_destino):
                os.makedirs(carpeta_destino)

            archivo_boleta = os.path.join(carpeta_destino, f"boleta_{self.num_doc}_{self.tipo_doc}.txt")
            with open(archivo_boleta, 'w', encoding='utf-8') as archivo:
                archivo.write(contenido_boleta)

            QMessageBox.information(self, "Archivo Guardado", f"La boleta se ha guardado en el archivo: {archivo_boleta}")
        except Exception as e:
            QMessageBox.critical(self, "Error al Guardar", f"No se pudo guardar la boleta en el archivo. Error: {str(e)}")
