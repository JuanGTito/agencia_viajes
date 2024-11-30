from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
import os

class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle('Agencia de Viajes')
        self.setFixedSize(600, 800)  # Fijar el tamaño de la ventana para que no sea redimensionable

        # Fondo de la ventana
        self.fondo_label = QLabel(self)
        self.fondo_label.setPixmap(QPixmap(os.getenv('IMG_FONDO')))
        self.fondo_label.setScaledContents(True)  # Escalar la imagen para ajustarse al QLabel
        self.fondo_label.resize(self.size())

        self.setWindowIcon(QIcon(os.getenv('IMG_ICO')))

        # Layout principal
        self.layout = QVBoxLayout()

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
        self.reserve_screen = ReservaScreen()
        self.reserve_screen.show()
        self.hide()  # Ocultar la ventana principal

    def show_buscar(self):
        # Lógica para abrir la pantalla de búsqueda
        from app.ui.windowBuscar import BuscarReservaScreen  # Importar aquí para evitar problemas de importación circular
        self.buscar_screen = BuscarReservaScreen()
        self.buscar_screen.show()
        self.hide()  # Ocultar la ventana principal

    def show_destinos(self):
        # Lógica para abrir la pantalla de destinos
        from app.ui.WindowDestinos import DestinosScreen  # Asegúrate de que esta clase existe
        self.destinos_screen = DestinosScreen()
        self.destinos_screen.show()
        self.hide()  # Ocultar la ventana principal

    def show_reportes(self):
        # Lógica para abrir la pantalla de destinos
        from app.ui.WindowReportes import ReportePDFScreen  # Asegúrate de que esta clase existe
        self.reportes_screen = ReportePDFScreen()
        self.reportes_screen.show()
        self.hide()  # Ocultar la ventana principal

    def closeEvent(self, event):
        # Confirmar antes de cerrar la aplicación
        reply = QMessageBox.question(self, 'Cerrar', '¿Estás seguro de que quieres salir?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

