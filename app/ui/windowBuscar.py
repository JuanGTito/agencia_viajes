from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
from app.services.queries import obtener_reserva
from app.ui.WindowPrincipal import VentanaPrincipal
import os

class BuscarReservaScreen(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle('Buscar Reserva')
        self.setFixedSize(800, 600)

        self.usuario = usuario

        self.fondo_label = QLabel(self)
        self.fondo_label.setPixmap(QPixmap(os.getenv('IMG_FONDO')))
        self.fondo_label.setScaledContents(True)
        self.fondo_label.resize(self.size())

        self.setWindowIcon(QIcon(os.getenv('IMG_ICO')))

        self.fontNegrita = QFont("Arial", 14, QFont.Bold)

        self.layout = QVBoxLayout()

        # Inicialización de la interfaz
        self.inicializar_interfaz()

        # Botón para regresar a la pantalla principal
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setFixedHeight(30)
        self.btn_regresar.setFont(self.fontNegrita)
        self.btn_regresar.clicked.connect(self.regresar_a_principal)

        # Contenedor horizontal para centrar el botón
        layout_centrado = QHBoxLayout()
        layout_centrado.addWidget(self.btn_regresar, alignment=Qt.AlignCenter)

        # Agregar el contenedor centrado al diseño principal
        self.layout.addLayout(layout_centrado)

        self.setLayout(self.layout)

    def inicializar_interfaz(self):
        """Método para inicializar la interfaz con los campos de búsqueda y tabla de resultados."""
        # Crear un layout horizontal para el campo de búsqueda
        h_layout_busqueda = QHBoxLayout()

        # ComboBox para seleccionar el criterio de búsqueda
        self.combo_criterio = QComboBox(self)
        self.combo_criterio.setFixedHeight(30)
        self.combo_criterio.setFont(self.fontNegrita)
        self.combo_criterio.addItems([
            "Nombre", "Documento/Pasaporte", "Destino", "Fecha de Salida",
            "Método de Pago", "Nacionalidad", "Fecha de Reserva"
        ])

        # Campo de entrada para el valor del criterio
        self.input_busqueda = QLineEdit(self)
        self.input_busqueda.setFixedHeight(30)
        self.input_busqueda.setPlaceholderText("Ingrese el valor de búsqueda")
        self.input_busqueda.setStyleSheet("QLineEdit { font-size: 14px; }")

        # Botón para realizar la búsqueda
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.setFont(self.fontNegrita)
        self.btn_buscar.clicked.connect(self.buscar_reserva)

        # Añadir los widgets al layout horizontal
        h_layout_busqueda.addWidget(self.combo_criterio)
        h_layout_busqueda.addWidget(self.input_busqueda)
        h_layout_busqueda.addWidget(self.btn_buscar)

        # Añadir el layout horizontal al layout principal
        self.layout.addLayout(h_layout_busqueda)

        # Crear la tabla para mostrar los resultados
        self.tabla_resultados = QTableWidget(self)
        self.tabla_resultados.setColumnCount(7)  # Número de columnas
        self.tabla_resultados.setHorizontalHeaderLabels([
            "Nombre", "Teléfono", "Destino", "Nacionalidad", "Email", "Tipo Paquete", "Monto Total"
        ])
        self.tabla_resultados.setStyleSheet("QTableWidget { font-size: 14px; }")
        self.tabla_resultados.setEditTriggers(QTableWidget.NoEditTriggers)  # Hacer la tabla de solo lectura
        self.tabla_resultados.setSelectionBehavior(QTableWidget.SelectRows)  # Selección por filas
        self.layout.addWidget(self.tabla_resultados)

    def buscar_reserva(self):
        """Buscar reservas en la base de datos y mostrar en la tabla."""
        criterio = self.combo_criterio.currentText()
        valor = self.input_busqueda.text()

        # Validar que el campo no esté vacío
        if not valor:
            QMessageBox.warning(self, "Campo vacío", "Por favor, ingrese un valor de búsqueda.")
            return

        # Mapear el criterio a los campos de la base de datos
        campo_busqueda = {
            "Nombre": "nombre",
            "Documento/Pasaporte": "num_doc",
            "Destino": "destino",
            "Fecha de Salida": "f_salida",
            "Método de Pago": "metodo",
            "Nacionalidad": "nacionalidad",
            "Fecha de Reserva": "f_reserva"
        }.get(criterio, "nombre")

        print(f"Campo de búsqueda: {campo_busqueda}, Valor: {valor}")
        # Realizar la búsqueda
        reservas = obtener_reserva(campo_busqueda, valor)  # Supongamos que este método acepta el campo y valor

        # Limpiar la tabla
        self.tabla_resultados.setRowCount(0)

        if reservas:
            self.tabla_resultados.setRowCount(len(reservas))
            for row, reserva in enumerate(reservas):
                self.tabla_resultados.setItem(row, 0, QTableWidgetItem(reserva['nombre']))
                self.tabla_resultados.setItem(row, 1, QTableWidgetItem(reserva['telefono']))
                self.tabla_resultados.setItem(row, 2, QTableWidgetItem(reserva['destino']))
                self.tabla_resultados.setItem(row, 3, QTableWidgetItem(reserva['nacionalidad']))
                self.tabla_resultados.setItem(row, 4, QTableWidgetItem(reserva['email']))
                self.tabla_resultados.setItem(row, 5, QTableWidgetItem(reserva['tipo_paquete']))
                self.tabla_resultados.setItem(row, 6, QTableWidgetItem(str(reserva['monto_total'])))
        else:
            QMessageBox.information(self, "Sin resultados", "No se encontraron reservas con ese criterio.")


    def regresar_a_principal(self):
        """Regresar a la pantalla principal."""
        self.close()
        self.pantalla_principal = VentanaPrincipal(self.usuario)
        self.pantalla_principal.show()
