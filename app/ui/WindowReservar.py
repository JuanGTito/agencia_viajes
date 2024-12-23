from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit, QStackedWidget, QDateEdit, QSpinBox
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import QDate, Qt
import os
from app.models.reserva import Reserva
from app.ui.WindowPrincipal import VentanaPrincipal
from app.ui.WindowImpresion import VentanaImpresion
from app.services.database import crear_conexion

class ReservaScreen(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle('Formulario de Reserva')
        self.setFixedSize(700, 750)
        
        self.usuario = usuario

        self.fondo_label = QLabel(self)
        self.fondo_label.setPixmap(QPixmap(os.getenv('IMG_FONDO')))
        self.fondo_label.setScaledContents(True)  # Escalar la imagen para ajustarse al QLabel
        self.fondo_label.resize(self.size())

        self.setWindowIcon(QIcon(os.getenv('IMG_ICO')))

        self.fontNegrita = QFont("Arial", 14, QFont.Bold)

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
        self.label_tipo_doc.setFont(self.fontNegrita)
        self.input_tipo_doc = QComboBox()
        self.input_tipo_doc.addItems(["DNI", "Pasaporte"])
        self.input_tipo_doc.setStyleSheet(""" QComboBox { font-size: 14px; } QComboBox QAbstractItemView { font-size: 14px; } """)
        self.input_tipo_doc.setFixedHeight(30)
        layout.addWidget(self.label_tipo_doc, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_tipo_doc, alignment=Qt.AlignLeft)

        self.label_num_doc = QLabel("Número de Documento:")
        self.label_num_doc.setFont(self.fontNegrita)
        self.input_num_doc = QLineEdit()
        self.input_num_doc.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_num_doc.setFixedHeight(30)
        layout.addWidget(self.label_num_doc, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_num_doc, alignment=Qt.AlignLeft)

        self.label_nombre = QLabel("Nombre Completo:")
        self.label_nombre.setFont(self.fontNegrita)
        self.input_nombre = QLineEdit()
        self.input_nombre.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_nombre.setFixedHeight(30)
        layout.addWidget(self.label_nombre, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_nombre, alignment=Qt.AlignLeft)

        self.label_apellido = QLabel("Apellido:")
        self.label_apellido.setFont(self.fontNegrita)
        self.input_apellido = QLineEdit()
        self.input_apellido.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_apellido.setFixedHeight(30)
        layout.addWidget(self.label_apellido, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_apellido, alignment=Qt.AlignLeft)

        self.label_fecha_nacimiento = QLabel("Fecha de Nacimiento:")
        self.label_fecha_nacimiento.setFont(self.fontNegrita)
        self.input_fecha_nacimiento = QDateEdit()
        self.input_fecha_nacimiento.setCalendarPopup(True)
        self.input_fecha_nacimiento.setFixedHeight(30)
        self.input_fecha_nacimiento.setStyleSheet(""" QDateEdit { font-size: 14px; } QDateEdit QAbstractItemView { font-size: 14px; } """)
        layout.addWidget(self.label_fecha_nacimiento, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_fecha_nacimiento, alignment=Qt.AlignLeft)

        self.label_genero = QLabel("Género:")
        self.label_genero.setFont(self.fontNegrita)
        self.input_genero = QComboBox()
        self.input_genero.addItems(["Masculino", "Femenino"])
        self.input_genero.setFixedHeight(30)
        self.input_genero.setStyleSheet(""" QComboBox { font-size: 14px; } QComboBox QAbstractItemView { font-size: 14px; } """)
        layout.addWidget(self.label_genero, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_genero, alignment=Qt.AlignLeft)

        self.label_nacionalidad = QLabel("Nacionalidad:")
        self.label_nacionalidad.setFont(self.fontNegrita)
        self.input_nacionalidad = QLineEdit()
        self.input_nacionalidad.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_nacionalidad.setFixedHeight(30)
        layout.addWidget(self.label_nacionalidad, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_nacionalidad, alignment=Qt.AlignLeft)

        self.label_telefono = QLabel("Número de Teléfono:")
        self.label_telefono.setFont(self.fontNegrita)
        self.input_telefono = QLineEdit()
        self.input_telefono.setFixedHeight(30)
        self.input_telefono.setStyleSheet("QLineEdit { font-size: 14px; }")
        layout.addWidget(self.label_telefono, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_telefono, alignment=Qt.AlignLeft)

        self.label_email = QLabel("Correo Electrónico:")
        self.label_email.setFont(self.fontNegrita)
        self.input_email = QLineEdit()
        self.input_email.setFixedHeight(30)
        self.input_email.setStyleSheet("QLineEdit { font-size: 14px; }")
        layout.addWidget(self.label_email, alignment=Qt.AlignLeft)
        layout.addWidget(self.input_email, alignment=Qt.AlignLeft)

        # Botón para pasar a la siguiente sección
        self.btn_siguiente = QPushButton("Siguiente")
        self.btn_siguiente.setFont(self.fontNegrita)
        self.btn_siguiente.setFixedSize(100, 35) 
        self.btn_siguiente.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        

        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setFont(self.fontNegrita)
        self.btn_regresar.setFixedSize(100, 35)
        self.btn_regresar.clicked.connect(self.regresar_a_principal)

        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(20)  # Espacio entre los botones
        botones_layout.addWidget(self.btn_regresar)
        botones_layout.addWidget(self.btn_siguiente)

        botones_layout.setAlignment(Qt.AlignCenter)

        layout.addLayout(botones_layout)

        # Crear widget y agregar layout
        personal_widget = QWidget()
        personal_widget.setLayout(layout)
        self.stacked_widget.addWidget(personal_widget)

    def crear_detalle_destino(self):
        layout = QVBoxLayout()

        # Obtener destinos y crear el combo
        destinos = self.reserva.obtener_destinos()

        self.label_destino = QLabel("Destino:")
        self.label_destino.setFont(self.fontNegrita)
        self.input_destino = QComboBox()

        # Agregar destinos al combo
        for id_destino, (destino, descripcion) in destinos.items():
            self.input_destino.addItem(f"{destino} - Descripción: {descripcion}", id_destino)
            
        self.input_destino.currentIndexChanged.connect(self.actualizar_campo_con_id_destino)
        self.input_destino.setStyleSheet(""" QComboBox { font-size: 14px; } QComboBox QAbstractItemView { font-size: 14px; } """)
        self.input_destino.setFixedHeight(30)

        layout.addWidget(self.label_destino)
        layout.addWidget(self.input_destino, alignment=Qt.AlignLeft)

        # Tipo de Paquete
        self.label_paquete = QLabel("Tipo de Paquete:")
        self.label_paquete.setFont(self.fontNegrita)
        self.input_paquete = QComboBox()
        self.input_paquete.setFixedHeight(30)
        self.input_paquete.setFixedWidth(270)
        self.input_paquete.setStyleSheet(""" QComboBox { font-size: 14px; } QComboBox QAbstractItemView { font-size: 14px; } """)
        layout.addWidget(self.label_paquete)
        layout.addWidget(self.input_paquete, alignment=Qt.AlignLeft)

        # Fecha de Salida
        self.label_fecha_salida = QLabel("Fecha de Salida:")
        self.label_fecha_salida.setFont(self.fontNegrita)
        self.input_fecha_salida = QDateEdit()
        self.input_fecha_salida.setMinimumDate(QDate.currentDate())
        self.input_fecha_salida.setFixedHeight(30)
        self.input_fecha_salida.setStyleSheet(""" QDateEdit { font-size: 14px; } QDateEdit QAbstractItemView { font-size: 14px; } """)
        layout.addWidget(self.label_fecha_salida)
        layout.addWidget(self.input_fecha_salida, alignment=Qt.AlignLeft)

        # Duración
        self.label_duracion = QLabel("Duración (días):")
        self.label_duracion.setFont(self.fontNegrita)
        self.input_duracion = QSpinBox()
        self.input_duracion.setMinimum(1)  # Mínimo 1 día
        self.input_duracion.setMaximum(365)  # Máximo 365 días (un año)
        self.input_duracion.textChanged.connect(self.calcular_precio_total)
        self.input_duracion.setFixedHeight(30)
        self.input_duracion.setStyleSheet(""" QSpinBox { font-size: 14px; } QSpinBox QAbstractItemView { font-size: 14px; } """)
        layout.addWidget(self.label_duracion)
        layout.addWidget(self.input_duracion, alignment=Qt.AlignLeft)

        # Fecha de Regreso
        self.label_fecha_regreso = QLabel("Fecha Llegada:")
        self.label_fecha_regreso.setFont(self.fontNegrita)
        self.input_fecha_regreso = QDateEdit()
        self.input_fecha_regreso.setReadOnly(True)  # Solo lectura
        self.input_fecha_regreso.setFixedHeight(30)
        self.input_fecha_regreso.setStyleSheet(""" QDateEdit { font-size: 14px; } QDateEdit QAbstractItemView { font-size: 14px; } """)
        layout.addWidget(self.label_fecha_regreso)
        layout.addWidget(self.input_fecha_regreso, alignment=Qt.AlignLeft)

        # Conexiones para calcular la fecha de regreso
        self.input_duracion.valueChanged.connect(self.actualizar_fecha_llegada)
        self.input_fecha_salida.dateChanged.connect(self.actualizar_fecha_llegada)

        # Botón "Siguiente"
        self.btn_siguiente_destino = QPushButton("Siguiente")
        self.btn_siguiente_destino.setFont(self.fontNegrita)
        self.btn_siguiente_destino.setFixedSize(100, 35) 
        self.btn_siguiente_destino.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))

        # Botón "Regresar"
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setFont(self.fontNegrita)
        self.btn_regresar.setFixedSize(100, 35)
        self.btn_regresar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

        # Layout para los botones
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(20)  # Espacio entre los botones
        botones_layout.addWidget(self.btn_regresar)
        botones_layout.addWidget(self.btn_siguiente_destino)

        # Centrar los botones
        botones_layout.setAlignment(Qt.AlignCenter)

        # Agregar los botones al layout principal
        layout.addLayout(botones_layout)

        # Crear el widget con el layout
        destino_widget = QWidget()
        destino_widget.setLayout(layout)

        # Agregar el widget a la pila (stacked_widget)
        self.stacked_widget.addWidget(destino_widget)

    def actualizar_fecha_llegada(self):
        # Obtener la fecha de salida y duración en días
        fecha_salida = self.input_fecha_salida.date()
        duracion = self.input_duracion.value()  # Duración en días

        if fecha_salida.isValid() and duracion > 0:
            # Sumar los días a la fecha de salida
            fecha_llegada = fecha_salida.addDays(duracion)
            self.input_fecha_regreso.setDate(fecha_llegada)

    def actualizar_campo_con_id_destino(self):
        id_destino_seleccionado = self.input_destino.currentData()
        print(f"ID del destino seleccionado: {id_destino_seleccionado}")

        self.input_paquete.clear()

        if id_destino_seleccionado is None:
            print("No se ha seleccionado un destino válido.")
            return

        # Obtener paquetes turísticos según el destino seleccionado
        paquetes = self.reserva.obtener_paquetes_por_destino(id_destino_seleccionado)

        if not paquetes:
            print("No se encontraron paquetes para el destino seleccionado.")
            return

        # Agregar los paquetes al ComboBox
        for id_paquete, tipo_paquete, hotel, precio_diario in paquetes:
            paquete_texto = f"{tipo_paquete} - Hotel: {hotel} - Precio Diario: {precio_diario} USD"
            self.input_paquete.addItem(paquete_texto, (id_paquete, hotel, precio_diario))

    def obtener_id_paquete(self):
        # Obtener el ID del paquete seleccionado en el ComboBox
        paquete_seleccionado = self.input_paquete.currentData()
        if paquete_seleccionado:
            try:
                # Intentar desempaquetar solo el primer valor
                id_paquete, *resto = paquete_seleccionado
                print(f"ID del paquete seleccionado: {id_paquete}")
                return id_paquete
            except ValueError:
                print("Paquete no válido: los datos no son correctos.")
                return None
        else:
            print("No se ha seleccionado un paquete válido.")
            return None 

    def obtener_precio_por_paquete(self, id_paquete):
        # Conectar con la base de datos y obtener el precio diario según el id_paquete
        conn = crear_conexion()
        precio_diario = None

        if conn:
            cursor = conn.cursor()
            try:
                # Realizar la consulta para obtener el precio según el id_paquete
                consulta = f"""
                    SELECT precio_diario
                    FROM paquete_turistico
                    WHERE id_paquete = {id_paquete}
                """
                cursor.execute(consulta)
                resultado = cursor.fetchone()

                if resultado:
                    precio_diario = resultado[0]
                    print(f"Precio diario obtenido para el paquete {id_paquete}: {precio_diario} USD")
                else:
                    print("No se encontró el paquete con el ID proporcionado.")

            except Exception as e:
                print(f"Error al obtener el precio del paquete: {e}")

            finally:
                cursor.close()
                conn.close()

        return precio_diario

    def calcular_precio_total(self):
        try:
            dias_estancia = self.input_duracion.value()
        except ValueError:
            self.input_total_a_pagar.setText("Días no válidos")
            return

        paquete_seleccionado = self.input_paquete.currentData()
        if paquete_seleccionado:
            try:
                # Desempaquetar los tres primeros valores
                id_paquete, hotel, tipo_paquete, *resto = paquete_seleccionado

                # Obtener el precio diario desde la base de datos usando el id_paquete
                precio_diario = self.obtener_precio_por_paquete(id_paquete)
                if precio_diario is not None:
                    total_a_pagar = dias_estancia * precio_diario
                    self.input_total_a_pagar.setText(f"{total_a_pagar} USD")
                else:
                    self.input_total_a_pagar.setText("No se pudo obtener el precio del paquete")
            except ValueError:
                self.input_total_a_pagar.setText("Paquete no válido")
        else:
            self.input_total_a_pagar.setText("Paquete no válido")
    
    def crear_reserva_pago(self):
        """Tercera sección: Reserva y Pago"""
        layout = QVBoxLayout()
    
        # Total a pagar
        self.label_total_a_pagar = QLabel("Total a Pagar:")
        self.label_total_a_pagar.setFont(self.fontNegrita)
        self.input_total_a_pagar = QLineEdit()
        self.input_total_a_pagar.setReadOnly(True)
        self.input_total_a_pagar.setFixedHeight(30)
        self.input_total_a_pagar.setStyleSheet("QLineEdit { font-size: 14px; }")
        layout.addWidget(self.label_total_a_pagar)
        layout.addWidget(self.input_total_a_pagar, alignment=Qt.AlignLeft)
    
        # Método de pago
        self.label_metodo_pago = QLabel("Método de Pago:")
        self.label_metodo_pago.setFont(self.fontNegrita)
        self.input_metodo_pago = QComboBox()
        self.input_metodo_pago.addItems(["Transferencia", "Efectivo"])
        self.input_metodo_pago.setFixedHeight(30)
        self.input_metodo_pago.setStyleSheet(""" QComboBox { font-size: 14px; } QComboBox QAbstractItemView { font-size: 14px; } """)
        layout.addWidget(self.label_metodo_pago)
        layout.addWidget(self.input_metodo_pago, alignment=Qt.AlignLeft)
    
        # Número de referencia
        self.label_referencia = QLabel("Número de Referencia (si aplica):")
        self.label_referencia.setFont(self.fontNegrita)
        self.input_referencia = QLineEdit()
        self.input_referencia.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_referencia.setFixedHeight(30)
        self.input_referencia.setStyleSheet("QLineEdit { font-size: 14px; }")
        layout.addWidget(self.label_referencia)
        layout.addWidget(self.input_referencia, alignment=Qt.AlignLeft)
    
        # Botones
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(20)  # Espacio entre los botones
    
        # Botón "Regresar"
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setFont(self.fontNegrita)
        self.btn_regresar.setFixedSize(100, 35)
        self.btn_regresar.setFixedWidth(180)
        self.btn_regresar.setFixedHeight(35)
        self.btn_regresar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        botones_layout.addWidget(self.btn_regresar)
    
        # Botón "Enviar Reserva"
        self.btn_enviar = QPushButton("Enviar Reserva")
        self.btn_enviar.setFont(self.fontNegrita)
        self.btn_enviar.setFixedSize(150, 35)
        self.btn_enviar.clicked.connect(self.enviar_reserva)
        self.btn_enviar.clicked.connect(self.regresar_a_principal)
        botones_layout.addWidget(self.btn_enviar)
    
        # Centrar los botones
        botones_layout.setAlignment(Qt.AlignCenter)
        layout.addLayout(botones_layout)
    
        # Crear el widget con el layout
        reserva_widget = QWidget()
        reserva_widget.setLayout(layout)
    
        # Agregar el widget a la pila (stacked_widget)
        self.stacked_widget.addWidget(reserva_widget)

    def validar_fechas(self):
        """Valida que la fecha de salida sea anterior a la de regreso."""
        if self.input_fecha_salida.date() > self.input_fecha_regreso.date():
            QMessageBox.warning(self, "Fecha incorrecta", "La fecha de regreso debe ser posterior a la fecha de salida.")
            return False
        return True

    def enviar_reserva(self):
        """Obtiene los datos y guarda la reserva."""
        # Recoge los datos del formulario
        tipo_doc = self.input_tipo_doc.currentText()
        num_doc = self.input_num_doc.text()
        nombre = self.input_nombre.text()
        apellido = self.input_apellido.text()
        fecha_nacimiento = self.input_fecha_nacimiento.date().toString("yyyy-MM-dd")
        genero = self.input_genero.currentText()
        telefono = self.input_telefono.text()
        email = self.input_email.text()
        nacionalidad = self.input_nacionalidad.text()
        fecha_salida = self.input_fecha_salida.date().toString("yyyy-MM-dd")
        metodo_pago = self.input_metodo_pago.currentText()
        referencia = self.input_referencia.text() if metodo_pago == "Transferencia" else None

        # Obtener duración en días desde el QSpinBox
        duracion_dias = self.input_duracion.value()

        # Obtener el monto total desde el QLineEdit
        monto_total_str = self.input_total_a_pagar.text()

        # Obtener el ID del paquete seleccionado (sin pasarle un argumento)
        id_paquete = self.obtener_id_paquete()

        # Limpiar cualquier símbolo de moneda y convertir a flotante
        try:
            monto_total = float(monto_total_str.replace("USD", "").replace("$", "").strip())
        except ValueError:
            QMessageBox.warning(self, "Monto inválido", "El monto total no es válido.")
            return

        # Verifica que todos los campos requeridos estén completos
        if not all([tipo_doc, num_doc, nombre, apellido, fecha_nacimiento, telefono, email, nacionalidad, fecha_salida, metodo_pago]):
            QMessageBox.warning(self, "Campos incompletos", "Por favor, completa todos los campos obligatorios.")
            return

        # Validar fechas antes de guardar (si aplica)
        if not self.validar_fechas():
            return

        # Guardar la reserva
        try:
            if self.reserva.guardar_reserva(tipo_doc, num_doc, nombre, apellido, fecha_nacimiento, genero, telefono, email,
                                            nacionalidad, duracion_dias, fecha_salida, monto_total, id_paquete, metodo_pago, referencia):
                # Mensaje de éxito
                QMessageBox.information(self, "Reserva Enviada", "Tu reserva ha sido enviada con éxito.")

                # Abrir la ventana de impresión
                ventana_impresion = VentanaImpresion(num_doc, self)
                ventana_impresion.exec()

                self.close()  # Cierra el formulario principal
            else:
                # Si la reserva no se guarda correctamente
                QMessageBox.warning(self, "Error al guardar", "Hubo un problema al guardar tu reserva. Inténtalo de nuevo.")
        except Exception as e:
            # Si hay error de conexión o cualquier otro problema
            QMessageBox.warning(self, "Error de Conexión", f"No se pudo conectar a la base de datos. Error: {str(e)}")

    def regresar_a_principal(self):
        self.close()
        self.pantalla_principal = VentanaPrincipal(self.usuario)
        self.pantalla_principal.show()


