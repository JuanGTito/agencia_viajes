from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QLabel
from PyQt5.QtCore import Qt
import os

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Agencia de Viajes')
        self.setMinimumSize(600, 800)

        self.fondo_label = QLabel(self)
        self.fondo_label.setPixmap(QPixmap(os.getenv('IMG_FONDO')))
        self.fondo_label.setScaledContents(True)  # Escalar la imagen para ajustarse al QLabel
        self.fondo_label.resize(self.size())

        self.setWindowIcon(QIcon(os.getenv('IMG_ICO')))

        self.layout = QVBoxLayout()

        # Layout horizontal para los botones alineados a la derecha
        button_layout = QVBoxLayout()

        # Espaciador a la izquierda para empujar los botones a la derecha
        button_layout.setAlignment(Qt.AlignRight)  # Alineación a la derecha

        # Botón para reservar
        self.btn_reservar = QPushButton("Reservar")
        self.btn_reservar.setStyleSheet("font-size: 16px;")
        self.btn_reservar.setFixedWidth(200)
        self.btn_reservar.setFixedHeight(45)
        self.btn_reservar.clicked.connect(self.show_reserva)
        button_layout.addWidget(self.btn_reservar)

        # Botón para buscar
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.setStyleSheet("font-size: 16px;")
        self.btn_buscar.setFixedWidth(200)
        self.btn_buscar.setFixedHeight(45)
        self.btn_buscar.clicked.connect(self.show_buscar)
        button_layout.addWidget(self.btn_buscar)

        # Botón para destinos
        self.btn_destinos = QPushButton("Destinos")
        self.btn_destinos.setStyleSheet("font-size: 16px;")
        self.btn_destinos.setFixedWidth(200)
        self.btn_destinos.setFixedHeight(45)
        self.btn_destinos.clicked.connect(self.show_destinos)
        button_layout.addWidget(self.btn_destinos)

        # Botón para reportes
        self.btn_reportes = QPushButton("Reportes")
        self.btn_reportes.setStyleSheet("font-size: 16px;")
        self.btn_reportes.setFixedWidth(200)
        self.btn_reportes.setFixedHeight(45)
        self.btn_reportes.clicked.connect(self.show_reportes)
        button_layout.addWidget(self.btn_reportes)

        # Agregar el layout de botones al layout principal
        self.layout.addLayout(button_layout)

        # Establecer el layout principal
        self.setLayout(self.layout)

    def show_reserva(self):
        # Lógica para abrir la pantalla de reserva
        from app.ui.WindowReservar import ReservaScreen  # Importar aquí para evitar problemas de importación circular
        self.reserve_screen = ReservaScreen()
        self.reserve_screen.show()
        self.hide()  # Ocultar la ventana principal

    def show_buscar(self):
        # Lógica para abrir la pantalla de búsqueda
        from app.ui.windowBuscar import BuscarReservaScreen  # Importar aquí para evitar problemas de importación circular
        self.buscar_screen = BuscarReservaScreen()
        self.buscar_screen.show()
        self.hide()  # Ocultar la ventana principal

    def show_destinos(self):
        # Lógica para abrir la pantalla de destinos
        from app.ui.WindowDestinos import DestinosScreen  # Asegúrate de que esta clase existe
        self.destinos_screen = DestinosScreen()
        self.destinos_screen.show()
        self.hide()  # Ocultar la ventana principal

    def show_reportes(self):
        # Lógica para abrir la pantalla de destinos
        from app.ui.WindowReportes import ReportePDFScreen  # Asegúrate de que esta clase existe
        self.reportes_screen = ReportePDFScreen()
        self.reportes_screen.show()
        self.hide()  # Ocultar la ventana principal

    def closeEvent(self, event):
        # Confirmar antes de cerrar la aplicación
        reply = QMessageBox.question(self, 'Cerrar', '¿Estás seguro de que quieres salir?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

