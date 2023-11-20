# python-masscan

A Python internet scanner that finds open HTTP proxies.

Python masscan use masscan and nmap with the `http-open-proxy.nse` script to get open HTTP proxies.
The projet has two main components

1. The scanner
2. The backend

Scanners scan the internet, find open proxies, then connect to the NodeJS backend and store them in a database.

Please read `scanner/README.md` and `backend/README.md`
