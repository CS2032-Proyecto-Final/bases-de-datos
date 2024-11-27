FROM python:3.9-slim

RUN pip3 install --no-cache-dir os boto3

RUN mkdir -p ~/.aws

WORKDIR /usr/src/app
COPY . .

# Declarar variable de entorno disponible para los scripts

CMD ["sh", "-c", "python3 ./pull_users.py && python3 ./load_users.py && tail -f /dev/null"]
