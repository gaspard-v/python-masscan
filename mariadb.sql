CREATE DATABASE openproxy CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE openproxy;

CREATE TABLE proxy (
    id BIGINT UNSIGNED AUTO_INCREMENT,
    adresse VARCHAR(50) NOT NULL UNIQUE,
    ip_type TINYINT NOT NULL DEFAULT 4,
    add_date DATETIME NOT NULL DEFAULT NOW(),
    update_date DATETIME NOT NULL DEFAULT NOW(),
    update_count INT UNSIGNED NOT NULL DEFAULT 0,
    CONSTRAINT is_ip_type CHECK (ip_type = 4 OR ip_type = 6),
    PRIMARY KEY(id)
);