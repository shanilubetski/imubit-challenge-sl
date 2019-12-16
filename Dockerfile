FROM ubuntu:latest

EXPOSE 5000

RUN mkdir /app
WORKDIR /app

RUN set -xe \
    && apt-get update \
    && apt-get install python-pip

RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY venv /app

CMD python _init_.py