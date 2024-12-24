from PyQt5.QtWidgets import QDialog, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer
from app.models.reserva import Reserva 
from app.ui.WindowPrincipal import VentanaPrincipal
from app.ui.WindowAdd import AgregarDestinoDialog
from app.ui.WindowEdit import EditarDestinoDialog
from app.services.database import crear_conexion
from dotenv import load_dotenv
import os

load_dotenv()

class DestinosScreen(QWidget):
    def __init__(self, usuario):
        super().__init__()
        self.setWindowTitle("Destinos")
        self.setFixedSize(700, 800)

        print(f"Nombre de usuario recibido: {usuario}")
        
        self.usuario = usuario

        self.fondo_label = QLabel(self)
        self.fondo_label.setPixmap(QPixmap(os.getenv('IMG_FONDO')))
        self.fondo_label.setScaledContents(True)  # Escalar la imagen para ajustarse al QLabel
        self.fondo_label.resize(self.size())

        self.setWindowIcon(QIcon(os.getenv('IMG_ICO')))

        self.fontNegrita = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        self.layout = QVBoxLayout()

        # Etiqueta
        self.label = QLabel("Destinos Disponibles:")
        self.layout.addWidget(self.label)

        # Verificar si el usuario es admin antes de mostrar el botón de agregar
        if self.es_admin(self.usuario):
            self.btn_agregar = QPushButton("Agregar Destino")
            self.btn_agregar.setFont(self.fontNegrita)
            self.btn_agregar.clicked.connect(self.agregar_destino)
            layout_izquierda = QHBoxLayout()
            layout_izquierda.addWidget(self.btn_agregar, alignment=Qt.AlignLeft)
            self.layout.addLayout(layout_izquierda)

        # Tabla de destinos
        self.tabla_destinos = QTableWidget()
        self.tabla_destinos.setColumnCount(3)  # Tres columnas: Lugar, Descripcion, Accion
        self.tabla_destinos.setHorizontalHeaderLabels(["Lugar", "Descripcion", "Accion"])  # Encabezados de columnas
        self.cargar_destinos()  # Cargar destinos desde la base de datos
        
        # Configuración de la tabla
        self.tabla_destinos.setSelectionBehavior(QTableWidget.SelectRows)  # Selección de fila
        self.tabla_destinos.setSelectionMode(QTableWidget.NoSelection)  # Sin selección
        self.tabla_destinos.setShowGrid(False)  # Ocultar líneas de cuadrícula
        self.tabla_destinos.setAlternatingRowColors(True)  # Colores alternos para filas

        row_height = 50  # Puedes ajustar este valor según el tamaño que desees
        self.tabla_destinos.setRowHeight(0, row_height)  # Establecer altura para la primera fila
        for row in range(self.tabla_destinos.rowCount()):
            self.tabla_destinos.setRowHeight(row, row_height)

        self.layout.addWidget(self.tabla_destinos)

        # Botón para regresar a la pantalla principal
        self.btn_regresar = QPushButton("Regresar")
        self.btn_regresar.setFixedHeight(30)
        self.btn_regresar.setFont(self.fontNegrita)
        self.btn_regresar.clicked.connect(self.regresar_a_principal)  # Conectar a la función de regreso
        
        # Contenedor horizontal para centrar el botón
        layout_centrado = QHBoxLayout()
        layout_centrado.addWidget(self.btn_regresar, alignment=Qt.AlignCenter)  # Agregar el botón con alineación centrada

        # Agregar el contenedor centrado al diseño principal
        self.layout.addLayout(layout_centrado)

        self.setLayout(self.layout)

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

    def cargar_destinos(self):
        """Carga los destinos en la tabla."""
        reserva = Reserva()  # Instancia de la clase Reserva
        destinos = reserva.obtener_destinos()  # Obtener destinos
        
        if not destinos:
            QMessageBox.warning(self, "Sin Destinos", "No hay destinos disponibles.")
            return
        
        # Verificar si el usuario es administrador
        es_admin = self.es_admin(self.usuario)
    
        # Configurar filas de la tabla
        self.tabla_destinos.setRowCount(len(destinos))  # Establecer el número de filas según el número de destinos
    
        # Mostrar la columna "Acción" solo si el usuario es administrador
        if es_admin:
            self.tabla_destinos.setColumnCount(3)  # Asegurarse de que haya tres columnas: Lugar, Descripción y Acción
        else:
            self.tabla_destinos.setColumnCount(2)  # Si no es admin, mostrar solo dos columnas (sin "Acción")
        
        # Llenar la tabla con los datos de los destinos
        for row, (id_destino, (nombre, descripcion)) in enumerate(destinos.items()):
            # Columna 0: Nombre del lugar
            self.tabla_destinos.setItem(row, 0, QTableWidgetItem(nombre))
            
            # Columna 1: Descripción
            descripcion_item = QTableWidgetItem(descripcion)
            descripcion_item.setTextAlignment(Qt.AlignTop)  # Alinear la descripción hacia arriba
            self.tabla_destinos.setItem(row, 1, descripcion_item)
    
            # Habilitar el ajuste de texto para la columna de Descripción
            self.tabla_destinos.item(row, 1).setText(descripcion)  # Actualiza el texto en la celda
            self.tabla_destinos.setWordWrap(True)  # Habilitar ajuste de texto
    
            # Si el usuario es admin, agregar los botones de Editar y Eliminar
            if es_admin:
                btn_editar = QPushButton("Editar")
                btn_editar.clicked.connect(lambda _, row=row: self.editar_destino(row))
                btn_eliminar = QPushButton("Eliminar")
                btn_eliminar.clicked.connect(lambda _, row=row: self.eliminar_destino(row))
    
                self.tabla_destinos.setCellWidget(row, 2, self.crear_acciones_layout(btn_editar, btn_eliminar))
        
        # Ajustar tamaño de columnas y filas automáticamente
        self.tabla_destinos.resizeColumnsToContents()  # Ajustar el tamaño de las columnas automáticamente
        self.tabla_destinos.resizeRowsToContents()  # Ajustar el tamaño de las filas automáticamente


    def crear_acciones_layout(self, btn_editar, btn_eliminar):
        """Crea un layout horizontal con los botones de editar y eliminar."""
        layout = QHBoxLayout()
        layout.addWidget(btn_editar)
        layout.addWidget(btn_eliminar)
        layout.setAlignment(Qt.AlignCenter)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def agregar_destino(self):
        """Lógica para agregar un nuevo destino desde la pantalla de destinos."""
        dialog = AgregarDestinoDialog(self)  # Crear una instancia del diálogo
        if dialog.exec_() == QDialog.Accepted:  # Mostrar el diálogo de forma modal
            self.cargar_destinos()  # Volver a cargar los destinos en la tabla tras agregar uno

    def editar_destino(self, row):
        """Lógica para editar un destino existente desde la pantalla principal."""
        nombre = self.tabla_destinos.item(row, 0).text()
        descripcion = self.tabla_destinos.item(row, 1).text()

        dialog = EditarDestinoDialog(nombre, descripcion, self)  # Crear una instancia del diálogo con datos precargados
        if dialog.exec_() == QDialog.Accepted:  # Mostrar el diálogo de forma modal
            self.cargar_destinos()  # Volver a cargar los destinos en la tabla tras editar uno

    def eliminar_destino(self, row):
        """Lógica para eliminar un destino."""
        nombre = self.tabla_destinos.item(row, 0).text()

        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar el destino '{nombre}'?",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            try:
                # Usar la función `crear_conexion` para conectarse a la base de datos
                conn = crear_conexion()
                cursor = conn.cursor()

                # Eliminar el destino de la base de datos
                cursor.execute("DELETE FROM catalogo_destino WHERE destino = %s", (nombre,))
                conn.commit()
                conn.close()

                QMessageBox.information(self, "Destino Eliminado", "El destino ha sido eliminado exitosamente.")
                self.cargar_destinos()  # Volver a cargar los destinos en la tabla tras eliminar uno
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al eliminar el destino: {str(e)}")

    def regresar_a_principal(self):
        self.close()
        self.pantalla_principal = VentanaPrincipal(self.usuario)
        self.pantalla_principal.show()

