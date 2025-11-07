CREATE TABLE usuarios(id int AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(255) NOT NULL,
email VARCHAR(255) NOT NULL UNIQUE,
senha VARCHAR(255) NOT NULL,
tipo ENUM('produtor', 'comprador', 'admin') NOT NULL,
localizacao VARCHAR(100) NULL);

CREATE TABLE produtos(id int AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(100) NOT NULL,
descricao VARCHAR(500) NULL,
preco DECIMAL(10,2) NOT NULL CHECK(preco>0),
quantidade int NOT NULL DEFAULT 0,
categoria ENUM('frutas', 'laticinios','graos') NOT NULL,
localizacao VARCHAR(255) NULL,
produtor_id int NOT NULL,
FOREIGN KEY (produtor_id) REFERENCES usuarios(id)
);
