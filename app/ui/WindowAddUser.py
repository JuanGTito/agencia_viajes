from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from app.services.database import crear_conexion
import bcrypt  # Importar bcrypt para encriptar la contraseña

class AgregarUsuarioWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Usuario")
        self.setFixedSize(400, 300)

        # Layout principal
        layout = QVBoxLayout()

        # Formulario para ingresar los datos del usuario
        form_layout = QFormLayout()

        self.input_nombre = QLineEdit(self)
        self.input_apellido = QLineEdit(self)
        self.input_correo = QLineEdit(self)
        self.input_telefono = QLineEdit(self)
        self.input_usuario = QLineEdit(self)
        self.input_contrasena = QLineEdit(self)
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        self.input_rol = QComboBox(self)
        self.input_rol.addItems(["Usuario", "Admin"])

        form_layout.addRow("Nombre:", self.input_nombre)
        form_layout.addRow("Apellido:", self.input_apellido)
        form_layout.addRow("Correo:", self.input_correo)
        form_layout.addRow("Teléfono:", self.input_telefono)
        form_layout.addRow("Nombre de Usuario:", self.input_usuario)
        form_layout.addRow("Contraseña:", self.input_contrasena)
        form_layout.addRow("Rol:", self.input_rol)

        layout.addLayout(form_layout)

        # Botón para guardar el usuario
        self.btn_guardar = QPushButton("Guardar Usuario")
        self.btn_guardar.clicked.connect(self.guardar_usuario)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

    def guardar_usuario(self):
        """Guardar un nuevo usuario en la base de datos con la contraseña encriptada."""
        nombre = self.input_nombre.text()
        apellido = self.input_apellido.text()
        correo = self.input_correo.text()
        telefono = self.input_telefono.text()
        usuario = self.input_usuario.text()
        contrasena = self.input_contrasena.text()
        rol = self.input_rol.currentText()

        if not all([nombre, apellido, correo, usuario, contrasena]):
            QMessageBox.warning(self, "Campos incompletos", "Por favor, complete todos los campos obligatorios.")
            return

        # Encriptar la contraseña con bcrypt
        contrasena_encriptada = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuario (nombre, apellido, correo, telefono, user_nombre, contrasena, rol) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (nombre, apellido, correo, telefono, usuario, contrasena_encriptada, rol)
            )
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Usuario Agregado", "El usuario ha sido agregado exitosamente.")
            self.accept()  # Cerrar la ventana

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al agregar el usuario: {str(e)}")
