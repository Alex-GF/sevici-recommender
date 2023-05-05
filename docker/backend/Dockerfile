FROM python:3.8.13-alpine3.16

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN apk add --no-cache git postgresql-dev libc-dev gcc nano bash
RUN apk add --no-cache g++ make libffi-dev python3-dev build-base
RUN apk add py3-pip py3-pillow py3-cffi py3-brotli musl-dev pango
RUN apk add --no-cache geos gdal


WORKDIR /usr/src/app/sevici-api

COPY ./sevici_api .

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN pip install ipdb
RUN pip install ipython
RUN chmod +x /usr/src/app/sevici-api/entrypoint.sh