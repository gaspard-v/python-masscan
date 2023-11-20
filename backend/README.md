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
