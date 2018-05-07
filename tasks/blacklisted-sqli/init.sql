CREATE USER 'dbuser'@'localhost' IDENTIFIED BY 'zJ2plyhR9';
GRANT SELECT ON cpanel.* TO 'dbuser'@'localhost';
FLUSH PRIVILEGES;

CREATE DATABASE cpanel;

USE cpanel;

CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT,
  login VARCHAR(30) NOT NULL,
  password VARCHAR(32) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO users VALUES (1, 'admin', 'f44ed65148ee6134c8c4360e17b0a45a');