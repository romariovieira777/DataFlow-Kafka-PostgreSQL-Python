FROM public.ecr.aws/docker/library/python:3.12-alpine

RUN apk add --no-cache bash gcc musl-dev libffi-dev librdkafka-dev

RUN pip3 install --upgrade pip && mkdir /src

COPY requirements.txt ./requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt

COPY src /src
COPY main.py ./main.py

WORKDIR /src

EXPOSE 80