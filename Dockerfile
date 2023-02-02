FROM python:alpine
WORKDIR /python-masscan
RUN apk add --no-cache nmap masscan mariadb-dev build-base openssl
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk del mariadb-dev build-base
COPY . .
CMD ["python", "main.py"]