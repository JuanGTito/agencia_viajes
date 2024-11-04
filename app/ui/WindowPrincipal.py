from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QLabel

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Agencia de Viajes')
        self.setGeometry(100, 100, 400, 300)

        self.fondo_label = QLabel(self)
        self.fondo_label.setPixmap(QPixmap('app/resources/images/fondo.jpg'))
        self.fondo_label.setScaledContents(True)  # Escalar la imagen para ajustarse al QLabel
        self.fondo_label.resize(self.size())

        self.setWindowIcon(QIcon('app/resources/images/icon.ico'))  # Ruta al ícono

        # Layout principal
        self.layout = QVBoxLayout()

        # Botón para reservar
        self.btn_reservar = QPushButton("Reservar")
        self.btn_reservar.clicked.connect(self.show_reserva)
        self.layout.addWidget(self.btn_reservar)

        # Botón para buscar
        self.btn_buscar = QPushButton("Buscar")
        self.btn_buscar.clicked.connect(self.show_buscar)
        self.layout.addWidget(self.btn_buscar)

        # Botón para destinos
        self.btn_destinos = QPushButton("Destinos")
        self.btn_destinos.clicked.connect(self.show_destinos)
        self.layout.addWidget(self.btn_destinos)

        self.btn_destinos = QPushButton("Reportes")
        self.btn_destinos.clicked.connect(self.show_destinos)
        self.layout.addWidget(self.btn_destinos)

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
        from app.ui.WindowReportes import ReportesScreen  # Asegúrate de que esta clase existe
        self.reportes_screen = ReportesScreen()
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

