from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit, QStackedWidget
from app.models.reserva import Reserva
from PyQt5.QtCore import QDate

class ReservaScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Formulario de Reserva')
        self.setGeometry(100, 100, 400, 600)

        self.reserva = Reserva()
        
        # StackedWidget para manejar las diferentes pantallas de formulario
        self.stacked_widget = QStackedWidget()

        # Crear secciones
        self.crear_informacion_personal()
        self.crear_detalle_destino()
        self.crear_reserva_pago()

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def crear_informacion_personal(self):
        """Primera sección: Información Personal"""
        layout = QVBoxLayout()

        self.label_tipo_doc = QLabel("Tipo de Documentación:")
        self.input_tipo_doc = QComboBox()
        self.input_tipo_doc.addItems(["DNI", "Pasaporte"])
        layout.addWidget(self.label_tipo_doc)
        layout.addWidget(self.input_tipo_doc)

        self.label_num_doc = QLabel("Número de Documento:")
        self.input_num_doc = QLineEdit()
        layout.addWidget(self.label_num_doc)
        layout.addWidget(self.input_num_doc)

        self.label_nombre = QLabel("Nombre Completo:")
        self.input_nombre = QLineEdit()
        layout.addWidget(self.label_nombre)
        layout.addWidget(self.input_nombre)

        self.label_apellido = QLabel("Apellido:")
        self.input_apellido = QLineEdit()
        layout.addWidget(self.label_apellido)
        layout.addWidget(self.input_apellido)

        self.label_fecha_nacimiento = QLabel("Fecha de Nacimiento:")
        self.input_fecha_nacimiento = QDateEdit()
        self.input_fecha_nacimiento.setCalendarPopup(True)
        layout.addWidget(self.label_fecha_nacimiento)
        layout.addWidget(self.input_fecha_nacimiento)

        self.label_genero = QLabel("Género:")
        self.input_genero = QComboBox()
        self.input_genero.addItems(["Masculino", "Femenino"])
        layout.addWidget(self.label_genero)
        layout.addWidget(self.input_genero)

        self.label_nacionalidad = QLabel("Nacionalidad:")
        self.input_nacionalidad = QLineEdit()
        layout.addWidget(self.label_nacionalidad)
        layout.addWidget(self.input_nacionalidad)

        self.label_telefono = QLabel("Número de Teléfono:")
        self.input_telefono = QLineEdit()
        layout.addWidget(self.label_telefono)
        layout.addWidget(self.input_telefono)

        self.label_email = QLabel("Correo Electrónico:")
        self.input_email = QLineEdit()
        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)

        # Botón para pasar a la siguiente sección
        self.btn_siguiente = QPushButton("Siguiente")
        self.btn_siguiente.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(self.btn_siguiente)

        # Crear widget y agregar layout
        personal_widget = QWidget()
        personal_widget.setLayout(layout)
        self.stacked_widget.addWidget(personal_widget)

    def crear_detalle_destino(self):
        """Segunda sección: Detalle del Destino"""
        layout = QVBoxLayout()

        destinos = self.reserva.obtener_destinos()

        self.label_destino = QLabel("Destino:")
        self.input_destino = QComboBox()
        for id_paquete, (id_cat_destino, tipo_paquete, hotel, precio_diario) in destinos.items():
            self.input_destino.addItem(f"{id_cat_destino} - Precio: {tipo_paquete} {hotel} {precio_diario}", id_paquete)
        layout.addWidget(self.label_destino)
        layout.addWidget(self.input_destino)

        # Selección de Paquete Turístico
        self.label_paquete = QLabel("Tipo de Paquete:")
        self.input_paquete = QComboBox()
        self.input_paquete.addItems(["Individual", "Familiar"])
        layout.addWidget(self.label_paquete)
        layout.addWidget(self.input_paquete)

        # Botones para regresar y avanzar
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(self.btn_regresar)

        self.btn_siguiente_destino = QPushButton("Siguiente")
        self.btn_siguiente_destino.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(self.btn_siguiente_destino)

        # Crear widget y agregar layout
        destino_widget = QWidget()
        destino_widget.setLayout(layout)
        self.stacked_widget.addWidget(destino_widget)

    def crear_reserva_pago(self):
        """Tercera sección: Reserva y Pago"""
        layout = QVBoxLayout()

        self.label_fecha_salida = QLabel("Fecha de Salida:")
        self.input_fecha_salida = QDateEdit()
        self.input_fecha_salida.setMinimumDate(QDate.currentDate())
        layout.addWidget(self.label_fecha_salida)
        layout.addWidget(self.input_fecha_salida)

        self.label_fecha_regreso = QLabel("Fecha de Regreso:")
        self.input_fecha_regreso = QDateEdit()
        self.input_fecha_regreso.setMinimumDate(QDate.currentDate())
        layout.addWidget(self.label_fecha_regreso)
        layout.addWidget(self.input_fecha_regreso)

        self.label_metodo_pago = QLabel("Método de Pago:")
        self.input_metodo_pago = QComboBox()
        self.input_metodo_pago.addItems(["Transferencia", "Efectivo"])
        layout.addWidget(self.label_metodo_pago)
        layout.addWidget(self.input_metodo_pago)

        self.label_referencia = QLabel("Número de Referencia (si aplica):")
        self.input_referencia = QLineEdit()
        layout.addWidget(self.label_referencia)
        layout.addWidget(self.input_referencia)

        # Botones para regresar y enviar
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(self.btn_regresar)

        self.btn_enviar = QPushButton("Enviar Reserva")
        self.btn_enviar.clicked.connect(self.enviar_reserva)
        layout.addWidget(self.btn_enviar)

        # Crear widget y agregar layout
        reserva_widget = QWidget()
        reserva_widget.setLayout(layout)
        self.stacked_widget.addWidget(reserva_widget)

    def validar_fechas(self):
        """Valida que la fecha de salida sea anterior a la de regreso."""
        if self.input_fecha_salida.date() > self.input_fecha_regreso.date():
            QMessageBox.warning(self, "Fecha incorrecta", "La fecha de regreso debe ser posterior a la fecha de salida.")
            return False
        return True

    def enviar_reserva(self):
        """Obtiene los datos y guarda la reserva"""
        # Recoge los datos y verifica si se llenaron
        tipo_doc = self.input_tipo_doc.currentText()
        num_doc = self.input_num_doc.text()
        nombre = self.input_nombre.text()
        apellido = self.input_apellido.text()
        fecha_nacimiento = self.input_fecha_nacimiento.date().toString("yyyy-MM-dd")
        genero = self.input_genero.currentText()
        telefono = self.input_telefono.text()
        email = self.input_email.text()
        nacionalidad = self.input_nacionalidad.text()
        destino_id = self.input_destino.currentData()
        fecha_salida = self.input_fecha_salida.date().toString("yyyy-MM-dd")
        fecha_regreso = self.input_fecha_regreso.date().toString("yyyy-MM-dd")
        metodo_pago = self.input_metodo_pago.currentText()
        referencia = self.input_referencia.text() if metodo_pago == "Transferencia" else None

        if not all([tipo_doc, num_doc, nombre, apellido, fecha_nacimiento, telefono, email, nacionalidad,
                    destino_id, fecha_salida, fecha_regreso, metodo_pago]):
            QMessageBox.warning(self, "Campos incompletos", "Por favor, completa todos los campos obligatorios.")
            return

        # Validar fechas antes de guardar
        if not self.validar_fechas():
            return

        # Guardar la reserva
        if self.reserva.guardar_reserva(tipo_doc, num_doc, nombre, apellido, fecha_nacimiento, genero, telefono, email,
                                        nacionalidad, destino_id, fecha_salida, fecha_regreso, metodo_pago, referencia):
            QMessageBox.information(self, "Reserva Enviada", "Tu reserva ha sido enviada con éxito.")
            self.close()
        else:
            QMessageBox.warning(self, "Error de Conexión", "No se pudo conectar a la base de datos.")
