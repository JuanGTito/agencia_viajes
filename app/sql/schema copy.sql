-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS agencia_viajes;
USE agencia_viajes;

-- Tabla de turistas
CREATE TABLE IF NOT EXISTS turista (
    id_turista INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fnac DATE NOT NULL,
    genero ENUM('Masculino', 'Femenino') NOT NULL,
    telefono VARCHAR(15),
    email VARCHAR(100) NOT NULL UNIQUE,
    tipo_doc ENUM('DNI', 'Pasaporte') NOT NULL,
    num_doc VARCHAR(50) NOT NULL UNIQUE,
    nacionalidad VARCHAR(50) NOT NULL
);

-- Tabla de catálogo de destinos (sin precios)
CREATE TABLE IF NOT EXISTS catalogo_destino (
    id_destino INT PRIMARY KEY AUTO_INCREMENT,
    destino VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla de paquetes turísticos (con precios específicos)
CREATE TABLE IF NOT EXISTS paquete_turistico (
    id_paquete INT PRIMARY KEY AUTO_INCREMENT,
    id_cat_destino INT NOT NULL,
    tipo_paquete ENUM('Individual', 'Familiar') NOT NULL,
    hotel ENUM('Si', 'No') NOT NULL,
    precio_diario DECIMAL(10, 2) NOT NULL, -- Precio por día
    FOREIGN KEY (id_cat_destino) REFERENCES catalogo_destino(id_destino) ON DELETE CASCADE
);

-- Tabla de reservas (con duración en días y fecha de reserva)
CREATE TABLE IF NOT EXISTS reserva (
    id_reserva INT PRIMARY KEY AUTO_INCREMENT,
    id_turista INT NOT NULL,
    id_paquete INT NOT NULL,
    f_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Fecha de creación de la reserva
    f_salida DATE NOT NULL,
    duracion_dias INT NOT NULL, -- Cantidad de días del paquete
    FOREIGN KEY (id_turista) REFERENCES turista(id_turista) ON DELETE CASCADE,
    FOREIGN KEY (id_paquete) REFERENCES paquete_turistico(id_paquete) ON DELETE CASCADE
);

-- Tabla de pagos
CREATE TABLE IF NOT EXISTS pago (
    id_pago INT PRIMARY KEY AUTO_INCREMENT,
    id_turista INT NOT NULL,
    id_reserva INT NOT NULL,
    metodo ENUM('Transferencia', 'Efectivo') NOT NULL,
    monto_total DECIMAL(10, 2) NOT NULL, -- Total calculado al generar la reserva
    ref_num VARCHAR(50),
    FOREIGN KEY (id_turista) REFERENCES turista(id_turista) ON DELETE CASCADE,
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva) ON DELETE CASCADE
);

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    user_nombre VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    rol ENUM('Usuario', 'Admin') DEFAULT 'Usuario',
    f_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar destinos en catalogo_destino
INSERT INTO catalogo_destino (destino, descripcion)
VALUES 
('Machu Picchu', 'Ciudadela Inca situada en la cima de la montaña Machu Picchu.'),
('Cusco', 'Capital histórica del Imperio Inca.'),
('Lago Titicaca', 'Lago navegable más alto del mundo, entre Perú y Bolivia.'),
('Nazca', 'Ciudad famosa por las líneas de Nazca.'),
('Paracas', 'Lugar con playas y fauna marina en la costa sur del Perú.'),
('Arequipa', 'La Ciudad Blanca con arquitectura colonial.'),
('Iquitos', 'Ciudad en la Amazonía peruana, accesible solo por vía fluvial o aérea.'),
('Lima', 'Capital del Perú, conocida por su gastronomía y arquitectura.'),
('Cañón del Colca', 'Uno de los cañones más profundos del mundo, hogar de cóndores.'),
('Huacachina', 'Oasis en el desierto, cerca de la ciudad de Ica.');

-- Insertar paquetes turísticos
INSERT INTO paquete_turistico (id_cat_destino, tipo_paquete, hotel, precio_diario)
VALUES 
-- Machu Picchu
(1, 'Individual', 'No', 200.00),
(1, 'Individual', 'Si', 300.00),
(1, 'Familiar', 'Si', 800.00),

-- Cusco
(2, 'Individual', 'No', 50.00),
(2, 'Individual', 'Si', 100.00),
(2, 'Familiar', 'Si', 200.00),

-- Lago Titicaca
(3, 'Individual', 'No', 80.00),
(3, 'Individual', 'Si', 150.00),
(3, 'Familiar', 'Si', 280.00),

-- Nazca
(4, 'Individual', 'No', 150.00),
(4, 'Individual', 'Si', 200.00),
(4, 'Familiar', 'Si', 350.00),

-- Paracas
(5, 'Individual', 'No', 60.00),
(5, 'Individual', 'Si', 120.00),
(5, 'Familiar', 'Si', 220.00),

-- Arequipa
(6, 'Individual', 'No', 40.00),
(6, 'Individual', 'Si', 80.00),
(6, 'Familiar', 'Si', 150.00),

-- Iquitos
(7, 'Individual', 'No', 120.00),
(7, 'Individual', 'Si', 180.00),
(7, 'Familiar', 'Si', 300.00),

-- Lima
(8, 'Individual', 'No', 50.00),
(8, 'Individual', 'Si', 90.00),
(8, 'Familiar', 'Si', 160.00),

-- Cañón del Colca
(9, 'Individual', 'No', 70.00),
(9, 'Individual', 'Si', 130.00),
(9, 'Familiar', 'Si', 250.00),

-- Huacachina
(10, 'Individual', 'No', 50.00),
(10, 'Individual', 'Si', 100.00),
(10, 'Familiar', 'Si', 180.00);

