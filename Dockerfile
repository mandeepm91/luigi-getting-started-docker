FROM python:3.7
RUN mkdir /src
COPY . /src
WORKDIR /src
RUN pip install -r requirements.txt