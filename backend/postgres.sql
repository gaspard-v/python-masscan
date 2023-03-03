CREATE DATABASE openproxy OWNER openproxy ENCODING 'UTF8' LC_COLLATE = 'en_US.UTF-8'  LC_CTYPE = 'en_US.utf8';

\c openproxy

CREATE TYPE token_state_t AS ENUM('valid', 'expired', 'deleted', 'invalid', 'halted');
CREATE TYPE permission_t AS ENUM('proxy_read', 'proxy_create', 'proxy_update', 'proxy_delete', 'proxy_all',
                                 'token_read', 'token_create', 'token_update', 'token_delete', 'token_all',
                                 'all_all');

CREATE TABLE proxy (
    id BIGSERIAL,
    address INET NOT NULL,
    port INT NOT NULL CHECK (port > 0 AND port < 65356),
    methodes TEXT NOT NULL,
    commentaire TEXT,
    add_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    update_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    update_count INT NOT NULL DEFAULT 0,
    UNIQUE (address, port),
    PRIMARY KEY(id)
);

CREATE TABLE data (
    id BIGSERIAL,
    data BYTEA,
    filename TEXT NOT NULL,
    commentaire TEXT,
    add_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY(id)
);

CREATE TABLE token_t (
    id BIGSERIAL,
    token_state token_state_t NOT NULL DEFAULT 'valid',
    token_permission permission_t ARRAY NOT NULL,
    token_data CHAR(10) NOT NULL UNIQUE,
    creation_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    modifiation_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY(id)
);
