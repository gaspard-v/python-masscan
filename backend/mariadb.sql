CREATE DATABASE IF NOT EXISTS openproxy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
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
    token_state VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY(id)
);

INSERT INTO token_state_t (token_state) VALUES ("valid"), ("expired"), ("deleted"), ("invalid"), ("halted");

CREATE TABLE permission_t (
    id SERIAL,
    permission VARCHAR(30) NOT NULL UNIQUE,
    PRIMARY KEY(id)
);

INSERT INTO permission_t (permission) VALUES ("proxy_read"), ("proxy_create"), ("proxy_update"), ("proxy_delete"), ("proxy_all"), 
                                             ("token_read"), ("token_create"), ("token_update"), ("token_delete"), ("token_all"),
                                             ("all_all");

CREATE TABLE token_t (
    id SERIAL,
    token_state_fk BIGINT UNSIGNED NOT NULL,
    token CHAR(10) NOT NULL UNIQUE,
    creation_date DATETIME NOT NULL DEFAULT NOW(),
    modifiation_date DATETIME NOT NULL DEFAULT NOW(),
    FOREIGN KEY (token_state_fk) REFERENCES token_state_t(id) ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY(id)
);

CREATE TABLE join_token_permission (
    token_fk BIGINT UNSIGNED,
    permission_fk BIGINT UNSIGNED,
    FOREIGN KEY (token_fk) REFERENCES token_t(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (permission_fk) REFERENCES permission_t(id) ON UPDATE CASCADE ON DELETE CASCADE,
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

CREATE PROCEDURE add_token (IN in_token CHAR(10), IN in_token_state VARCHAR(30), IN in_date BIGINT UNSIGNED)
BEGIN
    DECLARE var_token_state_id BIGINT UNSIGNED;
    DECLARE var_date DATETIME;

    SET var_date = FROM_UNIXTIME(in_date);
    SELECT id INTO var_token_state_id FROM token_state_t WHERE token_state = in_token_state;

    INSERT INTO token_t (token, token_state_fk, creation_date, modifiation_date) VALUES (in_token, var_token_state_id, var_date, var_date)
    ON DUPLICATE KEY UPDATE id=id, token_state_fk=var_token_state_id, modifiation_date=var_date;
END; //

CREATE PROCEDURE add_token_permission (IN in_token CHAR(10), IN in_permission VARCHAR(30))
BEGIN
    DECLARE var_permission_id BIGINT UNSIGNED;
    DECLARE var_token_id BIGINT UNSIGNED;

    SELECT id INTO var_permission_id FROM permission_t WHERE permission = in_permission;
    SELECT id INTO var_token_id FROM token_t WHERE token = in_token;

    INSERT INTO join_token_permission(token_fk, permission_fk) VALUES (var_token_id, var_permission_id);
    UPDATE token_t SET modifiation_date = NOW() WHERE id = var_token_id;
END; //

CREATE PROCEDURE delete_token_permission (IN in_token CHAR(10), in_permission VARCHAR(10))
BEGIN
    DECLARE var_permission_id BIGINT UNSIGNED;
    DECLARE var_token_id BIGINT UNSIGNED;

    SELECT id INTO var_permission_id FROM permission_t WHERE permission = in_permission;
    SELECT id INTO var_token_id FROM token_t WHERE token = in_token;
    DELETE FROM join_token_permission WHERE token_fk=var_token_id AND permission_fk=var_permission_id;
END; //

CREATE PROCEDURE get_token_permission (IN in_token CHAR(10))
BEGIN
    SELECT permission_t.permission FROM permission_t 
    INNER JOIN join_token_permission ON join_token_permission.permission_fk = permission_t.id 
    INNER JOIN token_t ON join_token_permission.token_fk = token_t.id AND token_t.token = in_token;

END; //
DELIMITER ;