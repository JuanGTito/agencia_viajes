from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from app.models.reserva import Reserva
from app.ui.WindowPrincipal import VentanaPrincipal

class BuscarReservaScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Buscar Reserva')
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()
        self.reserva = Reserva()  # Crear una instancia de la clase Reserva

        # Inicialización de campos de búsqueda
        self.inicializar_campos()

        # Botón para buscar la reserva
        self.layout.addWidget(self.btn_buscar)

        # Botón para regresar a la pantalla principal
        self.btn_regresar = QPushButton("Regresar a la Pantalla Principal")
        self.btn_regresar.clicked.connect(self.regresar_a_principal)  # Conectar a la función de regreso
        self.layout.addWidget(self.btn_regresar)

        self.setLayout(self.layout)

    def inicializar_campos(self):
        """Método para inicializar todos los campos del formulario"""

        # Crear un layout horizontal para el DNI y el botón de búsqueda
        h_layout = QHBoxLayout()

        self.label_dni_pasaporte = QLabel("Ingrese DNI o Pasaporte:")
        self.input_dni_pasaporte = QLineEdit(self)

        self.btn_buscar = QPushButton("Buscar Reserva")
        self.btn_buscar.clicked.connect(self.buscar_reserva)

        h_layout.addWidget(self.label_dni_pasaporte)
        h_layout.addWidget(self.input_dni_pasaporte)
        h_layout.addWidget(self.btn_buscar)

        self.layout.addLayout(h_layout)

        self.label_nombre = QLabel("Nombre:")
        self.input_nombre = QLineEdit(self)
        self.input_nombre.setReadOnly(True)  # Solo lectura
        self.layout.addWidget(self.label_nombre)
        self.layout.addWidget(self.input_nombre)

        self.label_telefono = QLabel("Teléfono:")
        self.input_telefono = QLineEdit(self)
        self.input_telefono.setReadOnly(True)  # Solo lectura
        self.layout.addWidget(self.label_telefono)
        self.layout.addWidget(self.input_telefono)

        self.label_destino = QLabel("Destino:")
        self.input_destino = QLineEdit(self)
        self.input_destino.setReadOnly(True)  # Solo lectura
        self.layout.addWidget(self.label_destino)
        self.layout.addWidget(self.input_destino)

        self.label_nacionalidad = QLabel("Nacionalidad:")
        self.input_nacionalidad = QLineEdit(self)
        self.input_nacionalidad.setReadOnly(True)  # Solo lectura
        self.layout.addWidget(self.label_nacionalidad)
        self.layout.addWidget(self.input_nacionalidad)

    def buscar_reserva(self):
        """Buscar reserva en la base de datos"""
        dni_pasaporte = self.input_dni_pasaporte.text()

        # Validar que el campo no esté vacío
        if not dni_pasaporte:
            QMessageBox.warning(self, "Campo vacío", "Por favor, ingresa un DNI o pasaporte.")
            return

        # Intentar obtener la reserva
        reserva = self.reserva.obtener_reserva(dni_pasaporte)

        if reserva:
            self.input_nombre.setText(reserva['nombre'])
            self.input_telefono.setText(reserva['telefono'])
            self.input_destino.setText(reserva['destino'])
            self.input_nacionalidad.setText(reserva['nacionalidad'])
        else:
            QMessageBox.warning(self, "No encontrado", "No se encontró ninguna reserva con ese DNI o pasaporte.")

    def regresar_a_principal(self):
        self.close()
        self.pantalla_principal = VentanaPrincipal()
        self.pantalla_principal.show()

