FROM python:3.10-bullseye

WORKDIR /app/

COPY ./requirements.txt /tmp/requirements.txt
COPY ./gpt3bot /app/gpt3bot

WORKDIR /tmp/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR /app/