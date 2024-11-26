FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir psycopg2 boto3

RUN mkdir -p ~/.aws

WORKDIR /usr/src/app
COPY . .

CMD ["python3", "./pull_user.py"]

CMD ["python3", "./load_users.py"]