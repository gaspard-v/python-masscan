# Python masscanner

A Python scanner that find open proxies.

## settings.json file

All keys must be present. Please use the `settings.example.json`

- `logging_file` Logging settings file, content shouldn't be modified. Default is `logging.ini`
- `masscan_executable` masscan executable path, shouldn't be modified. Default is `masscan`
- `masscan_binary_file` masscan stores proxies IPs in this file, in binary format. Default is `./masscan-open-proxy.bin`
- `masscan_json_file` masscan stores proxies IPs in the file too, in JSON format. Default is `./masscan-open-proxy.json`
- `masscan_plain_file` contains all IPs and ports in this format `1.1.1.1:3128`, this file is then used by nmap. Default is `./masscan-open-proxy.txt`
- `blacklist_file` contains all blacklisted IP ranges. Masscan will not scan then. Format is like `192.168.1.0/24`. Default is `./ipblacklist.txt`
- `port` port scanned by masscan. Default is `3128`
- `type` service scanner by masscan. Default is `http` and shouldn't be modified
- `mariadb_user` DEPRECIATED mariadb user
- `mariadb_password` DEPRECIATED mariadb password
- `mariadb_host` DEPRECIATED mariadb host
- `mariadb_database` DEPRECIATED mariadb database
- `mariadb_kwargs` DEPRECIATED mariadb addiationnals args. Default is `autocommit: true`
- `api_url` Full URI of the backend service
- `api_token` Token used to store data with the API (check `backend/README.md` file)
- `nmap_executable` nmap executable path, shouldn't be modified. Default is `nmap`
- `nmap_plain_file` nmap scan result in plain file format. Default is `./nmap_scan_$DATETIME.txt`
- `nmap_xml_file` nmap scan result in xml file format. Default is `./nmap_scan_$DATETIME.xml`
- `open_proxy_file` contains all open proxy in `1.1.1.1:3218` format. Default is `./open_proxy_$DATETIME.txt`
- `nmap_additional_args` nmap additional args
- `masscan_additional_args` masscan additional args
- `print_stdout` print nmap and masscan stdout. Default is `true`
- `print_stderr` print nmap and masscan stderr. Default is `true`

## Logs file

Logs file is `proxyscan.log`

## Build

### Docker image

1. Use `docker compose up --build` command
