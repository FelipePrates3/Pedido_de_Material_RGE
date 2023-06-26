--   mysql -u root -p  


CREATE DATABASE database_RGE;

USE database_RGE;

CREATE TABLE Pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    ure VARCHAR(255) NOT NULL,
    equipe VARCHAR(255) NOT NULL,
    material VARCHAR(255) NOT NULL,
    quantidade VARCHAR(255) NOT NULL,
    unidade VARCHAR(255) NOT NULL,
    justificativa TEXT NOT NULL
);

