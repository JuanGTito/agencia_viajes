from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
from app.services.database import crear_conexion
import bcrypt

class VentanaLogin(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login')
        self.setMinimumSize(400, 600)

        self.setWindowIcon(QIcon('app/resources/images/icon.ico'))  # Ruta al ícono

        # Estilo de la fuente para los labels (negrita, tamaño)
        font_negrita = QFont("Arial", 12, QFont.Bold)

        # Crear el logo y centrarlo
        self.label_logo = QLabel()
        self.cargar_logo()

        # Crear etiquetas y campos de usuario y contraseña
        self.label_usuario = QLabel("Usuario:")
        self.label_usuario.setFont(font_negrita)
        self.label_usuario.setAlignment(Qt.AlignCenter)
        self.input_usuario = QLineEdit()
        self.input_usuario.setFixedWidth(200)

        self.label_contrasena = QLabel("Contraseña:")
        self.label_contrasena.setFont(font_negrita)
        self.label_contrasena.setAlignment(Qt.AlignCenter)
        self.input_contrasena = QLineEdit()
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        self.input_contrasena.setFixedWidth(200)

        # Botón de iniciar sesión con tamaño reducido
        self.boton_login = QPushButton("Iniciar Sesión")
        self.boton_login.setFont(font_negrita)
        self.boton_login.setFixedWidth(120)
        self.boton_login.setFixedHeight(35)
        self.boton_login.clicked.connect(self.verificar_login)

        # Layout para centrar el botón horizontalmente
        layout_boton = QHBoxLayout()
        layout_boton.setAlignment(Qt.AlignCenter)
        layout_boton.addWidget(self.boton_login)

        # Layout principal
        layout_principal = QVBoxLayout()
        layout_principal.setAlignment(Qt.AlignCenter)  # Alineación vertical y horizontal centrada

        # Añadir el logo al layout principal
        layout_principal.addWidget(self.label_logo)

        # Añadir etiquetas y campos al layout principal (uno sobre otro)
        layout_principal.addWidget(self.label_usuario)
        layout_principal.addWidget(self.input_usuario)
        layout_principal.addWidget(self.label_contrasena)
        layout_principal.addWidget(self.input_contrasena)

        # Añadir el layout del botón al layout principal
        layout_principal.addLayout(layout_boton)

        # Establecer el layout principal en la ventana
        self.setLayout(layout_principal)

    def cargar_logo(self):
        """Carga el logo y lo ajusta al tamaño requerido."""
        pixmap = QPixmap("app/resources/images/logo.png")
        if pixmap.isNull():
            print("Error: El logo no se pudo cargar.")  # Manejo de error
            pixmap = QPixmap(150, 150)
            pixmap.fill()

        self.label_logo.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
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

        # Lógica para verificar el login.
        if self.verificar_credenciales(usuario, contrasena):
            self.accept()  # Cerrar el diálogo y aceptar el login
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
                contrasena_almacenada = resultado[0].encode('utf-8')  # Asegúrate de que esté en bytes
                # Compara el hash de la contraseña ingresada con el hash almacenado
                return bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_almacenada)
            
            return False

        except Exception as e:
            print(f"Error al verificar las credenciales: {e}")
            return False

        finally:
            cursor.close()
            conn.close()