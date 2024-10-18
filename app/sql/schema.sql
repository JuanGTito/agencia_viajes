-- Create the database
CREATE DATABASE IF NOT EXISTS agencia_viajes;
USE agencia_viajes;

-- Create the Turistas table
CREATE TABLE IF NOT EXISTS Turistas (
    ID_Turista INT PRIMARY KEY AUTO_INCREMENT,
    Nombre_Completo VARCHAR(150),
    Fecha_de_nacimiento DATE,
    Genero ENUM('Masculino', 'Femenino', 'Otro'),
    Telefono VARCHAR(15),
    Email VARCHAR(100),
    Numero_de_pasaporte VARCHAR(50),
    Nacionalidad VARCHAR(50)
);

-- Create the Destinos table
CREATE TABLE IF NOT EXISTS Destinos (
    ID_Destino INT PRIMARY KEY AUTO_INCREMENT,
    ID_Turista INT,
    Destino_principal ENUM('Playa del Carmen', 'Cusco', 'Buenos Aires', 'Barcelona', 'Cancún'),
    Precio DECIMAL(10, 2),
    Fecha_de_salida DATE,
    Fecha_de_regreso DATE,
    FOREIGN KEY (ID_Turista) REFERENCES Turistas(ID_Turista)
);

-- Create the Pagos table
CREATE TABLE IF NOT EXISTS Pagos (
    ID_Pago INT PRIMARY KEY AUTO_INCREMENT,
    ID_Turista INT,
    Metodo_de_pago ENUM('Transferencia', 'Pago en efectivo'),
    Monto DECIMAL(10, 2),
    Numero_de_referencia VARCHAR(50) NULL,
    FOREIGN KEY (ID_Turista) REFERENCES Turistas(ID_Turista)
);