FROM ubuntu:latest

EXPOSE 5000

#RUN mkdir /appl
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY venv /app

CMD python _init_.py