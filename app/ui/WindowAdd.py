from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from app.services.database import crear_conexion


class AgregarDestinoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Destino")
        self.setFixedSize(400, 300)
        
        self.fontNegrita = QFont("Arial", 14, QFont.Bold)

        # Layout principal
        layout = QVBoxLayout()

        # Formulario de entrada
        form_layout = QFormLayout()

        # Campo para el nombre del destino
        self.nombre_destino_input = QLineEdit(self)
        form_layout.addRow(QLabel("Nombre del Destino:"), self.nombre_destino_input)

        # Campo para la descripción
        self.descripcion_input = QTextEdit(self)
        form_layout.addRow(QLabel("Descripción:"), self.descripcion_input)

        # Botón para guardar
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setFont(self.fontNegrita)
        self.btn_guardar.clicked.connect(self.guardar_destino)
        
        # Añadir formulario y botón al layout
        layout.addLayout(form_layout)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

    def guardar_destino(self):
        """Lógica para guardar un nuevo destino en la base de datos."""
        destino = self.nombre_destino_input.text()
        descripcion = self.descripcion_input.toPlainText()

        if destino and descripcion:
            try:
                # Usar la función `crear_conexion` para conectarse a la base de datos
                conn = crear_conexion()
                cursor = conn.cursor()

                # Insertar destino en la base de datos
                cursor.execute("INSERT INTO catalogo_destino (destino, descripcion) VALUES (%s, %s)", (destino, descripcion))
                conn.commit()
                conn.close()

                QMessageBox.information(self, "Destino Agregado", "El destino ha sido agregado exitosamente.")
                self.accept()  # Cerrar el modal al agregar el destino
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al agregar el destino: {str(e)}")
        else:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete todos los campos.")

