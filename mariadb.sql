CREATE DATABASE openproxy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE openproxy;

CREATE TABLE proxy (
    id BIGINT UNSIGNED AUTO_INCREMENT,
    address VARCHAR(50) NOT NULL UNIQUE,
    ip_type TINYINT NOT NULL DEFAULT 4,
    methodes TEXT NOT NULL,
    commentaire VARCHAR(100) NOT NULL,
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
    commentaire TEXT,
    add_date DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY(id)
);

DELIMITER //
CREATE PROCEDURE add_proxy (IN address VARCHAR(50), IN ip_type TINYINT, IN methodes VARCHAR(100), IN scan_date BIGINT, IN commentaire TEXT)
BEGIN
    DECLARE var_scan_date DATETIME;
    SET var_scan_date = FROM_UNIXTIME(scan_date);
    INSERT INTO proxy (address, ip_type, methodes, commentaire, add_date, update_date) VALUES (address, ip_type, methodes, commentaire, var_scan_date, var_scan_date)
    ON DUPLICATE KEY UPDATE id=id, update_date=var_scan_date, commentaire=commentaire, methodes=methodes, update_count=update_count+1;
END; //

CREATE PROCEDURE add_data (IN data LONGBLOB, IN filename TEXT, IN commentaire TEXT)
BEGIN
    INSERT INTO data (data, filename, commentaire) VALUES (data, filename, commentaire);
END; //
DELIMITER ;