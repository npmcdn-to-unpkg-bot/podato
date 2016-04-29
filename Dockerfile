FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN apt-get install libpq-dev
RUN apt-get install libevent-dev

RUN curl -sL https://deb.nodesource.com/setup_5.x | bash -
RUN apt-get install -y nodejs

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -U pip
RUN pip install -r requirements.txt
ADD . /code/

RUN npm install -g webpack
RUN npm install