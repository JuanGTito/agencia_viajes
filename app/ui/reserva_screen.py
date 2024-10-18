from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox
from app.models.reserva import Reserva
from app.ui.ventana_principal import VentanaPrincipal

class ReservaScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Formulario de Reserva')
        self.setGeometry(100, 100, 400, 500)

        self.layout = QVBoxLayout()
        self.reserva = Reserva()  # Crear una instancia de la clase Reserva

        # Inicialización de campos de entrada
        self.inicializar_campos()

        # Botón para enviar reserva
        self.btn_enviar = QPushButton("Enviar Reserva")
        self.btn_enviar.clicked.connect(self.enviar_reserva)
        self.layout.addWidget(self.btn_enviar)

        # Botón para regresar a la pantalla principal
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(self.regresar_a_pantalla_principal)
        self.layout.addWidget(self.btn_regresar)

        self.setLayout(self.layout)

    def inicializar_campos(self):
        """Método para inicializar todos los campos del formulario"""
        self.label_nombre = QLabel("Nombre Completo:")
        self.input_nombre = QLineEdit(self)
        self.layout.addWidget(self.label_nombre)
        self.layout.addWidget(self.input_nombre)

        self.label_fecha_nacimiento = QLabel("Fecha de Nacimiento:")
        self.input_fecha_nacimiento = QLineEdit(self)
        self.layout.addWidget(self.label_fecha_nacimiento)
        self.layout.addWidget(self.input_fecha_nacimiento)

        self.label_genero = QLabel("Género:")
        self.input_genero = QComboBox(self)
        self.input_genero.addItems(["Masculino", "Femenino", "Otro"])
        self.layout.addWidget(self.label_genero)
        self.layout.addWidget(self.input_genero)

        self.label_telefono = QLabel("Número de Teléfono:")
        self.input_telefono = QLineEdit(self)
        self.layout.addWidget(self.label_telefono)
        self.layout.addWidget(self.input_telefono)

        self.label_email = QLabel("Correo Electrónico:")
        self.input_email = QLineEdit(self)
        self.layout.addWidget(self.label_email)
        self.layout.addWidget(self.input_email)

        self.label_pasaporte = QLabel("Número de Pasaporte:")
        self.input_pasaporte = QLineEdit(self)
        self.layout.addWidget(self.label_pasaporte)
        self.layout.addWidget(self.input_pasaporte)

        self.label_nacionalidad = QLabel("Nacionalidad:")
        self.input_nacionalidad = QLineEdit(self)
        self.layout.addWidget(self.label_nacionalidad)
        self.layout.addWidget(self.input_nacionalidad)

        self.label_destino = QLabel("Destino:")
        self.input_destino = QComboBox(self)

        # Cargar los destinos desde la clase Reserva
        self.input_destino.addItems(self.reserva.destinos.keys())
        self.layout.addWidget(self.label_destino)
        self.layout.addWidget(self.input_destino)

        self.label_fecha_salida = QLabel("Fecha de Salida:")
        self.input_fecha_salida = QLineEdit(self)
        self.layout.addWidget(self.label_fecha_salida)
        self.layout.addWidget(self.input_fecha_salida)

        self.label_fecha_regreso = QLabel("Fecha de Regreso:")
        self.input_fecha_regreso = QLineEdit(self)
        self.layout.addWidget(self.label_fecha_regreso)
        self.layout.addWidget(self.input_fecha_regreso)

        self.label_metodo_pago = QLabel("Método de Pago:")
        self.input_metodo_pago = QComboBox(self)
        self.input_metodo_pago.addItems(["Transferencia", "Pago en efectivo"])
        self.layout.addWidget(self.label_metodo_pago)
        self.layout.addWidget(self.input_metodo_pago)

        self.label_referencia = QLabel("Número de Referencia (si aplica):")
        self.input_referencia = QLineEdit(self)
        self.layout.addWidget(self.label_referencia)
        self.layout.addWidget(self.input_referencia)

    def regresar_a_pantalla_principal(self):
        """Cerrar la ventana actual y regresar a la pantalla principal"""
        self.close()
        self.pantalla_principal = VentanaPrincipal()
        self.pantalla_principal.show()

    def enviar_reserva(self):
        """Obtener los datos del formulario y guardar la reserva"""
        # Obtener los datos ingresados
        nombre = self.input_nombre.text()
        fecha_nacimiento = self.input_fecha_nacimiento.text()
        genero = self.input_genero.currentText()
        telefono = self.input_telefono.text()
        email = self.input_email.text()
        pasaporte = self.input_pasaporte.text()
        nacionalidad = self.input_nacionalidad.text()
        destino = self.input_destino.currentText()  # Usar el destino seleccionado
        fecha_salida = self.input_fecha_salida.text()
        fecha_regreso = self.input_fecha_regreso.text()
        metodo_pago = self.input_metodo_pago.currentText()
        referencia = self.input_referencia.text()

        # Validar que todos los campos obligatorios estén completos
        if not all([nombre, fecha_nacimiento, telefono, email, pasaporte, nacionalidad, destino, fecha_salida, fecha_regreso, metodo_pago]):
            QMessageBox.warning(self, "Campos incompletos", "Por favor, completa todos los campos obligatorios.")
            return

        # Intentar guardar la reserva
        if self.reserva.guardar_reserva(nombre, fecha_nacimiento, genero, telefono, email, pasaporte, nacionalidad,
                                        destino, fecha_salida, fecha_regreso, metodo_pago, referencia):
            QMessageBox.information(self, "Reserva Enviada", "Tu reserva ha sido enviada con éxito.")
            self.regresar_a_pantalla_principal()
        else:
            QMessageBox.warning(self, "Error de Conexión", "No se pudo conectar a la base de datos.")
