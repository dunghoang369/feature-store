FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y libgomp1

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt