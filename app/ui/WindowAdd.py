from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QComboBox, QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from app.services.database import crear_conexion


class AgregarDestinoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Destino")
        self.setFixedSize(400, 400)  # Aumenté el tamaño para incluir más campos
        
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

        # Tabla para agregar varios paquetes turísticos
        self.paquete_table = QTableWidget(self)
        self.paquete_table.setColumnCount(4)
        self.paquete_table.setHorizontalHeaderLabels(["Tipo de Paquete", "Hotel", "Precio Diario", "Eliminar"])
        self.paquete_table.setRowCount(0)

        # Botón para agregar un paquete
        self.btn_agregar_paquete = QPushButton("Agregar Paquete")
        self.btn_agregar_paquete.setFont(self.fontNegrita)
        self.btn_agregar_paquete.clicked.connect(self.agregar_paquete)

        # Botón para guardar el destino y los paquetes
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setFont(self.fontNegrita)
        self.btn_guardar.clicked.connect(self.guardar_destino)

        # Añadir formulario, tabla y botones al layout
        layout.addLayout(form_layout)
        layout.addWidget(self.paquete_table)
        layout.addWidget(self.btn_agregar_paquete)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

    def agregar_paquete(self):
        """Agrega una nueva fila para un paquete turístico en la tabla."""
        row_position = self.paquete_table.rowCount()
        self.paquete_table.insertRow(row_position)

        # Crear ComboBox para el tipo de paquete
        tipo_paquete = QComboBox(self)
        tipo_paquete.addItems(['Individual', 'Familiar'])
        self.paquete_table.setCellWidget(row_position, 0, tipo_paquete)

        # Crear ComboBox para el hotel
        hotel = QComboBox(self)
        hotel.addItems(['Si', 'No'])
        self.paquete_table.setCellWidget(row_position, 1, hotel)

        # Crear campo para el precio diario
        precio_diario = QLineEdit(self)
        self.paquete_table.setCellWidget(row_position, 2, precio_diario)

        # Crear botón para eliminar la fila
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(lambda: self.eliminar_paquete(row_position))
        self.paquete_table.setCellWidget(row_position, 3, btn_eliminar)

    def eliminar_paquete(self, row):
        """Elimina una fila de la tabla de paquetes."""
        self.paquete_table.removeRow(row)

    def guardar_destino(self):
        """Lógica para guardar un nuevo destino y sus paquetes turísticos en la base de datos."""
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

                # Obtener el ID del destino recién insertado
                id_destino = cursor.lastrowid

                # Insertar los paquetes turísticos asociados al destino
                for row in range(self.paquete_table.rowCount()):
                    tipo_paquete = self.paquete_table.cellWidget(row, 0).currentText()
                    hotel = self.paquete_table.cellWidget(row, 1).currentText()
                    precio_diario = self.paquete_table.cellWidget(row, 2).text()

                    if precio_diario:  # Solo insertar si el precio diario no está vacío
                        cursor.execute("""
                            INSERT INTO paquete_turistico (id_cat_destino, tipo_paquete, hotel, precio_diario)
                            VALUES (%s, %s, %s, %s)
                        """, (id_destino, tipo_paquete, hotel, precio_diario))
                        conn.commit()

                conn.close()

                QMessageBox.information(self, "Destino y Paquetes Agregados", "El destino y sus paquetes turísticos han sido agregados exitosamente.")
                self.accept()  # Cerrar el modal al agregar el destino y los paquetes
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al agregar el destino y los paquetes: {str(e)}")
        else:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete todos los campos.")
