import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from app.ui.ventana_principal import VentanaPrincipal  # Asegúrate de que este archivo exista
from app.services.database_service import verificar_conexion_bd  # Importar la nueva función

def main():
    """Función principal que inicializa la aplicación."""
    app = QApplication(sys.argv)

    # Verificar la conexión a la base de datos antes de iniciar la interfaz gráfica
    if verificar_conexion_bd():
        ventana = VentanaPrincipal()
        ventana.show()  # Mostrar la ventana principal
        sys.exit(app.exec_())  # Ejecutar la aplicación
    else:
        # Mostrar un mensaje de error si no se pudo conectar a la base de datos
        QMessageBox.critical(None, "Error de Conexión", "No se pudo conectar a la base de datos.")
        sys.exit(1)  # Salir con error

if __name__ == '__main__':
    main()
