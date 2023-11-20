# python-masscan-backend

A NodeJS backend to store data sent by python scanners.

## Build

### Docker image

1. Create a `.env.docker` file (use the `.env.docker.example`)
2. Change variables in the `.env.docker` like database informations
3. Init the build with `docker compose up --build`

## Run

### With Docker

1. Run `docker compose up -d`

## Token

The backend works with token and permissions.
Each token has it ows permissions.

### permissions

permissions are

- `proxy_read` : Allows access to proxies informations
- `proxy_write` : Allows the creation of new proxies informations
- `proxy_update` : Allows changes of already created proxies informations
- `proxy_delete` : Allows supression of proxies informations
- `proxy_all` : Gives all proxies informations permissions
- `token_read` : Allows access to tokens permissions
- `token_create` : Allows the creation of new tokens
- `token_update` : Allows changes of already created token
- `token_delete` : Allow supression of already created tokens
- `proxy_all` : Give all tokens permissions
- `all_all` : Give all permissions

### token

Token are 10 random characters.

### Create a token

to create a token, use the `add_token` and `add_token_permission` mariadb procedures

## Env file

```bash
 ## Listen port. default = 8080
PORT=8080

## Listen address or host. default = localhost
LISTEN_HOST="localhost"

## Database Host or Address. MUST BE DEFINED
DB_HOST=""

## Database user. MUST BE DEFINED
DB_USER=""

## Database password. MUST BE DEFINED
DB_PASSWORD=""

## Database name. MUST BE DEFINED
DB_DATABASE=""

## Database port. Default = 3306
DB_PORT=3306

## Enable development mode, define this variable to enable DEV mod. Default is disabled
#DEV=1
```
