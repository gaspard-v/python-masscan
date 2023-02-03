CREATE DATABASE openproxy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE openproxy;

CREATE TABLE proxy (
    id BIGINT UNSIGNED AUTO_INCREMENT,
    address VARCHAR(50) NOT NULL,
    port INT UNSIGNED NOT NULL CHECK (port > 0 AND port < 65356),
    ip_type TINYINT NOT NULL DEFAULT 4,
    methodes TEXT NOT NULL,
    commentaire TEXT,
    add_date DATETIME NOT NULL DEFAULT NOW(),
    update_date DATETIME NOT NULL DEFAULT NOW(),
    update_count INT UNSIGNED NOT NULL DEFAULT 0,
    CONSTRAINT is_ip_type CHECK (ip_type = 4 OR ip_type = 6),
    UNIQUE INDEX ux_address_port_proxy (address, port),
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

CREATE TABLE token_state_t (
    id SERIAL,
    token_state VARCHAR(20) NOT NULL UNIQUE DEFAULT "valid",
    PRIMARY KEY(id)
);

INSERT INTO token_state_t (token_state) VALUES "valid, expired", "deleted", "invalid", "halted";

CREATE TABLE permission_t (
    id SERIAL,
    permission VARCHAR(20) NOT NULL UNIQUE DEFAULT "read",
    PRIMARY KEY(id)
);

INSERT INTO permission_t (permission) VALUES "proxy_read", "proxy_create", "proxy_update", "proxy_delete", "proxy_all", 
                                             "token_read", "token_create", "token_update", "token_delete", "token_all",
                                             "all_all";

CREATE TABLE token (
    id SERIAL,
    token_state_fk SERIAL NOT NULL,
    token CHAR(10) NOT NULL UNIQUE,
    creation_date DATETIME NOT NULL DEFAULT NOW(),
    modifiation_date DATETIME NOT NULL DEFAULT NOW(),
    FOREIGN KEY (token_state) REFERENCE token_state_t(id) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY(id)
);

CREATE TABLE join_token_permission (
    token_fk SERIAL,
    permission_fk SERIAL,
    FOREIGN KEY (token_fk) REFERENCE token(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (permission_fk) REFERENCE permission_t(id) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY(token_fk, permission_fk)
);

DELIMITER //
CREATE PROCEDURE add_proxy (IN in_address VARCHAR(50), IN in_port INT UNSIGNED, IN in_ip_type TINYINT, IN in_methodes VARCHAR(100), IN in_scan_date BIGINT UNSIGNED, IN in_commentaire TEXT)
BEGIN
    DECLARE var_scan_date DATETIME;
    SET var_scan_date = FROM_UNIXTIME(in_scan_date);
    INSERT INTO proxy (address, port, ip_type, methodes, commentaire, add_date, update_date) VALUES (in_address, in_port, in_ip_type, in_methodes, in_commentaire, var_scan_date, var_scan_date)
    ON DUPLICATE KEY UPDATE id=id, port=in_port, update_date=var_scan_date, commentaire=in_commentaire, methodes=in_methodes, update_count=update_count+1;
END; //

CREATE PROCEDURE add_data (IN in_data LONGBLOB, IN in_filename TEXT, IN in_commentaire TEXT)
BEGIN
    INSERT INTO data (data, filename, commentaire) VALUES (in_data, in_filename, in_commentaire);
END; //
DELIMITER ;