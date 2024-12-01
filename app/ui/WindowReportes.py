from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QWidget, QMessageBox, QInputDialog
from PyQt5.QtGui import QPixmap, QFont, QIcon
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import pandas as pd
from app.ui.WindowPrincipal import VentanaPrincipal
from app.services.database import crear_conexion
import os

class ReportePDFScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Generar Reporte PDF')
        self.setMinimumSize(400, 600)

        self.fondo_label = QLabel(self)
        self.fondo_label.setPixmap(QPixmap(os.getenv('IMG_FONDO')))
        self.fondo_label.setScaledContents(True)  # Escalar la imagen para ajustarse al QLabel
        self.fondo_label.resize(self.size())

        self.setWindowIcon(QIcon(os.getenv('IMG_ICO')))

        self.fontNegrita = QFont("Arial", 14, QFont.Bold)

        # Layout para los botones
        layout = QVBoxLayout()

        # Botón para generar reporte PDF
        self.btn_generar_reporte = QPushButton("Generar Reporte PDF")
        self.btn_generar_reporte.clicked.connect(self.generar_reporte)
        layout.addWidget(self.btn_generar_reporte)

        # Botón para regresar a la pantalla principal
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(self.regresar_a_principal)
        layout.addWidget(self.btn_regresar)  # Aquí se usa el layout directamente

        self.setLayout(layout)  # Configura el layout para el widget


    def generar_reporte(self):
        # Solicitar al usuario que ingrese el DNI
        dni, ok = QInputDialog.getText(self, "Generar Reporte", "Ingrese el DNI del cliente:")
        if ok and dni:
            # Llama al método de generación de reporte
            self.generar_reporte_por_dni(dni)
        else:
            QMessageBox.warning(self, "Advertencia", "Debe ingresar un DNI válido.")

    def generar_reporte_por_dni(self, dni):
        # Obtener los datos del cliente y la reserva mediante el DNI
        datos = self.obtener_datos_por_dni(dni)

        if not datos:
            QMessageBox.warning(self, "Error", "No se encontraron datos para el DNI proporcionado.")
            return

        # Generar el reporte PDF
        archivo_pdf = self.generar_reporte_cliente_pdf(datos)
        if archivo_pdf:
            QMessageBox.information(self, "Reporte generado", f"El reporte PDF se ha generado: {archivo_pdf}")
        else:
            QMessageBox.warning(self, "Error", "No se pudo generar el reporte.")

    @staticmethod
    def obtener_datos_por_dni(dni):
        # Conectar a la base de datos
        conn = crear_conexion()
        if conn is None:
            return None

        cursor = conn.cursor()
        # Consulta SQL para obtener los datos por DNI
        query = """
        SELECT 
            t.nombre, 
            t.apellido, 
            t.telefono, 
            t.email, 
            t.nacionalidad, 
            cd.destino, 
            r.f_salida, 
            r.duracion_dias, 
            pt.tipo_paquete, 
            pt.hotel, 
            pt.precio_diario, 
            p.monto_total, 
            p.metodo, 
            p.ref_num
        FROM 
            turista t
        JOIN 
            reserva r ON t.id_turista = r.id_turista
        JOIN 
            paquete_turistico pt ON r.id_paquete = pt.id_paquete
        JOIN 
            catalogo_destino cd ON pt.id_cat_destino = cd.id_destino
        JOIN 
            pago p ON r.id_reserva = p.id_reserva
        WHERE 
            t.num_doc = %s;
        """

        try:
            cursor.execute(query, (dni,))
            datos = cursor.fetchone()  # Recupera solo un resultado
            return datos
        except Exception as e:
            print(f"Error al obtener datos por DNI: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    def generar_reporte_cliente_pdf(self, datos):
        if not datos:
            return "No hay datos para generar el reporte"

        archivo_pdf = f'reporte_cliente_{datos[0]}_{datos[1]}.pdf'
        c = canvas.Canvas(archivo_pdf, pagesize=letter)

        # Configuración del PDF
        c.setFont("Helvetica", 10)
        y = 750  # Posición inicial para escribir

        # Encabezado
        c.drawString(100, y, "Reporte de Reserva de Cliente")
        y -= 15
        c.drawString(100, y, f"Fecha del Reporte: {datetime.now().strftime('%Y-%m-%d')}")
        y -= 30

        # Datos del Cliente
        c.drawString(100, y, "________________________________________")
        y -= 15
        c.drawString(100, y, "Datos del Cliente")
        y -= 15
        c.drawString(100, y, f"• Nombre Completo: {datos[0]} {datos[1]}")
        y -= 15
        c.drawString(100, y, f"• Teléfono: {datos[2]}")
        y -= 15
        c.drawString(100, y, f"• Email: {datos[3]}")
        y -= 15
        c.drawString(100, y, f"• Nacionalidad: {datos[4]}")
        y -= 30

        # Detalles de la Reserva
        c.drawString(100, y, "________________________________________")
        y -= 15
        c.drawString(100, y, "Detalles de la Reserva")
        y -= 15
        c.drawString(100, y, f"• Destino: {datos[5]}")
        y -= 15
        c.drawString(100, y, f"• Fecha de Inicio del Viaje: {datos[6].strftime('%Y-%m-%d')}")
        y -= 15
        c.drawString(100, y, f"• Duración: {datos[7]} días")
        y -= 15
        c.drawString(100, y, f"• Paquete Turístico Seleccionado:")
        y -= 15
        c.drawString(110, y, f"o Tipo: {datos[8]}")
        y -= 15
        c.drawString(110, y, f"o Incluye Hotel: {'Sí' if datos[9] else 'No'}")
        y -= 15
        c.drawString(100, y, f"• Precio por Día: ${datos[10]:.2f}")
        y -= 15
        c.drawString(100, y, f"• Total de la Reserva: ${datos[11]:.2f}")
        y -= 30

        # Resumen de Pago
        c.drawString(100, y, "________________________________________")
        y -= 15
        c.drawString(100, y, "Resumen de Pago")
        y -= 15
        c.drawString(100, y, f"• Método de Pago: {datos[12]}")
        y -= 15
        c.drawString(100, y, f"• Monto Pagado: ${datos[11]:.2f}")
        y -= 15
        c.drawString(100, y, f"• Número de Referencia del Pago: {datos[13]}")
        y -= 30

        # Guardar el archivo PDF
        c.save()
        return archivo_pdf
    
    def regresar_a_principal(self):
        self.close()
        self.pantalla_principal = VentanaPrincipal()
        self.pantalla_principal.show()
