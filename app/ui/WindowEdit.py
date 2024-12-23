from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from app.services.database import crear_conexion

class EditarDestinoDialog(QDialog):
    def __init__(self, nombre, descripcion, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Destino")
        self.setFixedSize(400, 300)

        self.fontNegrita = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        layout = QVBoxLayout()

        # Formulario de entrada
        form_layout = QFormLayout()

        # Campo para el nombre del destino
        self.nombre_destino_input = QLineEdit(self)
        self.nombre_destino_input.setText(nombre)
        form_layout.addRow(QLabel("Nombre del Destino:"), self.nombre_destino_input)

        # Campo para la descripción
        self.descripcion_input = QTextEdit(self)
        self.descripcion_input.setText(descripcion)
        form_layout.addRow(QLabel("Descripción:"), self.descripcion_input)

        # Botón para guardar
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.setFont(self.fontNegrita)
        self.btn_guardar.clicked.connect(self.guardar_cambios)

        # Añadir formulario y botón al layout
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

    def guardar_cambios(self):
        """Lógica para guardar los cambios de un destino en la base de datos."""
        nuevo_nombre = self.nombre_destino_input.text()
        nueva_descripcion = self.descripcion_input.toPlainText()

        if nuevo_nombre and nueva_descripcion:
            try:
                # Usar la función `crear_conexion` para conectarse a la base de datos
                conn = crear_conexion()
                cursor = conn.cursor()

                # Actualizar el destino en la base de datos
                cursor.execute(
                    "UPDATE catalogo_destino SET descripcion = %s WHERE destino = %s",
                    (nueva_descripcion, nuevo_nombre)
                )
                conn.commit()
                conn.close()

                QMessageBox.information(self, "Destino Editado", "El destino ha sido actualizado exitosamente.")
                self.accept()  # Cerrar el modal al guardar los cambios
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al editar el destino: {str(e)}")
        else:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete todos los campos.")