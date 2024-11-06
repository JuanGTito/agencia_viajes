from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QWidget, QMessageBox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import pandas as pd
from app.services.database import crear_conexion

class ReportePDFScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Generar Reporte PDF')
        self.setGeometry(100, 100, 400, 300)

        # Layout para los botones
        layout = QVBoxLayout()

        # Botón para generar reporte PDF
        self.btn_generar_reporte = QPushButton("Generar Reporte PDF")
        self.btn_generar_reporte.clicked.connect(self.generar_reporte)
        layout.addWidget(self.btn_generar_reporte)

        # Botón para generar reporte Excel
        self.btn_generar_excel = QPushButton("Generar Reporte Excel")
        self.btn_generar_excel.clicked.connect(self.generar_reporte_excel)
        layout.addWidget(self.btn_generar_excel)

        self.setLayout(layout)

    def generar_reporte(self):
        # Obtener los datos de la base de datos
        datos = self.obtener_datos_reservas()
        
        # Generar el reporte PDF
        reporte_pdf = self.generar_reporte_pdf(datos)
        
        if reporte_pdf:
            QMessageBox.information(self, "Reporte generado", f"El reporte PDF se ha generado: {reporte_pdf}")
        else:
            QMessageBox.warning(self, "Error", "No se pudo generar el reporte.")

    @staticmethod
    def obtener_datos_reservas():
        # Obtener la conexión a la base de datos
        conn = crear_conexion()
        if conn is None:
            return None

        cursor = conn.cursor()

        # Consulta SQL para obtener los datos que necesitas
        query = """
        SELECT 
            t.nombre, 
            t.apellido, 
            t.telefono, 
            cd.destino, 
            pt.tipo_paquete, 
            p.monto_total, 
            r.f_reserva, 
            r.f_salida,
            r.duracion_dias, 
            p.metodo
        FROM 
            reserva r
        JOIN 
            turista t ON r.id_turista = t.id_turista
        JOIN 
            paquete_turistico pt ON r.id_paquete = pt.id_paquete
        JOIN 
            catalogo_destino cd ON pt.id_cat_destino = cd.id_destino
        JOIN 
            pago p ON r.id_reserva = p.id_reserva;
        """

        try:
            cursor.execute(query)
            datos = cursor.fetchall()  # Recupera todos los resultados
            return datos
        except Exception as e:
            print(f"Error al obtener datos: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def generar_reporte_pdf(self, datos):
        if not datos:
            return "No hay datos para generar el reporte"

        archivo_pdf = 'reporte_reservas.pdf'
        c = canvas.Canvas(archivo_pdf, pagesize=letter)

        # Cargar fuente TrueType (por ejemplo, DejaVu Sans)
        c.setFont("Helvetica", 10)
        y = 750  # Posición inicial para comenzar a escribir en el PDF

        # Encabezado del reporte
        c.drawString(100, y, "Reporte de Reservas - Agencia de Viajes")
        y -= 20

        # Iterar sobre los datos y escribirlos en el PDF
        for i, reserva in enumerate(datos, 1):
            c.drawString(100, y, f"{i}. Cliente: {reserva[0]} {reserva[1]}")
            y -= 15
            c.drawString(100, y, f"- Destino: {reserva[3]}")
            y -= 15
            c.drawString(100, y, f"- Paquete: {reserva[4]}")
            y -= 15
            c.drawString(100, y, f"- Monto Total: {str(reserva[5])}")
            y -= 15
            c.drawString(100, y, f"- Fecha de Reserva: {reserva[6].strftime('%d/%m/%Y')}")
            y -= 15
            c.drawString(100, y, f"- Fecha de Salida: {reserva[7].strftime('%d/%m/%Y')}")
            y -= 15
            c.drawString(100, y, f"- Duración: {reserva[8]} días")
            y -= 15
            c.drawString(100, y, f"- Método de Pago: {reserva[9]}")
            y -= 20  # Separar las reservas por 20 unidades de distancia

            # Control de salto de página si es necesario
            if y < 100:
                c.showPage()  # Salta a una nueva página
                c.setFont("Helvetica", 10)
                y = 750  # Restablecer la posición y

        # Guardar el archivo PDF
        c.save()
        return archivo_pdf

    def generar_reporte_excel(self, datos):
        if not datos:
            print("No hay datos para generar el reporte")  # Mensaje de depuración
            return "No hay datos para generar el reporte"

        try:
            # Convertir los datos a un DataFrame
            df = pd.DataFrame(datos, columns=["Nombre", "Apellido", "Telefono", "Destino", "Tipo Paquete", "Monto Total", "Fecha Reserva", "Fecha Salida", "Duración", "Método de Pago"])
            
            # Mostrar el DataFrame antes de guardarlo para depuración
            print("Datos para Excel:")
            print(df)

            # Guardar el DataFrame a un archivo Excel
            archivo_excel = 'reporte_reservas.xlsx'
            df.to_excel(archivo_excel, index=False)

            print(f"Archivo Excel generado: {archivo_excel}")  # Mensaje de depuración
            return archivo_excel
        except Exception as e:
            print(f"Error al generar el archivo Excel: {e}")
            return None
