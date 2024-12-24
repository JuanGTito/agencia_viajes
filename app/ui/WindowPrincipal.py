from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QLabel, QHBoxLayout, QMenu, QAction
from PyQt5.QtCore import Qt
from app.services.database import crear_conexion
from app.ui.WindowPerfil import PerfilDialog
from app.ui.WindowUser import GestionUsuariosWindow
from app.ui.WindowLogin import VentanaLogin
import os

class VentanaPrincipal(QWidget):
    def __init__(self, usuario):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle('Agencia de Viajes')
        self.setFixedSize(600, 800)  # Fijar el tamaño de la ventana para que no sea redimensionable

        self.usuario = usuario
        self.cerrando_sesion = False

        # Fondo de la ventana
        self.fondo_label = QLabel(self)
        self.fondo_label.setPixmap(QPixmap(os.getenv('IMG_FONDO')))
        self.fondo_label.setScaledContents(True)  # Escalar la imagen para ajustarse al QLabel
        self.fondo_label.resize(self.size())

        self.setWindowIcon(QIcon(os.getenv('IMG_ICO')))

        # Layout principal
        self.layout = QVBoxLayout()

        # Botón circular con inicial del tipo de usuario
        self.init_button = QPushButton(self)
        self.init_button.setText(self.usuario[0].upper())  # Inicial en mayúscula
        self.init_button.setFixedSize(40, 40)
        self.init_button.setFont(QFont("Arial", 14, QFont.Bold))

        # Modificar el estilo para el fondo gris claro, bordes negros y centrar el texto
        self.init_button.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color: #D3D3D3;  /* Gris claro */
                color: black;  /* Texto negro */
                border: 2px solid black;  /* Borde negro */
                text-align: center;  /* Centrar el texto */
                padding: 0px;  /* Asegurarse de que el texto esté centrado */
            }
            QPushButton:hover {
                background-color: #A9A9A9;  /* Gris más oscuro al pasar el ratón */
            }
            QPushButton::menu-indicator {
                width: 0px;
                height: 0px;
                image: none;  /* Eliminar el triángulo de menú desplegable */
            }
        """)

        # Menú desplegable
        self.menu = QMenu(self)
        opcion1 = QAction("Perfil", self)
        opcion3 = QAction("Cerrar sesión", self)
        self.menu.addAction(opcion1)

        # Conectar la acción de "Perfil"
        opcion1.triggered.connect(self.abrir_perfil)

        # Verificar si el usuario es administrador
        if self.es_admin(self.usuario):  # Si el usuario es administrador
            opcion4 = QAction("Agregar nuevo usuario", self)
            opcion4.triggered.connect(self.abrir_agregar_usuario)
            self.menu.addAction(opcion4)  # Agregar opción para agregar usuario

        self.menu.addAction(opcion3)
        opcion3.triggered.connect(self.cerrar_sesion)  # Agregar opción de cerrar sesión

        # Conectar el menú al botón
        self.init_button.setMenu(self.menu)

        # Layout para colocar el botón a la derecha
        header_layout = QHBoxLayout()
        header_layout.addStretch()  # Empuja el botón al extremo derecho
        header_layout.addWidget(self.init_button)

        # Añadir el layout al principal
        self.layout.addLayout(header_layout)

        # Layout para el encabezado (Logo y nombre del sistema)
        top_layout = QVBoxLayout()

        # Agregar el logo
        self.logo_label = QLabel(self)
        logo_pixmap = QPixmap(os.getenv('IMG_LOGO'))  # Cargar logo desde una ruta de imagen
        self.logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.KeepAspectRatio))  # Escalar el logo
        top_layout.addWidget(self.logo_label, alignment=Qt.AlignCenter)  # Centrado del logo

        # Agregar el nombre del sistema
        self.nombre_label = QLabel('Agencia de Viajes', self)
        self.nombre_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        top_layout.addWidget(self.nombre_label, alignment=Qt.AlignCenter)  # Centrado del nombre

        # Agregar el layout del encabezado al layout principal
        self.layout.addLayout(top_layout)

        # Espaciadores para centrar los botones en la ventana
        self.layout.addStretch(1)  # Empujar los botones hacia el centro

        # Layout para los botones (centrados)
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)  # Alineación de los botones al centro

        self.agregar_boton_con_imagen(button_layout, "Reservar", os.getenv('IMG_RESERVAR'), self.show_reserva)
        self.agregar_boton_con_imagen(button_layout, "Buscar", os.getenv('IMG_BUSCAR'), self.show_buscar)
        self.agregar_boton_con_imagen(button_layout, "Destinos", os.getenv('IMG_DESTINO'), self.show_destinos)
        self.agregar_boton_con_imagen(button_layout, "Reportes", os.getenv('IMG_REPORTE'), self.show_reportes)

        # Agregar el layout de botones al layout principal
        self.layout.addLayout(button_layout)

        self.layout.addStretch(3)  # Empujar más abajo para centrar verticalmente los botones

        # Footer (pie de página)
        footer_layout = QHBoxLayout()
        self.footer_label = QLabel('© 2024 Agencia de Viajes - Todos los derechos reservados.', self)
        self.footer_label.setStyleSheet("font-size: 12px; color: gray;")
        footer_layout.addWidget(self.footer_label, alignment=Qt.AlignCenter)  # Centrado del pie de página

        # Agregar el footer al layout principal
        self.layout.addLayout(footer_layout)

        # Establecer el layout principal
        self.setLayout(self.layout)

    def agregar_boton_con_imagen(self, layout, texto, imagen, funcion):
        # Crear un QHBoxLayout para cada botón
        boton_layout = QHBoxLayout()

        # Crear el QLabel para la imagen
        imagen_label = QLabel(self)
        pixmap = QPixmap(imagen)

        if not pixmap.isNull():  # Verificar si la imagen se cargó correctamente
            imagen_label.setPixmap(pixmap.scaled(30, 30, Qt.KeepAspectRatio))  # Ajustar tamaño de la imagen
        else:
            print(f"Error al cargar la imagen: {imagen}")

        imagen_label.setFixedSize(30, 30)  # Tamaño de la imagen

        # Crear el botón
        boton = QPushButton(texto)
        boton.setStyleSheet("font-size: 16px;")
        boton.setFixedWidth(200)
        boton.setFixedHeight(45)
        boton.clicked.connect(funcion)

        # Agregar la imagen y el botón al layout horizontal
        boton_layout.addWidget(imagen_label)  # Imagen a la izquierda
        boton_layout.addWidget(boton)  # Botón a la derecha

        # Agregar el layout horizontal al layout de botones
        layout.addLayout(boton_layout)

    def show_reserva(self):
        # Lógica para abrir la pantalla de reserva
        from app.ui.WindowReservar import ReservaScreen  # Importar aquí para evitar problemas de importación circular
        self.reserve_screen = ReservaScreen(self.usuario)
        self.reserve_screen.show()
        self.hide()  # Ocultar la ventana principal

    def show_buscar(self):
        # Lógica para abrir la pantalla de búsqueda
        from app.ui.windowBuscar import BuscarReservaScreen  # Importar aquí para evitar problemas de importación circular
        self.buscar_screen = BuscarReservaScreen(self.usuario)
        self.buscar_screen.show()
        self.hide()  # Ocultar la ventana principal

    def show_destinos(self, usuario):
        # Lógica para abrir la pantalla de destinos
        from app.ui.WindowDestinos import DestinosScreen
        self.destinos_screen = DestinosScreen(self.usuario)
        print(f"Nombre de usuario recibido: {usuario}")
        self.destinos_screen.show()
        self.hide()  # Ocultar la ventana principal

    def show_reportes(self):
        # Lógica para abrir la pantalla de destinos
        from app.ui.WindowReportes import ReportePDFScreen  # Asegúrate de que esta clase existe
        self.reportes_screen = ReportePDFScreen(self.usuario)
        self.reportes_screen.show()
        self.hide()  # Ocultar la ventana principal

    def es_admin(self, usuario):
        """
        Verifica si el usuario tiene rol de administrador.
        Retorna True si el usuario es administrador, False en caso contrario.
        """
        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT rol FROM usuario WHERE user_nombre = %s", (usuario,))
            datos = cursor.fetchone()
            conn.close()

            if datos and datos[0] == "Admin":  # Verifica si el tipo de usuario es 'admin'
                return True
            return False
        except Exception as e:
            print(f"Error al verificar rol de administrador: {e}")
            return False

    def abrir_perfil(self):
        """Método para abrir el diálogo de perfil."""
        perfil_dialog = PerfilDialog(self.usuario, self)  # Crear una instancia del diálogo de perfil
        perfil_dialog.exec_()
    
    def abrir_agregar_usuario(self):
        """Abrir el formulario de agregar nuevo usuario."""
        agregar_usuario_dialog = GestionUsuariosWindow(self)
        agregar_usuario_dialog.exec_()
    
    def cerrar_sesion(self):
        """Cerrar la sesión y redirigir a la pantalla de inicio de sesión"""
        confirm = QMessageBox.question(self, "Confirmar Cierre de Sesión", 
                                       "¿Estás seguro de que deseas cerrar sesión?", 
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirm == QMessageBox.Yes:
            # Limpiar la sesión
            self.usuario = None  # Limpiar el usuario actual
            self.cerrando_sesion = True  # Establecer que estamos cerrando sesión

            # Cerrar la ventana actual
            self.close()  # Esto llamará a closeEvent y no mostrará el cuadro de confirmación

            # Abrir la ventana de login
            self.abrir_login()

    def abrir_login(self):
        """Abrir la ventana de login"""
        self.ventana_login = VentanaLogin()  # Crear la instancia de la ventana de login
        self.ventana_login.exec_()

    def closeEvent(self, event):
        """Confirmar antes de cerrar la ventana (al hacer clic en la 'X')"""
        if not self.cerrando_sesion:  # Solo mostrar confirmación si no estamos cerrando sesión
            reply = QMessageBox.question(self, 'Cerrar', '¿Estás seguro de que quieres salir?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()  # Aceptar el evento de cierre
            else:
                event.ignore()  # Ignorar el evento de cierre (no cerrar la ventana)
        else:
            event.accept()  # Aceptar el evento de cierre si estamos cerrando sesión

