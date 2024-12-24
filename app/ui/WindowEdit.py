from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt  # Importar Qt
from app.services.database import crear_conexion

class EditarDestinoDialog(QDialog):
    def __init__(self, nombre, descripcion, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Destino")
        self.setFixedSize(600, 400)  # Aumenté el tamaño para incluir los paquetes
        
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

        # Tabla para editar los paquetes turísticos
        self.paquete_table = QTableWidget(self)
        self.paquete_table.setColumnCount(4)
        self.paquete_table.setHorizontalHeaderLabels(["Tipo de Paquete", "Hotel", "Precio Diario", "Eliminar"])
        self.paquete_table.setRowCount(0)

        # Botón para agregar un paquete
        self.btn_agregar_paquete = QPushButton("Agregar Paquete")
        self.btn_agregar_paquete.setFont(self.fontNegrita)
        self.btn_agregar_paquete.clicked.connect(self.agregar_paquete)

        # Botón para guardar los cambios
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.setFont(self.fontNegrita)
        self.btn_guardar.clicked.connect(self.guardar_cambios)

        # Añadir formulario, tabla y botones al layout
        layout.addLayout(form_layout)
        layout.addWidget(self.paquete_table)
        layout.addWidget(self.btn_agregar_paquete)
        layout.addWidget(self.btn_guardar)

        self.setLayout(layout)

        # Cargar los paquetes del destino
        self.cargar_paquetes(nombre)

    def cargar_paquetes(self, destino):
        """Carga los paquetes turísticos existentes para un destino en la tabla."""
        try:
            # Usar la función `crear_conexion` para conectarse a la base de datos
            conn = crear_conexion()
            cursor = conn.cursor()

            # Obtener los paquetes turísticos asociados al destino
            cursor.execute("""
                SELECT tipo_paquete, hotel, precio_diario, id_paquete
                FROM paquete_turistico
                WHERE id_cat_destino = (SELECT id_destino FROM catalogo_destino WHERE destino = %s)
            """, (destino,))
            paquetes = cursor.fetchall()

            # Insertar los paquetes en la tabla
            for paquete in paquetes:
                row_position = self.paquete_table.rowCount()
                self.paquete_table.insertRow(row_position)

                # Tipo de paquete
                tipo_paquete = QComboBox(self)
                tipo_paquete.addItems(['Individual', 'Familiar'])
                tipo_paquete.setCurrentText(paquete[0])
                self.paquete_table.setCellWidget(row_position, 0, tipo_paquete)

                # Hotel
                hotel = QComboBox(self)
                hotel.addItems(['Si', 'No'])
                hotel.setCurrentText(paquete[1])
                self.paquete_table.setCellWidget(row_position, 1, hotel)

                # Precio diario
                precio_diario = QLineEdit(self)
                precio_diario.setText(str(paquete[2]))
                self.paquete_table.setCellWidget(row_position, 2, precio_diario)

                # ID del paquete (oculto)
                id_paquete_item = QTableWidgetItem(str(paquete[3]))
                id_paquete_item.setFlags(id_paquete_item.flags() & ~Qt.ItemIsEditable)  # Usar Qt importado
                self.paquete_table.setItem(row_position, 3, id_paquete_item)

                # Botón de eliminar en la columna "Eliminar"
                btn_eliminar = QPushButton("Eliminar")
                btn_eliminar.clicked.connect(lambda checked, row=row_position: self.eliminar_paquete(row))
                self.paquete_table.setCellWidget(row_position, 3, btn_eliminar)

            conn.close()

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al cargar los paquetes: {str(e)}")

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
        btn_eliminar.clicked.connect(lambda checked, row=row_position: self.eliminar_paquete(row))
        self.paquete_table.setCellWidget(row_position, 3, btn_eliminar)

    def eliminar_paquete(self, row):
        """Elimina una fila de la tabla de paquetes y también de la base de datos."""
        # Obtener el ID del paquete
        id_paquete_item = self.paquete_table.item(row, 3)
        if id_paquete_item:
            id_paquete = id_paquete_item.text()

            try:
                # Usar la función `crear_conexion` para conectarse a la base de datos
                conn = crear_conexion()
                cursor = conn.cursor()

                # Eliminar el paquete de la base de datos
                cursor.execute("DELETE FROM paquete_turistico WHERE id_paquete = %s", (id_paquete,))
                conn.commit()
                conn.close()

                # Eliminar la fila de la tabla
                self.paquete_table.removeRow(row)

                QMessageBox.information(self, "Paquete Eliminado", "El paquete ha sido eliminado exitosamente.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al eliminar el paquete: {str(e)}")
        else:
            QMessageBox.warning(self, "Error", "No se puede eliminar el paquete, no se encontró un ID válido.")

    def guardar_cambios(self):
        """Lógica para guardar los cambios de un destino y sus paquetes turísticos en la base de datos."""
        nuevo_nombre = self.nombre_destino_input.text()
        nueva_descripcion = self.descripcion_input.toPlainText()
    
        if nuevo_nombre and nueva_descripcion:
            try:
                # Usar la función `crear_conexion` para conectarse a la base de datos
                conn = crear_conexion()
                cursor = conn.cursor()
    
                # Actualizar el destino en la base de datos
                cursor.execute(
                    "UPDATE catalogo_destino SET destino = %s, descripcion = %s WHERE destino = %s",
                    (nuevo_nombre, nueva_descripcion, nuevo_nombre)
                )
                conn.commit()
    
                # Obtener el id_destino para asociar los paquetes
                cursor.execute("SELECT id_destino FROM catalogo_destino WHERE destino = %s", (nuevo_nombre,))
                id_destino = cursor.fetchone()[0]
    
                # Actualizar o insertar los paquetes turísticos
                for row in range(self.paquete_table.rowCount()):
                    tipo_paquete_widget = self.paquete_table.cellWidget(row, 0)
                    hotel_widget = self.paquete_table.cellWidget(row, 1)
                    precio_diario_widget = self.paquete_table.cellWidget(row, 2)
    
                    # Verificar que los widgets existen y obtener sus valores
                    if tipo_paquete_widget and hotel_widget and precio_diario_widget:
                        tipo_paquete = tipo_paquete_widget.currentText()
                        hotel = hotel_widget.currentText()
                        precio_diario = precio_diario_widget.text()  # Asegúrate de que sea un QLineEdit
    
                        if precio_diario:  # Solo insertar o actualizar si el precio diario no está vacío
                            # Comprobar si ya existe un paquete con el mismo tipo y hotel
                            cursor.execute("""
                                SELECT id_paquete FROM paquete_turistico
                                WHERE id_cat_destino = %s AND tipo_paquete = %s AND hotel = %s
                            """, (id_destino, tipo_paquete, hotel))
                            existing_package = cursor.fetchone()
    
                            if existing_package:  # Si el paquete ya existe, actualizarlo
                                id_paquete = existing_package[0]
                                cursor.execute("""
                                    UPDATE paquete_turistico
                                    SET tipo_paquete = %s, hotel = %s, precio_diario = %s
                                    WHERE id_paquete = %s
                                """, (tipo_paquete, hotel, precio_diario, id_paquete))
                            else:  # Si no existe, insertarlo como un nuevo paquete
                                cursor.execute("""
                                    INSERT INTO paquete_turistico (id_cat_destino, tipo_paquete, hotel, precio_diario)
                                    VALUES (%s, %s, %s, %s)
                                """, (id_destino, tipo_paquete, hotel, precio_diario))
    
                conn.commit()
                conn.close()
    
                QMessageBox.information(self, "Destino y Paquetes Editados", "El destino y sus paquetes turísticos han sido actualizados exitosamente.")
                self.accept()  # Cerrar el modal al guardar los cambios
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error al editar el destino y los paquetes: {str(e)}")
        else:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete todos los campos.")
    