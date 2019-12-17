FROM ubuntu:latest

EXPOSE 5000

#RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD python imubitChallenge.py -p 5001:5000