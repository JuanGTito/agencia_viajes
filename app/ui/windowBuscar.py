from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import QDate, Qt
from app.models.reserva import Reserva
from app.ui.WindowPrincipal import VentanaPrincipal
import os

class BuscarReservaScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Buscar Reserva')
        self.setMinimumSize(600, 800)

        self.fondo_label = QLabel(self)
        self.fondo_label.setPixmap(QPixmap(os.getenv('IMG_FONDO')))
        self.fondo_label.setScaledContents(True)  # Escalar la imagen para ajustarse al QLabel
        self.fondo_label.resize(self.size())

        self.setWindowIcon(QIcon(os.getenv('IMG_ICO')))

        self.fontNegrita = QFont("Arial", 14, QFont.Bold)

        self.layout = QVBoxLayout()
        self.reserva = Reserva()  # Crear una instancia de la clase Reserva

        # Inicialización de campos de búsqueda
        self.inicializar_campos()

        # Botón para buscar la reserva
        self.layout.addWidget(self.btn_buscar)

        # Botón para regresar a la pantalla principal
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setFixedHeight(30)
        self.btn_regresar.setFont(self.fontNegrita)
        self.btn_regresar.clicked.connect(self.regresar_a_principal)  # Conectar a la función de regreso
        
        # Contenedor horizontal para centrar el botón
        layout_centrado = QHBoxLayout()
        layout_centrado.addWidget(self.btn_regresar, alignment=Qt.AlignCenter)  # Agregar el botón con alineación centrada

        # Agregar el contenedor centrado al diseño principal
        self.layout.addLayout(layout_centrado)

        self.setLayout(self.layout)

    def inicializar_campos(self):
        """Método para inicializar todos los campos del formulario"""
        
        self.layout = QVBoxLayout()

        # Crear layout horizontal para el DNI o Pasaporte y el botón de búsqueda
        h_layout_dni = QHBoxLayout()

        # Campo de entrada para DNI o Pasaporte con placeholder
        self.input_dni_pasaporte = QLineEdit(self)
        self.input_dni_pasaporte.setFixedHeight(30)
        self.input_dni_pasaporte.setPlaceholderText("Ingrese DNI o Pasaporte")  # Placeholder text
        self.input_dni_pasaporte.setStyleSheet("QLineEdit { font-size: 14px; }")

        # Crear el botón de búsqueda y agregarlo a la derecha del campo
        self.btn_buscar = QPushButton("Buscar Reserva")
        self.btn_buscar.setFont(self.fontNegrita)
        self.btn_buscar.clicked.connect(self.buscar_reserva)

        # Añadir el campo de entrada y el botón al layout horizontal
        h_layout_dni.addWidget(self.input_dni_pasaporte)
        h_layout_dni.addWidget(self.btn_buscar)

        # Añadir el layout horizontal de DNI y el botón al layout principal
        self.layout.addLayout(h_layout_dni)

        self.label_nombre = QLabel("Nombre:")
        self.label_nombre.setFont(self.fontNegrita)
        self.input_nombre = QLineEdit(self)
        self.input_nombre.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_nombre.setReadOnly(True)
        self.input_nombre.setFixedHeight(30)
        self.layout.addWidget(self.label_nombre, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.input_nombre, alignment=Qt.AlignLeft)

        self.label_telefono = QLabel("Teléfono:")
        self.label_telefono.setFont(self.fontNegrita)
        self.input_telefono = QLineEdit(self)
        self.input_telefono.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_telefono.setReadOnly(True)  # Solo lectura
        self.input_telefono.setFixedHeight(30)
        self.layout.addWidget(self.label_telefono, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.input_telefono, alignment=Qt.AlignLeft)

        self.label_destino = QLabel("Destino:")
        self.label_destino.setFont(self.fontNegrita)
        self.input_destino = QLineEdit(self)
        self.input_destino.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_destino.setReadOnly(True)  # Solo lectura
        self.input_destino.setFixedHeight(30)
        self.layout.addWidget(self.label_destino, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.input_destino, alignment=Qt.AlignLeft)

        self.label_nacionalidad = QLabel("Nacionalidad:")
        self.label_nacionalidad.setFont(self.fontNegrita)
        self.input_nacionalidad = QLineEdit(self)
        self.input_nacionalidad.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_nacionalidad.setReadOnly(True)  # Solo lectura
        self.input_nacionalidad.setFixedHeight(30)
        self.layout.addWidget(self.label_nacionalidad, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.input_nacionalidad, alignment=Qt.AlignLeft)

        self.label_email = QLabel("Email:")
        self.label_email.setFont(self.fontNegrita)
        self.input_email = QLineEdit(self)
        self.input_email.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_email.setReadOnly(True)  # Solo lectura
        self.input_email.setFixedHeight(30)
        self.layout.addWidget(self.label_email, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.input_email, alignment=Qt.AlignLeft)

        self.label_paquete = QLabel("Tipo de Paquete:")
        self.label_paquete.setFont(self.fontNegrita)
        self.input_paquete = QLineEdit(self)
        self.input_paquete.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_paquete.setReadOnly(True)  # Solo lectura
        self.input_paquete.setFixedHeight(30)
        self.layout.addWidget(self.label_paquete, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.input_paquete, alignment=Qt.AlignLeft)

        self.label_monto_total = QLabel("Monto Total:")
        self.label_monto_total.setFont(self.fontNegrita)
        self.input_monto_total = QLineEdit(self)
        self.input_monto_total.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_monto_total.setReadOnly(True)  # Solo lectura
        self.input_monto_total.setFixedHeight(30)
        self.layout.addWidget(self.label_monto_total, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.input_monto_total, alignment=Qt.AlignLeft)

        self.label_fecha_reserva = QLabel("Fecha de Reserva:")
        self.label_fecha_reserva.setFont(self.fontNegrita)
        self.input_fecha_reserva = QLineEdit(self)
        self.input_fecha_reserva.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_fecha_reserva.setReadOnly(True)  # Solo lectura
        self.input_fecha_reserva.setFixedHeight(30)
        self.layout.addWidget(self.label_fecha_reserva, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.input_fecha_reserva, alignment=Qt.AlignLeft)

        self.label_fecha_salida = QLabel("Fecha de Salida:")
        self.label_fecha_salida.setFont(self.fontNegrita)
        self.input_fecha_salida = QLineEdit(self)
        self.input_fecha_salida.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_fecha_salida.setReadOnly(True)  # Solo lectura
        self.input_fecha_salida.setFixedHeight(30)
        self.layout.addWidget(self.label_fecha_salida, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.input_fecha_salida, alignment=Qt.AlignLeft)

        self.label_duracion_dias = QLabel("Duración (Días):")
        self.label_duracion_dias.setFont(self.fontNegrita)
        self.input_duracion_dias = QLineEdit(self)
        self.input_duracion_dias.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_duracion_dias.setReadOnly(True)  # Solo lectura
        self.input_duracion_dias.setFixedHeight(30)
        self.layout.addWidget(self.label_duracion_dias, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.input_duracion_dias, alignment=Qt.AlignLeft)

        self.label_metodo_pago = QLabel("Método de Pago:")
        self.label_metodo_pago.setFont(self.fontNegrita)
        self.input_metodo_pago = QLineEdit(self)
        self.input_metodo_pago.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_metodo_pago.setReadOnly(True)  # Solo lectura
        self.input_metodo_pago.setFixedHeight(30)
        self.layout.addWidget(self.label_metodo_pago, alignment=Qt.AlignLeft)
        self.layout.addWidget(self.input_metodo_pago, alignment=Qt.AlignLeft)

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

            f_reserva = reserva['f_reserva'].strftime('%d-%m-%Y') if reserva['f_reserva'] else "No disponible"
            f_salida = reserva['f_salida'].strftime('%d-%m-%Y') if reserva['f_salida'] else "No disponible"

            self.input_nombre.setText(reserva['nombre'])
            self.input_telefono.setText(reserva['telefono'])
            self.input_destino.setText(reserva['destino'])
            self.input_nacionalidad.setText(reserva['nacionalidad'])
            self.input_email.setText(reserva['email'])
            self.input_paquete.setText(reserva['tipo_paquete'])
            self.input_monto_total.setText(str(reserva['monto_total']))
            self.input_fecha_reserva.setText(f_reserva)
            self.input_fecha_salida.setText(f_salida)
            self.input_duracion_dias.setText(str(reserva['duracion_dias']))
            self.input_metodo_pago.setText(reserva['metodo'])
        else:
            QMessageBox.warning(self, "No encontrado", "No se encontró ninguna reserva con ese DNI o pasaporte.")

    def regresar_a_principal(self):
        self.close()
        self.pantalla_principal = VentanaPrincipal()
        self.pantalla_principal.show()
