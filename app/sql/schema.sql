-- Crear base de datos si no existe
CREATE DATABASE IF NOT EXISTS agencia_viajes;
USE agencia_viajes;

-- Crear la tabla turistas
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

-- Crear la tabla catalogo_destino
CREATE TABLE IF NOT EXISTS catalogo_destino (
    id_destino INT PRIMARY KEY AUTO_INCREMENT,
    destino VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL
);

-- Crear la tabla destinos (conectada a catalogo_destino)
CREATE TABLE IF NOT EXISTS destino (
    id_viaje INT PRIMARY KEY AUTO_INCREMENT,
    id_turista INT NOT NULL,
    id_cat_destino INT NOT NULL,
    f_salida DATE NOT NULL,
    f_regreso DATE NOT NULL,
    FOREIGN KEY (id_turista) REFERENCES turista(id_turista) ON DELETE CASCADE,
    FOREIGN KEY (id_cat_destino) REFERENCES catalogo_destino(id_destino) ON DELETE CASCADE
);

-- Crear la tabla pagos
CREATE TABLE IF NOT EXISTS pago (
    id_pago INT PRIMARY KEY AUTO_INCREMENT,
    id_turista INT NOT NULL,
    metodo ENUM('Transferencia', 'Efectivo') NOT NULL,
    monto DECIMAL(10, 2) NOT NULL,
    ref_num VARCHAR(50),
    FOREIGN KEY (id_turista) REFERENCES turista(id_turista) ON DELETE CASCADE
);

-- Crear la tabla usuarios para login
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    user_nombre VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    rol ENUM('Usuario', 'Admin') DEFAULT 'Usuario',
    f_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar datos iniciales en catalogo_destino
INSERT INTO catalogo_destino (destino, precio)
VALUES 
('Playa del Carmen', 500.00),
('Cusco', 600.00),
('Buenos Aires', 700.00),
('Barcelona', 800.00),
('Cancún', 550.00);

-- Insertar datos iniciales en turista
INSERT INTO turista (nombre, apellido, fnac, genero, telefono, email, tipo_doc, num_doc, nacionalidad)
VALUES ('Juan', 'Pérez', '1990-05-15', 'Masculino', '123456789', 'juan.perez@email.com', 'Pasaporte', 'A12345678', 'Peruana');

-- Insertar datos iniciales en destino
INSERT INTO destino (id_turista, id_cat_destino, f_salida, f_regreso)
VALUES (1, 5, '2024-12-01', '2024-12-15');

-- Insertar datos iniciales en pagos
INSERT INTO pago (id_turista, metodo, monto, ref_num)
VALUES (1, 'Transferencia', 550.00, 'REF123456');

-- Insertar usuario inicial
INSERT INTO usuario (user_nombre, contrasena, email, rol)
VALUES ('admin', 'hashed_password_here', 'admin@example.com', 'Admin');
