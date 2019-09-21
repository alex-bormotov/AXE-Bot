FROM python:3.7.4-slim-stretch

RUN apt-get update \
    && apt-get -y install curl build-essential libssl-dev \
    && apt-get clean \
    && pip3 install --upgrade pip


RUN mkdir /axe-bot
WORKDIR /axe-bot


ENV LD_LIBRARY_PATH /usr/local/lib


COPY requirements.txt /axe-bot/
RUN pip3 install numpy --no-cache-dir \
  && pip3 install -r requirements.txt --no-cache-dir


COPY . /axe-bot/


CMD [ "python3", "./bot.py" ]
