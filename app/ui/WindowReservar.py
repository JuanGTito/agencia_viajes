from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit
from app.models.reserva import Reserva
from app.ui.WindowPrincipal import VentanaPrincipal

class ReservaScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Formulario de Reserva')
        self.setGeometry(100, 100, 400, 600)

        self.layout = QVBoxLayout()
        self.reserva = Reserva()

        self.inicializar_campos()

        self.btn_enviar = QPushButton("Enviar Reserva")
        self.btn_enviar.clicked.connect(self.enviar_reserva)
        self.layout.addWidget(self.btn_enviar)

        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(self.regresar_a_pantalla_principal)
        self.layout.addWidget(self.btn_regresar)

        self.setLayout(self.layout)

    def inicializar_campos(self):
        """Método para inicializar todos los campos del formulario"""
        self.label_tipo_doc = QLabel("Tipo de Documentación:")
        self.input_tipo_doc = QComboBox(self)
        self.input_tipo_doc.addItems(["DNI", "Pasaporte"])
        self.layout.addWidget(self.label_tipo_doc)
        self.layout.addWidget(self.input_tipo_doc)

        self.label_num_doc = QLabel("Número de Documento:")
        self.input_num_doc = QLineEdit(self)
        self.layout.addWidget(self.label_num_doc)
        self.layout.addWidget(self.input_num_doc)

        self.label_nombre = QLabel("Nombre Completo:")
        self.input_nombre = QLineEdit(self)
        self.layout.addWidget(self.label_nombre)
        self.layout.addWidget(self.input_nombre)

        self.label_apellido = QLabel("Apellido:")
        self.input_apellido = QLineEdit(self)
        self.layout.addWidget(self.label_apellido)
        self.layout.addWidget(self.input_apellido)

        self.label_fecha_nacimiento = QLabel("Fecha de Nacimiento:")
        self.input_fecha_nacimiento = QDateEdit(self)
        self.layout.addWidget(self.label_fecha_nacimiento)
        self.layout.addWidget(self.input_fecha_nacimiento)

        self.label_genero = QLabel("Género:")
        self.input_genero = QComboBox(self)
        self.input_genero.addItems(["Masculino", "Femenino"])
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

        self.label_nacionalidad = QLabel("Nacionalidad:")
        self.input_nacionalidad = QLineEdit(self)
        self.layout.addWidget(self.label_nacionalidad)
        self.layout.addWidget(self.input_nacionalidad)

        # Obtener destinos y almacenarlos
        destinos = self.reserva.obtener_destinos()
        print(destinos) 

        self.label_destino = QLabel("Destino:")
        self.input_destino = QComboBox(self)

        # Agregar cada destino al ComboBox con su ID
        for id_destino, (nombre, precio) in destinos.items():
            self.input_destino.addItem(nombre, id_destino)  # Agregar el nombre y establecer el ID como dato

        self.layout.addWidget(self.label_destino)
        self.layout.addWidget(self.input_destino)        

        self.label_fecha_salida = QLabel("Fecha de Salida:")
        self.input_fecha_salida = QDateEdit(self)
        self.layout.addWidget(self.label_fecha_salida)
        self.layout.addWidget(self.input_fecha_salida)

        self.label_fecha_regreso = QLabel("Fecha de Regreso:")
        self.input_fecha_regreso = QDateEdit(self)
        self.layout.addWidget(self.label_fecha_regreso)
        self.layout.addWidget(self.input_fecha_regreso)

        self.label_metodo_pago = QLabel("Método de Pago:")
        self.input_metodo_pago = QComboBox(self)
        self.input_metodo_pago.addItems(["Transferencia", "Efectivo"])
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
        tipo_doc = self.input_tipo_doc.currentText()
        num_doc = self.input_num_doc.text()
        nombre = self.input_nombre.text()
        apellido = self.input_apellido.text()
        fecha_nacimiento = self.input_fecha_nacimiento.date().toString("yyyy-MM-dd") 
        genero = self.input_genero.currentText()
        telefono = self.input_telefono.text()
        email = self.input_email.text()
        nacionalidad = self.input_nacionalidad.text()
        destino = self.input_destino.currentText()
        fecha_salida = self.input_fecha_salida.date().toString("yyyy-MM-dd")
        fecha_regreso = self.input_fecha_regreso.date().toString("yyyy-MM-dd")
        metodo_pago = self.input_metodo_pago.currentText()

        referencia = self.input_referencia.text() if metodo_pago == "Transferencia" else None

        if not all([tipo_doc, num_doc, nombre, apellido, fecha_nacimiento, telefono, email, nacionalidad,
                    destino, fecha_salida, fecha_regreso, metodo_pago]):
            QMessageBox.warning(self, "Campos incompletos", "Por favor, completa todos los campos obligatorios.")
            return

        if self.reserva.guardar_reserva(tipo_doc, num_doc, nombre, apellido, fecha_nacimiento, genero, telefono, email,
                                         nacionalidad, destino, fecha_salida, fecha_regreso,
                                         metodo_pago, referencia):
            QMessageBox.information(self, "Reserva Enviada", "Tu reserva ha sido enviada con éxito.")
            self.regresar_a_pantalla_principal()
        else:
            QMessageBox.warning(self, "Error de Conexión", "No se pudo conectar a la base de datos.")

