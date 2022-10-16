CREATE DATABASE openproxy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE openproxy;

CREATE TABLE proxy (
    id BIGINT UNSIGNED AUTO_INCREMENT,
    address VARCHAR(50) NOT NULL UNIQUE,
    ip_type TINYINT NOT NULL DEFAULT 4,
    add_date DATETIME NOT NULL DEFAULT NOW(),
    update_date DATETIME NOT NULL DEFAULT NOW(),
    update_count INT UNSIGNED NOT NULL DEFAULT 0,
    CONSTRAINT is_ip_type CHECK (ip_type = 4 OR ip_type = 6),
    PRIMARY KEY(id)
);

CREATE TABLE data (
    id BIGINT UNSIGNED AUTO_INCREMENT,
    data LONGBLOB,
    filename TEXT NOT NULL,
    add_date DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY(id)
);

DELIMITER //
CREATE PROCEDURE add_proxy (IN address VARCHAR(50), IN ip_type TINYINT)
BEGIN
    INSERT INTO proxy (address, ip_type) VALUES (address, ip_type)
    ON DUPLICATE KEY UPDATE id=id, update_date=NOW(), update_count=update_count+1;
END; //

CREATE PROCEDURE add_data (IN data LONGBLOB, IN filename TEXT)
BEGIN
    INSERT INTO data (data, filename) VALUES (data, filename);
END; //
DELIMITER ;