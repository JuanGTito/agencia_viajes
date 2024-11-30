from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton, QMessageBox
from app.models.reserva import Reserva 
from app.ui.WindowPrincipal import VentanaPrincipal

class DestinosScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Destinos")
        self.setGeometry(100, 100, 600, 500)  # Configura la posición y el tamaño de la ventana

        # Layout principal
        self.layout = QVBoxLayout()

        # Etiqueta
        self.label = QLabel("Destinos Disponibles:")
        self.layout.addWidget(self.label)

        # Tabla de destinos
        self.tabla_destinos = QTableWidget()
        self.tabla_destinos.setColumnCount(2)  # Dos columnas: Nombre y Precio
        self.tabla_destinos.setHorizontalHeaderLabels(["Lugar", "Descripcion"])  # Encabezados de columnas
        self.cargar_destinos()  # Cargar destinos desde la base de datos
        
        # Configuración de la tabla
        self.tabla_destinos.setSelectionBehavior(QTableWidget.SelectRows)  # Selección de fila
        self.tabla_destinos.setSelectionMode(QTableWidget.NoSelection)  # Sin selección
        self.tabla_destinos.setShowGrid(False)  # Ocultar líneas de cuadrícula
        self.tabla_destinos.setAlternatingRowColors(True)  # Colores alternos para filas
        
        self.layout.addWidget(self.tabla_destinos)

        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(self.regresar_a_principal)  # Conectar a la función de regreso
        self.layout.addWidget(self.btn_regresar)

        self.setLayout(self.layout)

    def cargar_destinos(self):
        """Carga los destinos en la tabla."""
        reserva = Reserva()  # Instancia de la clase Reserva
        destinos = reserva.obtener_destinos()  # Obtener destinos

        if not destinos:
            QMessageBox.warning(self, "Sin Destinos", "No hay destinos disponibles.")
            return
        
        # Configurar filas de la tabla
        self.tabla_destinos.setRowCount(len(destinos))  # Establecer el número de filas según el número de destinos
        
        # Llenar la tabla con los datos de los destinos
        for row, (id_destino, (nombre, descripcion)) in enumerate(destinos.items()):
            self.tabla_destinos.setItem(row, 0, QTableWidgetItem(nombre))  # Columna 0: Nombre del lugar
            self.tabla_destinos.setItem(row, 1, QTableWidgetItem(descripcion))  # Columna 1: Precio

        # Ajustar tamaño de columnas
        self.tabla_destinos.resizeColumnsToContents()  # Ajustar el tamaño de las columnas automáticamente

    def regresar_a_principal(self):
        self.close()
        self.pantalla_principal = VentanaPrincipal()
        self.pantalla_principal.show()
