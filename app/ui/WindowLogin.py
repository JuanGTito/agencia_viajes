from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
from app.services.database import crear_conexion
import bcrypt
import os

class VentanaLogin(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login')
        self.setMinimumSize(500, 700)

        self.setWindowIcon(QIcon(os.getenv('IMG_ICO')))

        self.fondo_label = QLabel(self)
        self.fondo_label.setPixmap(QPixmap(os.getenv('IMG_FONDO')))
        self.fondo_label.setScaledContents(True)  # Escalar la imagen para ajustarse al QLabel
        self.fondo_label.resize(self.size())

        fontNegrita = QFont("Arial", 17, QFont.Bold)

        self.label_logo = QLabel()
        self.cargar_logo()

        self.label_usuario = QLabel("Usuario:")
        self.label_usuario.setFont(fontNegrita)
        self.label_usuario.setAlignment(Qt.AlignCenter)
        self.input_usuario = QLineEdit()
        self.input_usuario.setStyleSheet("QLineEdit { font-size: 15px; }")
        self.input_usuario.setFixedWidth(200)
        self.input_usuario.setFixedHeight(30)

        self.label_contrasena = QLabel("Contraseña:")
        self.label_contrasena.setFont(fontNegrita)
        self.label_contrasena.setAlignment(Qt.AlignCenter)
        self.input_contrasena = QLineEdit()
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        self.input_contrasena.setStyleSheet("QLineEdit { font-size: 15px; }")
        self.input_contrasena.setFixedWidth(200)
        self.input_contrasena.setFixedHeight(30)

        self.boton_login = QPushButton("Iniciar Sesión")
        self.boton_login.setFont(fontNegrita)
        self.boton_login.setFixedWidth(180)
        self.boton_login.setFixedHeight(35)
        self.boton_login.clicked.connect(self.verificar_login)

        layout_boton = QHBoxLayout()
        layout_boton.setAlignment(Qt.AlignCenter)
        layout_boton.addWidget(self.boton_login)

        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignCenter)

        layout_principal.addWidget(self.label_logo)

        layout_principal.addWidget(self.label_usuario)
        layout_principal.addWidget(self.input_usuario)
        layout_principal.addWidget(self.label_contrasena)
        layout_principal.addWidget(self.input_contrasena)

        layout_principal.addLayout(layout_boton)

        self.setLayout(layout_principal)

    def cargar_logo(self):
        """Carga el logo y lo ajusta al tamaño requerido."""
        pixmap = QPixmap(os.getenv('IMG_LOGO'))
        if pixmap.isNull():
            print("Error: El logo no se pudo cargar.")
            pixmap = QPixmap(150, 150)
            pixmap.fill()

        self.label_logo.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        self.label_logo.setAlignment(Qt.AlignCenter)

    def crear_campo(self, texto, font, es_contrasena=False):
        """Crea un label y un campo de entrada, con opciones para contraseña."""
        label = QLabel(texto)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)

        input_text = QLineEdit()
        input_text.setFixedWidth(200)
        if es_contrasena:
            input_text.setEchoMode(QLineEdit.Password)

        return label, input_text

    def verificar_login(self):
        usuario = self.input_usuario.text()
        contrasena = self.input_contrasena.text()

        if self.verificar_credenciales(usuario, contrasena):
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")

    def verificar_credenciales(self, usuario, contrasena):
        """Verifica las credenciales del usuario en la base de datos."""
        conn = crear_conexion()
        if conn is None:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT contrasena FROM usuario WHERE user_nombre = %s", (usuario,))
            resultado = cursor.fetchone()
            
            if resultado is not None:
                contrasena_almacenada = resultado[0].encode('utf-8')
                return bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_almacenada)
            
            return False

        except Exception as e:
            print(f"Error al verificar las credenciales: {e}")
            return False

        finally:
            cursor.close()
            conn.close()