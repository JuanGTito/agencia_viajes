from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Agencia de Viajes')
        self.setGeometry(100, 100, 400, 300)

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

        self.setLayout(self.layout)

    def show_reserva(self):
        # Lógica para abrir la pantalla de reserva
        from app.ui.reserva_screen import ReservaScreen  # Importar aquí para evitar problemas de importación circular
        self.reserve_screen = ReservaScreen()
        self.reserve_screen.show()
        self.hide()  # Ocultar la ventana principal

    def show_buscar(self):
        # Lógica para abrir la pantalla de reserva
        from app.ui.buscar_reserva import BuscarReservaScreen  # Importar aquí para evitar problemas de importación circular
        self.buscar_screen = BuscarReservaScreen()
        self.buscar_screen.show()
        self.hide()  # Ocultar la ventana principal

    def closeEvent(self, event):
        # Confirmar antes de cerrar la aplicación
        reply = QMessageBox.question(self, 'Cerrar', '¿Estás seguro de que quieres salir?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
