FROM python:3.8

WORKDIR /HlebBot
COPY requirements.txt /HlebBot
RUN pip install -r requirements.txt
COPY . /HlebBot
