from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox, QDateEdit, QStackedWidget, QDateEdit, QSpinBox
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import QDate
import os
from app.models.reserva import Reserva
from app.ui.WindowPrincipal import VentanaPrincipal
from app.services.database import crear_conexion

class ReservaScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Formulario de Reserva')
        self.setMinimumSize(600, 800)

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
        layout.addWidget(self.label_tipo_doc)
        layout.addWidget(self.input_tipo_doc)

        self.label_num_doc = QLabel("Número de Documento:")
        self.label_num_doc.setFont(self.fontNegrita)
        self.input_num_doc = QLineEdit()
        self.input_num_doc.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_num_doc.setFixedHeight(30)
        layout.addWidget(self.label_num_doc)
        layout.addWidget(self.input_num_doc)

        self.label_nombre = QLabel("Nombre Completo:")
        self.label_nombre.setFont(self.fontNegrita)
        self.input_nombre = QLineEdit()
        self.input_nombre.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_nombre.setFixedHeight(30)
        layout.addWidget(self.label_nombre)
        layout.addWidget(self.input_nombre)

        self.label_apellido = QLabel("Apellido:")
        self.label_apellido.setFont(self.fontNegrita)
        self.input_apellido = QLineEdit()
        self.input_apellido.setStyleSheet("QLineEdit { font-size: 14px; }")
        self.input_apellido.setFixedHeight(30)
        layout.addWidget(self.label_apellido)
        layout.addWidget(self.input_apellido)

        self.label_fecha_nacimiento = QLabel("Fecha de Nacimiento:")
        self.label_fecha_nacimiento.setFont(self.fontNegrita)
        self.input_fecha_nacimiento = QDateEdit()
        self.input_fecha_nacimiento.setCalendarPopup(True)
        layout.addWidget(self.label_fecha_nacimiento)
        layout.addWidget(self.input_fecha_nacimiento)

        self.label_genero = QLabel("Género:")
        self.label_genero.setFont(self.fontNegrita)
        self.input_genero = QComboBox()
        self.input_genero.addItems(["Masculino", "Femenino"])
        layout.addWidget(self.label_genero)
        layout.addWidget(self.input_genero)

        self.label_nacionalidad = QLabel("Nacionalidad:")
        self.label_nacionalidad.setFont(self.fontNegrita)
        self.input_nacionalidad = QLineEdit()
        layout.addWidget(self.label_nacionalidad)
        layout.addWidget(self.input_nacionalidad)

        self.label_telefono = QLabel("Número de Teléfono:")
        self.label_telefono.setFont(self.fontNegrita)
        self.input_telefono = QLineEdit()
        layout.addWidget(self.label_telefono)
        layout.addWidget(self.input_telefono)

        self.label_email = QLabel("Correo Electrónico:")
        self.label_email.setFont(self.fontNegrita)
        self.input_email = QLineEdit()
        layout.addWidget(self.label_email)
        layout.addWidget(self.input_email)

        # Botón para pasar a la siguiente sección
        self.btn_siguiente = QPushButton("Siguiente")
        self.btn_siguiente.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(self.btn_siguiente)

        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(self.regresar_a_principal)  # Conectar a la función de regreso
        layout.addWidget(self.btn_regresar)

        # Crear widget y agregar layout
        personal_widget = QWidget()
        personal_widget.setLayout(layout)
        self.stacked_widget.addWidget(personal_widget)

    def crear_detalle_destino(self):
        layout = QVBoxLayout()
    
        destinos = self.reserva.obtener_destinos()
    
        self.label_destino = QLabel("Destino:")
        self.label_destino.setFont(self.fontNegrita)
        self.input_destino = QComboBox()
    
        for id_destino, (destino, descripcion) in destinos.items():
            self.input_destino.addItem(f"{destino} - Descripción: {descripcion}", id_destino)
    
        self.input_destino.currentIndexChanged.connect(self.actualizar_campo_con_id_destino)
    
        layout.addWidget(self.label_destino)
        layout.addWidget(self.input_destino)
    
        self.label_paquete = QLabel("Tipo de Paquete:")
        self.label_paquete.setFont(self.fontNegrita)
        self.input_paquete = QComboBox()
        layout.addWidget(self.label_paquete)
        layout.addWidget(self.input_paquete)

        self.label_fecha_salida = QLabel("Fecha de Salida:")
        self.label_fecha_salida.setFont(self.fontNegrita)
        self.input_fecha_salida = QDateEdit()
        self.input_fecha_salida.setMinimumDate(QDate.currentDate())
        layout.addWidget(self.label_fecha_salida)
        layout.addWidget(self.input_fecha_salida)

        # Duración (cambiar a QSpinBox)
        self.label_duracion = QLabel("Duración (días):")
        self.label_duracion.setFont(self.fontNegrita)
        self.input_duracion = QSpinBox()
        self.input_duracion.setMinimum(1)  # Mínimo 1 día
        self.input_duracion.setMaximum(365)  # Máximo 365 días (un año)
        self.input_duracion.textChanged.connect(self.calcular_precio_total)
        layout.addWidget(self.label_duracion)
        layout.addWidget(self.input_duracion)

        self.label_fecha_regreso = QLabel("Fecha Llegada:")
        self.label_fecha_regreso.setFont(self.fontNegrita)
        self.input_fecha_regreso = QDateEdit()
        self.input_fecha_regreso.setReadOnly(True)  # Solo lectura
        layout.addWidget(self.label_fecha_regreso)
        layout.addWidget(self.input_fecha_regreso)

        self.input_duracion.valueChanged.connect(self.actualizar_fecha_llegada)
        self.input_fecha_salida.dateChanged.connect(self.actualizar_fecha_llegada)  # Conectar a la señal dateChanged de fecha de salida
    
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(self.btn_regresar)
    
        self.btn_siguiente_destino = QPushButton("Siguiente")
        self.btn_siguiente_destino.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        layout.addWidget(self.btn_siguiente_destino)
    
        destino_widget = QWidget()
        destino_widget.setLayout(layout)
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
        for id_paquete, tipo_paquete, precio_diario in paquetes:
            paquete_texto = f"{tipo_paquete} - Precio Diario: {precio_diario} USD"
            self.input_paquete.addItem(paquete_texto, (id_paquete, precio_diario))

    def obtener_id_paquete(self):
        # Obtener el ID del paquete seleccionado en el ComboBox
        paquete_seleccionado = self.input_paquete.currentData()
        if paquete_seleccionado:
            id_paquete, _ = paquete_seleccionado
            print(f"ID del paquete seleccionado: {id_paquete}")
            return id_paquete
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
            _, precio_diario = paquete_seleccionado
            total_a_pagar = dias_estancia * precio_diario
            self.input_total_a_pagar.setText(f"{total_a_pagar} USD")
        else:
            self.input_total_a_pagar.setText("Paquete no válido")

    def crear_reserva_pago(self):
        """Tercera sección: Reserva y Pago"""
        layout = QVBoxLayout()

        self.label_total_a_pagar = QLabel("Total a Pagar:")
        self.label_total_a_pagar.setFont(self.fontNegrita)
        self.input_total_a_pagar = QLineEdit()
        self.input_total_a_pagar.setReadOnly(True)
        layout.addWidget(self.label_total_a_pagar)
        layout.addWidget(self.input_total_a_pagar)

        self.label_metodo_pago = QLabel("Método de Pago:")
        self.label_metodo_pago.setFont(self.fontNegrita)
        self.input_metodo_pago = QComboBox()
        self.input_metodo_pago.addItems(["Transferencia", "Efectivo"])
        layout.addWidget(self.label_metodo_pago)
        layout.addWidget(self.input_metodo_pago)

        self.label_referencia = QLabel("Número de Referencia (si aplica):")
        self.label_referencia.setFont(self.fontNegrita)
        self.input_referencia = QLineEdit()
        layout.addWidget(self.label_referencia)
        layout.addWidget(self.input_referencia)

        # Botones para regresar y enviar
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(self.btn_regresar)

        self.btn_enviar = QPushButton("Enviar Reserva")
        self.btn_enviar.clicked.connect(self.enviar_reserva)
        self.btn_enviar.clicked.connect(self.regresar_a_principal)
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
                self.close()  # Cierra el formulario
            else:
                # Si la reserva no se guarda correctamente
                QMessageBox.warning(self, "Error al guardar", "Hubo un problema al guardar tu reserva. Inténtalo de nuevo.")
        except Exception as e:
            # Si hay error de conexión o cualquier otro problema
            QMessageBox.warning(self, "Error de Conexión", f"No se pudo conectar a la base de datos. Error: {str(e)}")

    def regresar_a_principal(self):
        self.close()
        self.pantalla_principal = VentanaPrincipal()
        self.pantalla_principal.show()


