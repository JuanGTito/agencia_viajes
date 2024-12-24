from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
import bcrypt
from app.services.database import crear_conexion

class EditarUsuarioWindow(QDialog):
    def __init__(self, id_usuario, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Usuario")
        self.setFixedSize(400, 300)
        self.id_usuario = id_usuario

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

        # Botón para guardar los cambios
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.clicked.connect(self.guardar_cambios)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

        # Cargar los datos actuales del usuario
        self.cargar_usuario()

    def cargar_usuario(self):
        """Cargar los datos del usuario desde la base de datos para editarlos."""
        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, apellido, correo, telefono, user_nombre, contrasena, rol FROM usuario WHERE id_usuario = %s", (self.id_usuario,))
            usuario = cursor.fetchone()
            conn.close()

            if usuario:
                self.input_nombre.setText(usuario[0])
                self.input_apellido.setText(usuario[1])
                self.input_correo.setText(usuario[2])
                self.input_telefono.setText(usuario[3])
                self.input_usuario.setText(usuario[4])
                self.input_contrasena.setText('')  # No mostrar la contraseña original
                self.input_rol.setCurrentText(usuario[6])
            else:
                QMessageBox.warning(self, "Error", "Usuario no encontrado.")
                self.reject()  # Cerrar la ventana si no se encuentra el usuario

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al cargar los datos del usuario: {str(e)}")

    def guardar_cambios(self):
        """Guardar los cambios realizados en el usuario."""
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

        # Encriptar la contraseña antes de guardarla
        contrasena_encriptada = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuario SET nombre = %s, apellido = %s, correo = %s, telefono = %s, "
                "user_nombre = %s, contrasena = %s, rol = %s WHERE id_usuario = %s",
                (nombre, apellido, correo, telefono, usuario, contrasena_encriptada, rol, self.id_usuario)
            )
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Usuario Actualizado", "Los datos del usuario han sido actualizados.")
            self.accept()  # Cerrar la ventana

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al actualizar los datos del usuario: {str(e)}")