from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QDialog
from PyQt5.QtCore import Qt
from app.services.database import crear_conexion
from PyQt5.QtGui import QIcon
from app.ui.WindowAddUser import AgregarUsuarioWindow
from app.ui.WindowEditUser import EditarUsuarioWindow

class GestionUsuariosWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestión de Usuarios")
        self.setFixedSize(600, 400)

        # Layout principal
        layout = QVBoxLayout()

        # Botón para agregar nuevo usuario
        self.btn_agregar = QPushButton("Agregar Usuario")
        self.btn_agregar.clicked.connect(self.agregar_usuario)
        layout.addWidget(self.btn_agregar)

        # Crear la tabla para mostrar los usuarios
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(7)  # 6 columnas: ID, Nombre, Apellido, Correo, Rol, Acción
        self.table_widget.setHorizontalHeaderLabels(["ID", "Nombre", "Apellido", "Correo", "Rol", "Modificar", "Eliminar"])
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)  # No permitir edición directa
        layout.addWidget(self.table_widget)

        # Cargar los usuarios desde la base de datos
        self.cargar_usuarios()

        # Establecer el layout
        self.setLayout(layout)

    def cargar_usuarios(self):
        """Carga los usuarios desde la base de datos y los muestra en la tabla."""
        try:
            conn = crear_conexion()
            cursor = conn.cursor()
            cursor.execute("SELECT id_usuario, nombre, apellido, correo, rol FROM usuario")
            usuarios = cursor.fetchall()
            conn.close()

            # Limpiar la tabla antes de agregar nuevos datos
            self.table_widget.setRowCount(0)

            # Agregar los usuarios a la tabla
            for usuario in usuarios:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)

                # Insertar los datos del usuario en las celdas
                for col, value in enumerate(usuario):
                    self.table_widget.setItem(row_position, col, QTableWidgetItem(str(value)))

                # Botones de Modificar
                btn_modificar = QPushButton("Modificar")
                btn_modificar.clicked.connect(lambda checked, id_usuario=usuario[0]: self.modificar_usuario(id_usuario))
                self.table_widget.setCellWidget(row_position, 5, btn_modificar)

                # Botones de Eliminar
                btn_eliminar = QPushButton("Eliminar")
                btn_eliminar.clicked.connect(lambda checked, id_usuario=usuario[0]: self.eliminar_usuario(id_usuario))
                self.table_widget.setCellWidget(row_position, 6, btn_eliminar)

            # Ajustar el tamaño de las columnas automáticamente según el contenido
            self.table_widget.resizeColumnsToContents()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al cargar los usuarios: {str(e)}")

    def agregar_usuario(self):
        """Abrir una ventana para agregar un nuevo usuario."""
        agregar_window = AgregarUsuarioWindow(self)
        agregar_window.exec_()  # Mostrar la ventana modal

    def modificar_usuario(self, id_usuario):
        """Abrir una ventana para modificar los datos del usuario seleccionado."""
        editar_window = EditarUsuarioWindow(id_usuario, self)
        editar_window.exec_()  # Mostrar la ventana modal

    def eliminar_usuario(self, id_usuario):
        """Eliminar un usuario de la base de datos."""
        confirm = QMessageBox.question(self, "Confirmar Eliminación", "¿Estás seguro de que deseas eliminar este usuario?", QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.Yes:
            try:
                conn = crear_conexion()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
                conn.commit()
                conn.close()

                QMessageBox.information(self, "Usuario Eliminado", "El usuario ha sido eliminado exitosamente.")
                self.cargar_usuarios()  # Recargar la lista de usuarios después de eliminar

            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al eliminar el usuario: {str(e)}")