import bcrypt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from app.services.database import crear_conexion
import re


class PerfilDialog(QDialog):
    def __init__(self, usuario_nombre, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Perfil del Usuario")
        self.setFixedSize(400, 350)  # Aumenté el tamaño para incluir la contraseña
        
        self.usuario_nombre = usuario_nombre  # Usuario que está accediendo al perfil
        self.fontNegrita = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        layout = QVBoxLayout()

        # Formulario de entrada
        form_layout = QFormLayout()

        # Campo para el nombre del usuario
        self.nombre_input = QLineEdit(self)
        form_layout.addRow(QLabel("Nombre:"), self.nombre_input)

        # Campo para el correo electrónico
        self.email_input = QLineEdit(self)
        form_layout.addRow(QLabel("Correo Electrónico:"), self.email_input)

        # Campo para cambiar la contraseña
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)  # Ocultar la contraseña
        form_layout.addRow(QLabel("Nueva Contraseña:"), self.password_input)

        # Botón para mostrar/ocultar la contraseña
        self.toggle_password_btn = QPushButton("👁️ Mostrar Contraseña")
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        
        # Botón para guardar cambios
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.setFont(self.fontNegrita)
        self.btn_guardar.clicked.connect(self.guardar_perfil)
        
        # Añadir formulario, botón de mostrar/ocultar contraseña y guardar cambios al layout
        layout.addLayout(form_layout)
        layout.addWidget(self.toggle_password_btn)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

        # Cargar los datos del perfil al inicializar el diálogo
        self.cargar_datos_perfil()

    def cargar_datos_perfil(self):
        """Cargar los datos del perfil del usuario desde la base de datos."""
        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, correo, contrasena FROM usuario WHERE user_nombre = %s", (self.usuario_nombre,))
            datos = cursor.fetchone()
            conn.close()

            if datos:
                self.nombre_input.setText(datos[0])  # Nombre
                self.email_input.setText(datos[1])  # Correo
                self.password_input.setText("")  # No mostramos la contraseña cifrada
                self.password_cifrada = datos[2]  # Guardamos la contraseña cifrada
            else:
                QMessageBox.warning(self, "Error", "No se encontraron datos para este usuario.")
        except Exception as e:
            print(f"Error al obtener los datos del usuario: {e}")
            QMessageBox.warning(self, "Error", "Hubo un error al cargar los datos del perfil.")

    def guardar_perfil(self):
        """Lógica para guardar los cambios en el perfil en la base de datos."""
        nombre = self.nombre_input.text()
        email = self.email_input.text()
        nueva_contraseña = self.password_input.text()

        # Validación de los campos
        if nombre and email:
            # Validar correo electrónico
            if not self.validar_email(email):
                QMessageBox.warning(self, "Correo Inválido", "Por favor, ingrese un correo electrónico válido.")
                return

            try:
                # Usar la función `crear_conexion` para conectarse a la base de datos
                conn = crear_conexion()
                cursor = conn.cursor()

                # Si se proporciona una nueva contraseña, la ciframos antes de guardarla
                if nueva_contraseña:
                    hashed_password = bcrypt.hashpw(nueva_contraseña.encode('utf-8'), bcrypt.gensalt())
                    cursor.execute("""
                        UPDATE usuario 
                        SET nombre = %s, correo = %s, contrasena = %s 
                        WHERE user_nombre = %s
                    """, (nombre, email, hashed_password, self.usuario_nombre))
                else:
                    cursor.execute("""
                        UPDATE usuario 
                        SET nombre = %s, correo = %s 
                        WHERE user_nombre = %s
                    """, (nombre, email, self.usuario_nombre))

                conn.commit()
                conn.close()

                QMessageBox.information(self, "Perfil Actualizado", "El perfil ha sido actualizado exitosamente.")
                self.accept()  # Cerrar el modal al guardar los cambios
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al actualizar el perfil: {str(e)}")
        else:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete todos los campos.")

    def validar_email(self, email):
        """Valida que el correo electrónico tenga un formato correcto."""
        patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(patron, email) is not None

    def toggle_password_visibility(self):
        """Alternar la visibilidad de la contraseña."""
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setText("👁️ Ocultar Contraseña")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setText("👁️ Mostrar Contraseña")
