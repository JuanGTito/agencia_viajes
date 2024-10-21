# Agencia de Viajes

Desarrollo de una aplicación para la gestión de reservas en una agencia de viajes.

## Descripción

Esta aplicación permite a los usuarios registrar turistas, gestionar destinos y procesar pagos de manera eficiente. La interfaz de usuario es amigable y está diseñada con PyQt5 para proporcionar una experiencia fluida.

## Características

- Registro de turistas con información personal y de contacto.
- Gestión de destinos disponibles con precios y fechas de viaje.
- Procesamiento de pagos mediante transferencia y pago en efectivo.
- Búsqueda de reservas mediante DNI o número de pasaporte.

## Tecnologías Utilizadas

- **Python**: Lenguaje de programación principal.
- **PyQt5**: Biblioteca para el desarrollo de la interfaz gráfica.
- **PyMySQL**: Conexión y manejo de la base de datos MySQL.
- **SQLAlchemy**: ORM para facilitar el manejo de la base de datos.
- **NumPy y Pandas**: Manipulación de datos.

## Estructura del Proyecto

agencia_viajes/ 
│ 
├── app/ 
│   ├── services/ 
│   │   └── database.py # Módulo para conexión a la base de datos. 
│   │   └── queries.py # Módulo para consultas a la base de datos. 
│   │   └── database_service.py # verificador de conexion. 
│   ├── models/ 
│   │   └── reserva.py # Lógica de reservas y acceso a datos. 
│   ├── ui/ 
│   │   ├── WindowDestinos.py # Interfaz para buscar reservas. 
│   │   └── WindowLogin.py # Pantalla principal de la aplicación.
│   │   └── WindowReserva.py # Interfaz para llenar formulario.  
│   │   └── WindowPrincipal.py # Interfaz principal.  
│   │   └── WindowBuscar.py # Interfaz principal.  
│   └── resources/ 
│       └── images/ # Imágenes de la aplicación. 
├── .env  
├── main.py # app principal. 
├── requirements.txt # Dependencias del proyecto. 
└── README.md # Documentación del proyecto.

## Instalación

1. Clona el repositorio:
   git clone https://github.com/tu_usuario/agencia_viajes.git
   cd agencia_viajes

2. Crea un entorno virtual:
    Copiar código
    python -m venv venv

3. Activa el entorno virtual:
    - En Windows:
        venv\Scripts\activate
    - En macOS y Linux:
        source venv/bin/activate

4. Instala las dependencias:
    pip install -r requirements.txt

5. Ejecuta la aplicación:
    python app/ui/main.py