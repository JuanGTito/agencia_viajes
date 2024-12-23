import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog
from app.ui.WindowPrincipal import VentanaPrincipal
from app.ui.WindowLogin import VentanaLogin  # Importar la nueva ventana de login
from app.services.database_service import verificar_conexion_bd  # Importar la función para verificar la base de datos

def main():
    """Función principal que inicializa la aplicación."""
    app = QApplication(sys.argv)

    # Verificar la conexión a la base de datos antes de iniciar la interfaz gráfica
    if not verificar_conexion_bd():
        # Mostrar un mensaje de error si no se pudo conectar a la base de datos
        QMessageBox.critical(None, "Error de Conexión", "No se pudo conectar a la base de datos.")
        sys.exit(1)  # Salir con error

    # Mostrar la ventana de login
    login = VentanaLogin()
    if login.exec_() == QDialog.Accepted:
        # Si el login es exitoso, mostrar la ventana principal
        usuario = login.usuario
        ventana = VentanaPrincipal(usuario)
        ventana.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)  # Si no se aceptó el login, salir de la aplicación

if __name__ == '__main__':
    main()