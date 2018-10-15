FROM python:3.6-slim
ENV PYTHONUNBUFFERED 1

RUN mkdir /djangocrawler
WORKDIR /djangocrawler
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . /djangocrawler/
